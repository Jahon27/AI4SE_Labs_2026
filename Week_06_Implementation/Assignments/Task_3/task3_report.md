# Task 3 Report

I asked Copilot to generate the embeddings and implement the search function. At first, I chose `BAAI/bge-small-en-v1.5` because it is lightweight, free, works locally, and is suitable for semantic search. After testing it with coding queries, I noticed that some results were not very relevant. For example, a query about file operations returned decorator and test chunks instead of clear file-reading code.

I then asked Copilot to switch to `jinaai/jina-embeddings-v2-base-code`, because this model is designed specifically for code search. The Jina model gave better results for the query about recording function calls and tracking exceptions. Its top result was `playground/playground/decorators.py`, which correctly contains the function-call and exception tracking code.

The embeddings are stored in JSON together with each chunk's file path, ID, and content. For searching, the script converts the user's query into an embedding and use cosine similarity to compare it with all stored vectors. The three highest scores are returned. The final model generated 768-dimensional embeddings for all 102 chunks.
