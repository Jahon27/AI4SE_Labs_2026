"""Calculate Macro Multiset F1 for the Task 2 Text-to-SQL predictions."""

import csv
import json
import importlib.util
import sqlite3
from collections import Counter, defaultdict, deque
from pathlib import Path


TASK3_DIR = Path(__file__).resolve().parent
TASK2_DATA_DIR = TASK3_DIR.parent / "Task_2" / "data"
LABELS_PATH = TASK2_DATA_DIR / "restaurants_dataset.csv"
PREDICTION_PATHS = {
    "RTF": TASK2_DATA_DIR / "predictions_rtf.csv",
    "CO-STAR": TASK2_DATA_DIR / "predictions_costar.csv",
    "ToT": TASK2_DATA_DIR / "predictions_tot.csv",
}
OUTPUT_PATH = TASK3_DIR / "task3_results.csv"


def task2_evaluator():
    """Load Task 2's evaluator module without modifying the Task 2 files."""
    evaluator_path = TASK2_DATA_DIR / "evaluate_retrieval_predictions.py"
    spec = importlib.util.spec_from_file_location("task2_evaluator", evaluator_path)
    if spec is None or spec.loader is None:
        raise ImportError(f"Could not load Task 2 evaluator from {evaluator_path}")
    evaluator = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(evaluator)
    return evaluator


def row_multiset(rows):
    return Counter(tuple(row) for row in rows)


def multiset_f1(expected, predicted):
    """Return F1 for two row multisets, treating two empty results as perfect."""
    expected_counts = row_multiset(expected)
    predicted_counts = row_multiset(predicted)
    true_positives = sum((expected_counts & predicted_counts).values())
    expected_count = sum(expected_counts.values())
    predicted_count = sum(predicted_counts.values())

    if expected_count == 0 and predicted_count == 0:
        return 1.0
    if expected_count == 0 or predicted_count == 0:
        return 0.0
    return 2 * true_positives / (expected_count + predicted_count)


def load_labels():
    labels_by_question = defaultdict(deque)
    with LABELS_PATH.open(encoding="utf-8", newline="") as source:
        for line_number, row in enumerate(csv.DictReader(source), start=2):
            try:
                result = json.loads(row["result"])
            except json.JSONDecodeError as error:
                raise ValueError(
                    f"Invalid JSON label result on line {line_number} of {LABELS_PATH}"
                ) from error
            if not isinstance(result, list):
                raise ValueError(
                    f"Expected a JSON array label result on line {line_number} "
                    f"of {LABELS_PATH}"
                )
            labels_by_question[row["question"]].append(result)
    return labels_by_question


def evaluate(prediction_path, labels_by_question, connection):
    scores = []
    sql_errors = 0
    with prediction_path.open(encoding="utf-8", newline="") as source:
        for line_number, row in enumerate(csv.DictReader(source), start=2):
            question = row["question"]
            if not labels_by_question[question]:
                raise ValueError(
                    f"No matching label question for prediction on line "
                    f"{line_number}: {question!r}"
                )

            expected_rows = labels_by_question[question].popleft()
            try:
                predicted_rows = connection.execute(row["predicted_sql"]).fetchall()
            except sqlite3.Error:
                sql_errors += 1
                scores.append(0.0)
                continue
            scores.append(multiset_f1(expected_rows, predicted_rows))

    unmatched_labels = sum(len(results) for results in labels_by_question.values())
    if unmatched_labels:
        raise ValueError(
            f"{unmatched_labels} label records had no corresponding prediction"
        )
    if not scores:
        raise ValueError(f"No predictions found in {prediction_path}")
    return sum(scores) / len(scores), sql_errors, len(scores)


def main():
    csv.field_size_limit(1_000_000_000)
    evaluator = task2_evaluator()
    labels = load_labels()
    summaries = []

    connection = evaluator.load_database()
    try:
        for framework, prediction_path in PREDICTION_PATHS.items():
            framework_labels = defaultdict(deque)
            for question, results in labels.items():
                framework_labels[question] = deque(results)
            macro_f1, sql_errors, question_count = evaluate(
                prediction_path, framework_labels, connection
            )
            summaries.append(
                {
                    "framework": framework,
                    "questions": question_count,
                    "macro_multiset_f1": f"{macro_f1:.6f}",
                    "macro_multiset_f1_percent": f"{100 * macro_f1:.2f}",
                    "sql_errors": sql_errors,
                }
            )
            print(
                f"{framework}: Macro Multiset F1 = {100 * macro_f1:.2f}% "
                f"({question_count} questions; {sql_errors} SQL errors)"
            )
    finally:
        connection.close()

    with OUTPUT_PATH.open("w", encoding="utf-8", newline="") as output:
        writer = csv.DictWriter(output, fieldnames=summaries[0].keys())
        writer.writeheader()
        writer.writerows(summaries)
    print(f"Saved: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
