from retrieval.hybrid.hybrid_retriever import HybridRetriever
from retrieval.reranking.cross_encoder import CrossEncoderReranker


def main():

    query = "What are the principles of natural justice in disciplinary proceedings?"

    print("========================================")
    print("CROSS-ENCODER RERANKER TEST")
    print("========================================")

    print("\n1. Loading hybrid retriever...")

    hybrid = HybridRetriever()

    print("\n2. Running hybrid retrieval...")

    hybrid_results = hybrid.query(
        query,
        top_k=10,
        retrieval_k=20
    )

    print(
        f"Hybrid candidates: "
        f"{len(hybrid_results)}"
    )

    print("\n3. Loading cross-encoder...")

    reranker = CrossEncoderReranker()

    print("\n4. Running cross-encoder reranking...")

    results = reranker.rerank(
        query,
        hybrid_results,
        top_k=10
    )

    print("\n========================================")
    print("CROSS-ENCODER RESULTS")
    print("========================================")

    for i, result in enumerate(
        results,
        start=1
    ):

        print(f"\n--- RESULT {i} ---")

        print(
            f"Cross-Encoder Score: "
            f"{result['cross_encoder_score']:.6f}"
        )

        print(
            f"RRF Score: "
            f"{result['rrf_score']:.6f}"
        )

        print(
            f"Case ID: "
            f"{result['case_id']}"
        )

        print(
            f"Title: "
            f"{result['title']}"
        )

        print(
            f"Chunk Index: "
            f"{result['chunk_index']}"
        )

        text = result.get(
            "text",
            ""
        )

        print(
            f"Text Preview: "
            f"{text[:200].replace(chr(10), ' ')}..."
        )


if __name__ == "__main__":
    main()