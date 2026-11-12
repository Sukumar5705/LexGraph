from pathlib import Path
import json

import faiss
import numpy as np


def build_faiss_index():
    project_root = Path(__file__).resolve().parents[2]

    embeddings_path = (
        project_root
        / "data"
        / "embeddings"
        / "embeddings_2023.npy"
    )

    chunks_path = (
        project_root
        / "data"
        / "processed"
        / "chunks_2023.jsonl"
    )

    output_dir = project_root / "data" / "vectorstore"
    output_dir.mkdir(parents=True, exist_ok=True)

    index_path = output_dir / "faiss_2023.index"
    mapping_path = output_dir / "chunk_mapping_2023.json"

    print("Loading embeddings...")
    embeddings = np.load(embeddings_path).astype("float32")

    print(f"Embedding shape: {embeddings.shape}")

    # Because embeddings were generated with normalize_embeddings=True,
    # inner product is equivalent to cosine similarity.
    dimension = embeddings.shape[1]

    index = faiss.IndexFlatIP(dimension)

    print("Adding embeddings to FAISS...")
    index.add(embeddings)

    print(f"FAISS index size: {index.ntotal}")

    # Keep the relationship:
    # FAISS vector position -> chunk record
    print("Building chunk mapping...")

    mapping = []

    with chunks_path.open("r", encoding="utf-8") as file:
        for line_number, line in enumerate(file):
            chunk = json.loads(line)

            mapping.append(
                {
                    "vector_id": line_number,
                    "case_id": chunk["case_id"],
                    "chunk_index": chunk["chunk_index"],
                    "title": chunk["title"],
                    "citation": chunk["citation"],
                    "decision_date": chunk["decision_date"],
                }
            )

    if len(mapping) != index.ntotal:
        raise ValueError(
            f"Mismatch: FAISS has {index.ntotal} vectors "
            f"but mapping has {len(mapping)} chunks."
        )

    print("Saving FAISS index...")
    faiss.write_index(index, str(index_path))

    print("Saving chunk mapping...")
    with mapping_path.open("w", encoding="utf-8") as file:
        json.dump(mapping, file, ensure_ascii=False, indent=2)

    print("\n--- COMPLETE ---")
    print(f"Vectors indexed: {index.ntotal}")
    print(f"Dimension: {dimension}")
    print(f"FAISS index: {index_path}")
    print(f"Chunk mapping: {mapping_path}")


if __name__ == "__main__":
    build_faiss_index()