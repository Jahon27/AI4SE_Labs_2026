# Task 3 — Custom Metric for Text-to-SQL

## Proposed Metric: Macro Multiset F1-score

Execution Accuracy only measures exact matches (1 or 0), ignoring partially correct results.

I chose **Macro Multiset F1-score**, which measures the overlap between predicted and expected SQL results, including duplicates.

**F1 = 2 × TP / (P + G)**

Where:
- TP - matching rows
- P - predicted rows
- G - expected rows

If both results are empty, F1 = 1. SQL errors receive F1 = 0. The final score is averaged across 155 questions.

## Why This Metric?

F1 rewards partially correct results and penalizes missing or extra rows.

It **complements Execution Accuracy** rather than replacing it, providing a more detailed evaluation of SQL query quality.

## Implementation

The metric was implemented in `custom_metric.py`, using the same database and predictions from Task 2.

## Results

| Framework | Accuracy | Macro Multiset F1 | SQL Errors |
|-----------|----------|-------------------|------------|
| RTF | 27.74% | 27.7419% | 0 |
| CO-STAR | 27.74% | 27.7419% | 0 |
| ToT | 27.74% | 27.7421% | 0 |

## Conclusion

Interestingly, all three frameworks achieved **almost identical results**, despite using different prompting strategies.

This is quite amusing, especially since ToT uses more complex reasoning than RTF and CO-STAR.

ToT performed slightly better, but the difference is negligible.

The experiment suggests that **more complex prompting does not necessarily improve performance**.

Although F1 did not reveal significant differences, it remains useful for measuring partial correctness.

## Limitations

F1 requires exact row matches, and empty expected and predicted results receive a perfect score, which may inflate the overall results.