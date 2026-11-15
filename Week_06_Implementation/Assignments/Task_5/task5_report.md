# Task 5 Report

Here I asked GitHub Copilot to create a Python script that would automatically generate the missing code. The script uses the Jina embedding model to convert each task description into an embedding. It then finds the five most relevant code chunks using cosine similarity and sends them together with the task description and method context to gpt-6-luna.

I chose gpt-6-luna because I wanted to get better results when generating Python code.

There were 10 missing methods, and the pipeline generated all of them. After the first test run, two tests failed because some generated methods did not behave as expected. I asked Copilot to use the failing tests as additional context and regenerate those methods through the pipeline.

After a few retries, all 481 unit tests passed successfully, with no failures. I also encountered a small API issue because the model did not support temperature=0, so Copilot used the default temperature instead. No unit tests were modified.
