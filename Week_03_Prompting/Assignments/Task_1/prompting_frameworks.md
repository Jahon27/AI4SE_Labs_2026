# RTF — Natural Language to SQL

## Role
You are a Text-to-SQL expert specializing in SQLite with access to the VS Code workspace.

## Task
Convert all questions from `data/restaurants_dataset.csv` into SQL queries.

- Use `data/restaurants-schema.csv` and `data/restaurants-db.txt`.
- Ignore irrelevant information.
- Use only existing tables and columns.
- Do not use the dataset's `result` column.

## Format
Save results to `data/predictions_rtf.csv` with columns:
`question,[predicted_sql]`

- One valid SQLite SELECT query per question.
- Preserve original questions and order.
- No explanations or Markdown in SQL fields.
- For unanswerable questions, use `SELECT NULL WHERE 1 = 0;`.
- Record the model name and execution time separately.
- Do not modify source files.

---

## Input
`data/restaurants_dataset.csv`

# CO-STAR — Natural Language to SQL

## Context
The project contains a restaurant database and 155 natural language questions.
The RTF baseline achieved 27.74% accuracy.

Available files:
- `data/restaurants-schema.csv` — database structure.
- `data/restaurants-db.txt` — restaurant records.
- `data/restaurants_dataset.csv` — questions and evaluation labels.

## Objective
Generate accurate SQLite SELECT queries for all 155 questions.
Correctly identify restaurant names, cities, food types, streets, and rating conditions.
Ignore irrelevant text and never use evaluation labels.

## Style
Use precise SQL syntax and appropriate JOIN operations.
Extract each condition independently.
Use only existing tables and columns.
Avoid unnecessary complexity and assumptions.

## Tone
Technical, direct, and deterministic.
No explanations or conversational responses in predictions.

## Audience
The output is intended for an automated SQLite evaluator that compares query results against expected database results.

## Response
Save predictions to `data/predictions_costar.csv`.

Required CSV columns:
`question,predicted_sql`

Requirements:
- Exactly 155 predictions in the original order.
- Each query must return `RESTAURANT.ID, RESTAURANT.NAME`.
- Use valid SQLite SELECT statements.
- Preserve original questions exactly.
- Do not use the dataset's `result` column.
- Do not modify source files or previous RTF predictions.
- Record the model name and execution time separately.
- Do not include explanations or Markdown in the CSV.

---

## Input
`data/restaurants_dataset


# Tree of Thoughts (ToT) — Natural Language to SQL

## Problem
Generate accurate SQLite queries for 155 restaurant questions.
Use `data/restaurants-schema.csv` and `data/restaurants-db.txt`.
Ignore irrelevant text. Never use the dataset's `result` column.

## BRANCH
For each question, consider 3 different SQL approaches:
1. Direct filtering.
2. JOIN-based filtering.
3. Subquery-based filtering.

## EVALUATE
Score each approach from 1–5 based on:
- SQL correctness.
- Coverage of question constraints.
- Simplicity.
- Limitations for future modifications.

Briefly justify each score.

## PRUNE
Discard the weakest approach.
Check the remaining candidates for missing conditions and incorrect columns.

## DECIDE
Select the most accurate valid SQLite query.
Use only existing tables and columns.

## Response
Save all predictions to `data/predictions_tot.csv` with exactly:
`question,predicted_sql`

- Preserve all 155 questions and their order.
- Return `RESTAURANT.ID, RESTAURANT.NAME`.
- Use SELECT queries only.
- No reasoning, explanations, or Markdown in the CSV.
- Do not modify previous predictions or source files.
- Record model name and execution time separately.

Example evaluation (internal only):
```text
Candidate 1: 4/5 — simple but incomplete.
Candidate 2: 5/5 — correct JOIN and filters.
Candidate 3: 3/5 — unnecessary complexity.
Decision: Candidate 2.