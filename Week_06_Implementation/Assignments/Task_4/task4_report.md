# Task 4 Report

To complete task, I asked Copilot agent to create a Python script called match_embeddings.py. Since I already had 102 embeddings from Task 3, I decided to reuse them instead of generating new ones.

I chose cosine similarity because it is a common method for comparing embeddings and finding similar vectors. I also decided to use a simple linear search because the dataset is quite small, so there was no need for a more complicated solution like a vector database.

The script compares the input embedding with all stored embeddings, sorts them by similarity, and returns the top n results. This means I can choose how many chunks I want to retrieve.

After implementing the script, I asked Copilot to test it with n=3 and n=5. Both tests worked correctly and returned the requested number of chunks in the correct order. Copilot also checked invalid inputs, such as negative values of n and incorrect embedding dimensions.
