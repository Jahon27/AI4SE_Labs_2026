import json
import math
from pathlib import Path


EMBEDDINGS_FILE = (
    Path(__file__).parent.parent / "Task_3" / "chunk_embeddings.json"
)
EMBEDDING_DIMENSION = 768


def cosine_similarity(first, second):
    first_length = math.sqrt(sum(value * value for value in first))
    second_length = math.sqrt(sum(value * value for value in second))
    if first_length == 0 or second_length == 0:
        return 0.0

    dot_product = sum(left * right for left, right in zip(first, second))
    return dot_product / (first_length * second_length)


def match_embeddings(query_embedding, n):
    if n <= 0:
        raise ValueError("n must be greater than zero")
    if len(query_embedding) != EMBEDDING_DIMENSION:
        raise ValueError(
            f"query embedding must contain {EMBEDDING_DIMENSION} numbers"
        )

    stored_chunks = json.loads(EMBEDDINGS_FILE.read_text(encoding="utf-8"))
    matches = []
    for chunk in stored_chunks:
        score = cosine_similarity(query_embedding, chunk["embedding"])
        matches.append(
            {
                "file_path": chunk["file_path"],
                "chunk_id": chunk["chunk_id"],
                "similarity": score,
                "content": chunk["content"],
            }
        )

    matches.sort(key=lambda result: result["similarity"], reverse=True)
    return matches[:n]


def run_tests():
    stored_chunks = json.loads(EMBEDDINGS_FILE.read_text(encoding="utf-8"))
    query_embedding = stored_chunks[0]["embedding"]

    for number in (3, 5):
        results = match_embeddings(query_embedding, number)
        assert len(results) == number
        scores = [result["similarity"] for result in results]
        assert scores == sorted(scores, reverse=True)
        print(f"n={number}: returned {len(results)} sorted results")


if __name__ == "__main__":
    run_tests()
