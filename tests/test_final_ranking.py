from retrieval.hybrid.hybrid_retriever import HybridRetriever
from retrieval.reranking.cross_encoder import CrossEncoderReranker
from retrieval.reranking.authority_ranker import AuthorityRanker


def main():

    query = "Eldeco Housing and Industries Limited Ashok Vidyarthi Geetha Nanjundaswamy" 

    print("========================================")
    print("FINAL RANKING PIPELINE TEST")
    print("========================================")

    # ---------------------------------------------
    # 1. Hybrid retrieval
    # ---------------------------------------------

    print("\n1. Loading hybrid retriever...")

    hybrid = HybridRetriever()

    print("\nRunning hybrid retrieval...")

    hybrid_results = hybrid.query(
        query,
        top_k=10,
        retrieval_k=20
    )

    print(
        f"Hybrid candidates: "
        f"{len(hybrid_results)}"
    )

    # ---------------------------------------------
    # 2. Cross-encoder reranking
    # ---------------------------------------------

    print("\n2. Loading cross-encoder...")

    cross_encoder = CrossEncoderReranker()

    print("\nRunning cross-encoder...")

    cross_results = cross_encoder.rerank(
        query,
        hybrid_results,
        top_k=10
    )

    # ---------------------------------------------
    # 3. Authority ranking
    # ---------------------------------------------

    print("\n3. Loading authority ranker...")

    authority_ranker = AuthorityRanker()

    print("\nApplying authority + relevance ranking...")

    final_results = authority_ranker.rerank(
        cross_results,
        authority_weight=0.10,
        cross_encoder_weight=0.30
    )

    # ---------------------------------------------
    # 4. Final results
    # ---------------------------------------------

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
            f"Cross-Encoder Score: "
            f"{result['cross_encoder_score']:.6f}"
        )

        print(
            f"Normalized Cross Score: "
            f"{result['normalized_cross_encoder_score']:.6f}"
        )

        print(
            f"Authority Score: "
            f"{result['authority_score']:.2f}"
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