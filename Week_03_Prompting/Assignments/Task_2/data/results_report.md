### RTF Results

The RTF framework achieved an accuracy of 27.74% (43/155).

The model successfully generated SQL queries for some questions, but struggled with extracting correct conditions from complex natural language inputs, especially those containing irrelevant text.

This result will serve as a baseline for comparison with other prompting frameworks.

### CO-STAR Results

The CO-STAR framework achieved an accuracy of **27.74% (43/155)**.

Despite providing more structured instructions through Context, Objective, Style, Tone, Audience, and Response, CO-STAR did not improve overall accuracy compared to RTF.

This suggests that more detailed prompt instructions do not necessarily lead to better SQL generation performance.

### Tree of Thoughts (ToT) Results

The Tree of Thoughts framework achieved an accuracy of **27.74% (43/155)**.

Despite generating and evaluating multiple SQL candidates before selecting the best one, ToT did not improve accuracy compared to RTF and CO-STAR.

### Comparison

| Framework | Accuracy | Correct Predictions |
|-----------|----------|---------------------|
| RTF | 27.74% | 43/155 |
| CO-STAR | 27.74% | 43/155 |
| ToT | 27.74% | 43/155 |

### Conclusion

Interestingly, all three prompting frameworks achieved **exactly the same accuracy of 27.74% (43/155)**.

This is a surprising result because RTF, CO-STAR, and ToT use different prompting strategies and levels of complexity.

The experiment suggests that more structured instructions and additional reasoning steps do not necessarily improve Text-to-SQL performance.

However, identical accuracy does not necessarily mean that all three frameworks generated identical SQL queries or correctly answered the same questions.