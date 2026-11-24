# Assessment by mimo-2.6-flash

# Week 03 Prompting
- Awarded: 1.5b out of 5b
- Commentary: All three prompts were formulated and actually used to generate 155-question prediction sets with an evaluation script, so the core pipeline exists. However, every task is partially complete: required justification/provenance reports (Task 1), visualisation and credible inference-time measurement (Task 2), and the metric defence/comparison report (Task 3) are missing, and Task 4 contains only the assignment description with no student report. The identical 27.74% accuracy across all three prompts and the duplicated/copy-pasted metadata (identical RTF and CO-STAR timestamps and 1019.53 ms timings, ToT metadata pointing at predictions_rtf.csv) further weaken confidence in the experimental rigor.

## Task 1
- Awarded: 0.5b   (max 1b)
- Commentary: Three valid, non-ROSES, non-zero-shot frameworks are used (RTF, CO-STAR, Tree of Thoughts) and the prompts in prompting_frameworks.md are concretely tailored to the Task 2 Text-to-SQL problem, specifying inputs, output CSV schema, 155-row ordering, and anti-leakage rules; they were demonstrably carried into Task 2. However, the explicitly required report explaining why each framework was chosen and where it was found is entirely absent — there is no rationale, expectation, or source citation anywhere in Task_1, and ToT is more a reasoning procedure than a prompt framework (an unremarked substitution).

## Task 2
- Awarded: 0.5b   (max 1b)
- Commentary: Three separate prediction files (155 rows each, genuinely differing SQL between frameworks), metadata files, an evaluation script, and a brief comparison report with a summary table are present, satisfying the "solutions + report" core. Shortcomings: the required "nice visualisation" is missing (no image or chart anywhere in Task_2); inference times are not discussed in the report and the metadata is unreliable — RTF and CO-STAR share identical 1019.53 ms timings and identical timestamps (indicating copied rather than measured values, and 1 s for 155 generations is implausible), while the ToT metadata uses a different schema and mislabels its source as predictions_rtf.csv. All three frameworks reporting exactly 43/155 despite visibly different queries is also insufficiently scrutinised in the report.

## Task 3
- Awarded: 0.5b   (max 1b)
- Commentary: custom_metric.py is a solid, runnable implementation of Macro Multiset F1 (partial-credit row-multiset F1 averaged over questions, graceful handling of SQL errors and empty-vs-empty results, reuse of the Task 2 evaluator's DB loader, and per-framework label copies to avoid state bleed), and task3_results.csv reports values for all three prompts. Missing are both written deliverables: there is no report arguing/defending why this metric is good and applicable, no discussion of whether it complements or replaces exact-match accuracy, and no comparative narrative over the metric values (which differ only at the sixth decimal, 0.277419/0.277419/0.277421 — essentially indistinguishable from the original accuracy, a point the student never addresses).

## Task 4
- Awarded: 0b   (max 2b)
- Commentary: Only the Task_4.md assignment description exists. No detailed analysis, no tables or graphs, no statistical significance test, and no discussion of prompt/model/coding-agent factors were submitted, so no credit can be awarded.