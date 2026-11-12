from retrieval.hybrid.hybrid_retriever import HybridRetriever


def main():

    query = "What are the principles of natural justice in disciplinary proceedings?"

    print("========================================")
    print("HYBRID RETRIEVAL TEST")
    print("========================================")

    print("\nLoading hybrid retriever...")

    retriever = HybridRetriever()

    print("\nRunning hybrid search...")

    results = retriever.query(
        query,
        top_k=10,
        retrieval_k=20
    )

    print("\n========================================")
    print("HYBRID RESULTS")
    print("========================================")

    for i, result in enumerate(
        results,
        start=1
    ):

        print(f"\n--- RESULT {i} ---")

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
            f"Citation: "
            f"{result['citation']}"
        )

        print(
            f"Vector Rank: "
            f"{result['vector_rank']}"
        )

        print(
            f"BM25 Rank: "
            f"{result['bm25_rank']}"
        )

        print(
            f"Vector Score: "
            f"{result['vector_score']}"
        )

        print(
            f"BM25 Score: "
            f"{result['bm25_score']}"
        )


if __name__ == "__main__":
    main()