from typing import List, Dict

from sentence_transformers import CrossEncoder


MODEL_NAME = "cross-encoder/ms-marco-MiniLM-L-6-v2"


class CrossEncoderReranker:
    """
    Cross-encoder reranker for legal retrieval candidates.

    Takes:
        query + retrieved legal text

    and produces a relevance score for each candidate.
    """

    def __init__(self):

        print(
            f"Loading cross-encoder: {MODEL_NAME}"
        )

        self.model = CrossEncoder(
            MODEL_NAME
        )

    def rerank(
        self,
        query: str,
        results: List[Dict],
        top_k: int = 10
    ) -> List[Dict]:
        """
        Rerank retrieval results using the
        cross-encoder relevance score.
        """

        if not results:
            return []

        pairs = []

        for result in results:

            text = result.get(
                "text",
                ""
            )

            pairs.append(
                [
                    query,
                    text
                ]
            )

        print(
            f"Scoring {len(pairs)} candidates..."
        )

        scores = self.model.predict(
            pairs
        )

        reranked = []

        for result, score in zip(
            results,
            scores
        ):

            updated_result = dict(result)

            updated_result[
                "cross_encoder_score"
            ] = float(score)

            reranked.append(
                updated_result
            )

        reranked.sort(
            key=lambda x: x[
                "cross_encoder_score"
            ],
            reverse=True
        )

        return reranked[:top_k]