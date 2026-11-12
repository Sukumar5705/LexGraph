from pathlib import Path
import json

import faiss
import numpy as np


class VectorStore:
    """
    Wrapper around the existing FAISS vector index
    and its chunk metadata mapping.
    """

    def __init__(self):

        project_root = Path(__file__).resolve().parents[2]

        self.index_path = (
            project_root
            / "data"
            / "vectorstore"
            / "faiss_2023.index"
        )

        self.mapping_path = (
            project_root
            / "data"
            / "vectorstore"
            / "chunk_mapping_2023.json"
        )

        self.chunks_path = (
            project_root
            / "data"
            / "processed"
            / "chunks_2023.jsonl"
        )

        print("Loading FAISS index...")

        self.index = faiss.read_index(
            str(self.index_path)
        )

        print(
            f"FAISS index loaded: "
            f"{self.index.ntotal} vectors"
        )

        print("Loading chunk mapping...")

        with self.mapping_path.open(
            "r",
            encoding="utf-8"
        ) as file:

            self.mapping = json.load(file)

        print(
            f"Chunk mapping loaded: "
            f"{len(self.mapping)} entries"
        )

        print("Loading chunks...")

        self.chunks = []

        with self.chunks_path.open(
            "r",
            encoding="utf-8"
        ) as file:

            for line in file:
                self.chunks.append(
                    json.loads(line)
                )

        print(
            f"Chunks loaded: "
            f"{len(self.chunks)}"
        )

    def query(
        self,
        vector,
        top_k=10
    ):
        """
        Search the FAISS index.

        Returns metadata together with the
        actual legal chunk text.
        """

        vector = np.asarray(
            vector,
            dtype=np.float32
        )

        if vector.ndim == 1:
            vector = vector.reshape(1, -1)

        distances, indices = self.index.search(
            vector,
            top_k
        )

        results = []

        for score, vector_id in zip(
            distances[0],
            indices[0]
        ):

            if vector_id < 0:
                continue

            metadata = self.mapping[vector_id]

            chunk = self.chunks[vector_id]

            result = {
                "vector_id": int(vector_id),

                "score": float(score),

                "case_id": metadata.get(
                    "case_id"
                ),

                "chunk_index": metadata.get(
                    "chunk_index"
                ),

                "title": metadata.get(
                    "title"
                ),

                "citation": metadata.get(
                    "citation"
                ),

                "decision_date": metadata.get(
                    "decision_date"
                ),

                "text": chunk.get(
                    "text",
                    ""
                ),

                "source": "vector",
            }

            results.append(result)

        return results