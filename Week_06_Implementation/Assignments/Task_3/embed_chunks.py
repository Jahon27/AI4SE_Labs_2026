import json
import math
from pathlib import Path

from sentence_transformers import SentenceTransformer


TASK_3_FOLDER = Path(__file__).parent
CHUNKS_FILE = TASK_3_FOLDER.parent / "Task_2" / "chunks.json"
EMBEDDINGS_FILE = TASK_3_FOLDER / "chunk_embeddings.json"
MODEL_NAME = "jinaai/jina-embeddings-v2-base-code"


def cosine_similarity(first, second):
    first_length = math.sqrt(sum(value * value for value in first))
    second_length = math.sqrt(sum(value * value for value in second))
    if first_length == 0 or second_length == 0:
        return 0.0
    dot_product = sum(left * right for left, right in zip(first, second))
    return dot_product / (first_length * second_length)


def load_model():
    return SentenceTransformer(MODEL_NAME, trust_remote_code=True)


def search(query, model=None, top_k=3):
    if model is None:
        model = load_model()

    query_embedding = model.encode(query).tolist()
    chunks = json.loads(EMBEDDINGS_FILE.read_text(encoding="utf-8"))
    results = []

    for chunk in chunks:
        score = cosine_similarity(query_embedding, chunk["embedding"])
        results.append(
            {
                "file_path": chunk["file_path"],
                "chunk_id": chunk["chunk_id"],
                "similarity": score,
                "content": chunk["content"],
            }
        )

    return sorted(results, key=lambda result: result["similarity"], reverse=True)[:top_k]


def create_embeddings(model):
    chunks = json.loads(CHUNKS_FILE.read_text(encoding="utf-8"))
    contents = [chunk["content"] for chunk in chunks]
    embeddings = model.encode(contents)
    embedded_chunks = []

    for chunk, embedding in zip(chunks, embeddings):
        embedded_chunks.append(
            {
                "file_path": chunk["file_path"],
                "chunk_id": chunk["chunk_id"],
                "content": chunk["content"],
                "embedding": embedding.tolist(),
            }
        )

    EMBEDDINGS_FILE.write_text(
        json.dumps(embedded_chunks, indent=2),
        encoding="utf-8",
    )
    return embedded_chunks


def main():
    if not CHUNKS_FILE.is_file():
        raise FileNotFoundError(f"Chunks file not found: {CHUNKS_FILE}")

    model = load_model()
    chunks = create_embeddings(model)
    print(f"Created {EMBEDDINGS_FILE} with {len(chunks)} embeddings.")

    print("Example search results:")
    for result in search("How are orders processed?", model):
        print(
            f"- {result['file_path']} (chunk {result['chunk_id']}, "
            f"score {result['similarity']:.4f})"
        )


if __name__ == "__main__":
    main()
