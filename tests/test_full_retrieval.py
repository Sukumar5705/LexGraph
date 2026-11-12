from retrieval.hybrid.hybrid_retriever import HybridRetriever
from retrieval.reranking.authority_ranker import AuthorityRanker


def main():

    query = "right to be heard under the Forest Act and reserved forest"

    print("========================================")
    print("FULL RETRIEVAL PIPELINE TEST")
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

    print("\n3. Loading authority ranker...")

    authority_ranker = AuthorityRanker()

    print("\n4. Applying authority ranking...")

    final_results = authority_ranker.rerank(
        hybrid_results,
        authority_weight=0.10
    )

    print("\n========================================")
    print("FINAL RANKED RESULTS")
    print("========================================")

    for i, result in enumerate(
        final_results,
        start=1
    ):

        print(f"\n--- RESULT {i} ---")

        print(
            f"Final Score: "
            f"{result['final_score']:.6f}"
        )

        print(
            f"RRF Score: "
            f"{result['rrf_score']:.6f}"
        )

        print(
            f"Authority Score: "
            f"{result['authority_score']:.2f}"
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
            f"Citing Cases: "
            f"{result['citing_count']}"
        )

        print(
            f"Cited Cases: "
            f"{result['cited_count']}"
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


if __name__ == "__main__":
    main()