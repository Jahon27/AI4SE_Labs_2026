# Task 2 Report

In this task, I was asked to split the cloned repository into smaller chunks that could later be used in a RAG system.

To complete this task, I asked GitHub Copilot agent to create a Python script that would read the source code files from the AI4SE_Playground repository and split them into smaller parts. I asked Copilot to use a chunk size of 50 lines because I thought it would be a good balance between keeping enough code context and making the chunks easy to search. The agent created a script called chunk_repository.py, which splits each file separately and skips unnecessary files like images, binary files, and Git-related files. I also asked Copilot to save the results in a JSON file because JSON is commonly used to store and exchange structured data in RAG pipelines. It is also simple to read and work with in Python. Each chunk contains the file path, chunk ID, and code content.

After running the script, Copilot generated 102 chunks from 26 source files and saved them in chunks.json. I then asked Copilot to check the implementation, and it confirmed that the script worked without errors.
