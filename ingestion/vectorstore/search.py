from pathlib import Path
import json

import faiss
from sentence_transformers import SentenceTransformer


MODEL_NAME = "BAAI/bge-small-en-v1.5"


def search(query, top_k=5):
    project_root = Path(__file__).resolve().parents[2]

    index_path = (
        project_root
        / "data"
        / "vectorstore"
        / "faiss_2023.index"
    )

    mapping_path = (
        project_root
        / "data"
        / "vectorstore"
        / "chunk_mapping_2023.json"
    )

    chunks_path = (
        project_root
        / "data"
        / "processed"
        / "chunks_2023.jsonl"
    )

    print("Loading model...")
    model = SentenceTransformer(MODEL_NAME)

    print("Loading FAISS index...")
    index = faiss.read_index(str(index_path))

    print("Loading mappings...")
    with mapping_path.open("r", encoding="utf-8") as file:
        mapping = json.load(file)

    print("Loading chunks...")
    chunks = []

    with chunks_path.open("r", encoding="utf-8") as file:
        for line in file:
            chunks.append(json.loads(line))

    query_embedding = model.encode(
        [query],
        normalize_embeddings=True,
        convert_to_numpy=True,
    )

    scores, indices = index.search(query_embedding, top_k)

    print("\n" + "=" * 80)
    print(f"QUERY: {query}")
    print("=" * 80)

    for rank, (score, vector_id) in enumerate(
        zip(scores[0], indices[0]),
        start=1,
    ):
        info = mapping[vector_id]
        chunk = chunks[vector_id]

        print(f"\n--- RESULT {rank} ---")
        print(f"Similarity: {score:.4f}")
        print(f"Case ID: {info['case_id']}")
        print(f"Title: {info['title']}")
        print(f"Citation: {info['citation']}")
        print(f"Decision date: {info['decision_date']}")
        print(f"Chunk index: {info['chunk_index']}")
        print("\nText:")
        print(chunk["text"][:1500])


if __name__ == "__main__":
    query = input("Enter legal query: ").strip()

    if query:
        search(query, top_k=5)