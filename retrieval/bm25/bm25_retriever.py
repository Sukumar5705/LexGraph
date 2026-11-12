from pathlib import Path
import json
import re

from rank_bm25 import BM25Okapi


class BM25Retriever:
    """
    BM25 keyword-based retriever over the 18,999 legal chunks.
    """

    def __init__(self):

        project_root = Path(__file__).resolve().parents[2]

        self.chunks_path = (
            project_root
            / "data"
            / "processed"
            / "chunks_2023.jsonl"
        )

        print("Loading chunks for BM25...")

        self.chunks = self._load_chunks()

        print(
            f"Chunks loaded: {len(self.chunks)}"
        )

        print("Building BM25 index...")

        self.tokenized_corpus = [
            self._tokenize(chunk["text"])
            for chunk in self.chunks
        ]

        self.bm25 = BM25Okapi(
            self.tokenized_corpus
        )

        print("BM25 index ready.")

    def _load_chunks(self):

        chunks = []

        with self.chunks_path.open(
            "r",
            encoding="utf-8"
        ) as file:

            for line in file:
                chunks.append(
                    json.loads(line)
                )

        return chunks

    def _tokenize(self, text):

        return re.findall(
            r"\b\w+\b",
            text.lower()
        )

    def query(
        self,
        query,
        top_k=10
    ):
        """
        Search the BM25 index.

        Returns a list of results containing
        chunk and case metadata.
        """

        query_tokens = self._tokenize(
            query
        )

        scores = self.bm25.get_scores(
            query_tokens
        )

        ranked_indices = scores.argsort()[::-1]

        results = []

        for index in ranked_indices:

            if len(results) >= top_k:
                break

            score = float(
                scores[index]
            )

            if score <= 0:
                continue

            chunk = self.chunks[index]

            results.append(
                {
                    "chunk_id": chunk.get(
                        "chunk_id"
                    ),
                    "chunk_index": chunk.get(
                        "chunk_index"
                    ),
                    "case_id": chunk.get(
                        "case_id"
                    ),
                    "title": chunk.get(
                        "title"
                    ),
                    "citation": chunk.get(
                        "citation"
                    ),
                    "decision_date": chunk.get(
                        "decision_date"
                    ),
                    "text": chunk.get(
                        "text"
                    ),
                    "score": score,
                    "source": "bm25",
                }
            )

        return results