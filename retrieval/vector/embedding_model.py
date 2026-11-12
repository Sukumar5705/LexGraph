from typing import List

import numpy as np
from sentence_transformers import SentenceTransformer


MODEL_NAME = "BAAI/bge-small-en-v1.5"


class EmbeddingModel:
    """
    Wrapper around the same embedding model used to build
    the existing FAISS index.
    """

    def __init__(self):
        print(f"Loading embedding model: {MODEL_NAME}")

        self.model = SentenceTransformer(
            MODEL_NAME
        )

    def embed(
        self,
        texts: List[str]
    ) -> List[List[float]]:
        """
        Convert text into normalized embeddings.
        """

        embeddings = self.model.encode(
            texts,
            normalize_embeddings=True,
            convert_to_numpy=True,
        )

        embeddings = embeddings.astype(
            np.float32
        )

        return embeddings.tolist()

    def embed_one(
        self,
        text: str
    ) -> List[float]:
        """
        Convert a single text into one normalized
        embedding vector.
        """

        embedding = self.model.encode(
            [text],
            normalize_embeddings=True,
            convert_to_numpy=True,
        )

        embedding = embedding.astype(
            np.float32
        )

        return embedding[0].tolist()