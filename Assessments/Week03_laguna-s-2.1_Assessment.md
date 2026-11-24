# Assessment by laguna-s-2.1

# Week 03 Prompting
- Awarded: 3.5b out of 5b
- Commentary: The student worked on a Text-to-SQL problem (Restaurants dataset, 155 questions) using the RTF, CO-STAR, and Tree of Thoughts prompting frameworks. The prediction data files and metric implementation are solid and well-structured, demonstrating good technical execution. However, Task 1 is missing the rationale report explaining framework choices and sources, Task 2 lacks the requested visualization and inference-time analysis, and Task 3 has no written report comparing the new metric values across prompts, despite a well-implemented Macro Multiset F1 metric. Task 4 carries no deliverables.

## Task 1
- Awarded: 0.5b   (max 1b)
- Commentary: The student formulated three distinct prompts (RTF, CO-STAR, ToT) in `Task_1/prompting_frameworks.md`, each correctly structured according to its framework conventions. The prompts are detailed and appropriate for the Text-to-SQL problem. However, the required report on why each framework was chosen and where it was found is absent — the file presents the framework structure but provides no rationale for the selections or source attribution. This constitutes roughly half of the required deliverables.

## Task 2
- Awarded: 0.5b   (max 1b)
- Commentary: Prediction files (`predictions_rtf.csv`, `predictions_costar.csv`, `predictions_tot.csv`) with 155 rows each and corresponding metadata files are present, satisfying the data-deliverable requirement. The `results_report.md` contains a comparison table showing all three frameworks achieved 27.74% accuracy (43/155). However, the report omits the explicitly requested visualization, and inference times are not discussed — the metadata files even show an identical 1019.53ms for RTF and CO-STAR, suggesting limited independent measurement. The RTF/CO-STAR predictions are nearly identical (e.g., the same city-name extraction bug on line 8), undermining the claim of an independent comparison.

## Task 3
- Awarded: 0.5b   (max 1b)
- Commentary: The `custom_metric.py` implementation of Macro Multiset F1 is well-designed and original — it complements the exact-match accuracy metric by rewarding partial overlap in result row multisets, which is valuable for Text-to-SQL where partial correctness matters. The implementation correctly loads the Task 2 evaluator, executes predictions against the database, and computes per-framework values in `task3_results.csv` (all around 27.74%, 0 SQL errors). However, no written report comparing the metric values across prompts is provided; the CSV contains raw numbers but no interpretation, discussion of what the metric reveals, or comparison to the original accuracy metric.

## Task 4
- Awarded: 2b   (max 2b)
- Commentary: No deliverables were required or submitted for this task.
