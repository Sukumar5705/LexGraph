from retrieval.vector.embedding_model import EmbeddingModel
from retrieval.vector.vector_store import VectorStore
from retrieval.bm25.bm25_retriever import BM25Retriever


class HybridRetriever:
    """
    Combines FAISS vector retrieval and BM25 retrieval
    using Reciprocal Rank Fusion (RRF).
    """

    def __init__(self):

        print("Initializing hybrid retriever...")

        self.embedding_model = EmbeddingModel()
        self.vector_store = VectorStore()
        self.bm25_retriever = BM25Retriever()

    def _rrf_score(self, rank, k=60):
        """
        Calculate Reciprocal Rank Fusion score.
        """

        return 1.0 / (k + rank)

    def query(
        self,
        query,
        top_k=10,
        retrieval_k=20
    ):
        """
        Perform hybrid retrieval using FAISS and BM25.

        Results are grouped at case level while retaining
        the strongest available legal chunk text.
        """

        # ---------------------------------------------
        # 1. Vector retrieval
        # ---------------------------------------------

        query_vector = self.embedding_model.embed_one(
            query
        )

        vector_results = self.vector_store.query(
            query_vector,
            top_k=retrieval_k
        )

        # ---------------------------------------------
        # 2. BM25 retrieval
        # ---------------------------------------------

        bm25_results = self.bm25_retriever.query(
            query,
            top_k=retrieval_k
        )

        # ---------------------------------------------
        # 3. Reciprocal Rank Fusion
        # ---------------------------------------------

        fused = {}

        for rank, result in enumerate(
            vector_results,
            start=1
        ):

            case_id = result.get("case_id")

            if not case_id:
                continue

            if case_id not in fused:

                fused[case_id] = {
                    "case_id": case_id,
                    "title": result.get("title"),
                    "citation": result.get("citation"),
                    "decision_date": result.get(
                        "decision_date"
                    ),
                    "text": result.get("text", ""),
                    "chunk_index": result.get(
                        "chunk_index"
                    ),
                    "rrf_score": 0.0,
                    "vector_rank": None,
                    "bm25_rank": None,
                    "vector_score": None,
                    "bm25_score": None,
                }

            fused[case_id]["rrf_score"] += (
                self._rrf_score(rank)
            )

            if fused[case_id]["vector_rank"] is None:

                fused[case_id]["vector_rank"] = rank

                fused[case_id]["vector_score"] = (
                    result.get("score")
                )

                fused[case_id]["text"] = (
                    result.get("text", "")
                )

                fused[case_id]["chunk_index"] = (
                    result.get("chunk_index")
                )

        for rank, result in enumerate(
            bm25_results,
            start=1
        ):

            case_id = result.get("case_id")

            if not case_id:
                continue

            if case_id not in fused:

                fused[case_id] = {
                    "case_id": case_id,
                    "title": result.get("title"),
                    "citation": result.get("citation"),
                    "decision_date": result.get(
                        "decision_date"
                    ),
                    "text": result.get("text", ""),
                    "chunk_index": result.get(
                        "chunk_index"
                    ),
                    "rrf_score": 0.0,
                    "vector_rank": None,
                    "bm25_rank": None,
                    "vector_score": None,
                    "bm25_score": None,
                }

            fused[case_id]["rrf_score"] += (
                self._rrf_score(rank)
            )

            if fused[case_id]["bm25_rank"] is None:

                fused[case_id]["bm25_rank"] = rank

                fused[case_id]["bm25_score"] = (
                    result.get("score")
                )

        # ---------------------------------------------
        # 4. Sort by fused score
        # ---------------------------------------------

        ranked_results = sorted(
            fused.values(),
            key=lambda x: x["rrf_score"],
            reverse=True
        )

        # ---------------------------------------------
        # 5. Return top cases
        # ---------------------------------------------

        return ranked_results[:top_k]