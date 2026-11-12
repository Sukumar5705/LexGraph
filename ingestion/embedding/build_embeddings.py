from pathlib import Path
import json

import numpy as np
from sentence_transformers import SentenceTransformer


MODEL_NAME = "BAAI/bge-small-en-v1.5"
BATCH_SIZE = 32


def load_chunks(input_path):
    chunks = []

    with input_path.open("r", encoding="utf-8") as file:
        for line in file:
            chunks.append(json.loads(line))

    return chunks


def build_embeddings():
    project_root = Path(__file__).resolve().parents[2]

    input_path = (
        project_root
        / "data"
        / "processed"
        / "chunks_2023.jsonl"
    )

    output_dir = project_root / "data" / "embeddings"
    output_dir.mkdir(parents=True, exist_ok=True)

    embeddings_path = output_dir / "embeddings_2023.npy"

    print("Loading chunks...")
    chunks = load_chunks(input_path)

    print(f"Chunks loaded: {len(chunks)}")

    print(f"Loading embedding model: {MODEL_NAME}")
    model = SentenceTransformer(MODEL_NAME)

    texts = [chunk["text"] for chunk in chunks]

    print("Generating embeddings...")
    embeddings = model.encode(
        texts,
        batch_size=BATCH_SIZE,
        show_progress_bar=True,
        normalize_embeddings=True,
        convert_to_numpy=True,
    )

    embeddings = embeddings.astype(np.float32)

    np.save(embeddings_path, embeddings)

    print("\n--- COMPLETE ---")
    print(f"Chunks: {len(chunks)}")
    print(f"Embedding shape: {embeddings.shape}")
    print(f"Embedding dimension: {embeddings.shape[1]}")
    print(f"Saved to: {embeddings_path}")


if __name__ == "__main__":
    build_embeddings()