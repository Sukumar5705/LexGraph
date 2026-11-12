from backend.core.rag_pipeline import RAGPipeline


def main():

    print("=" * 40)
    print("FULL RAG PIPELINE TEST")
    print("=" * 40)

    pipeline = RAGPipeline()

    query = "What is the legal principle under Order VII Rule 11 CPC, and which Supreme Court cases in the retrieved evidence discuss or apply it?"
    result = pipeline.run(
        query=query,
        top_k=10,
        retrieval_k=20,
        reference_date="2024-01-01",
    )

    print("\n========================================")
    print("FINAL ANSWER")
    print("========================================")

    print(result["answer"])

    print("\n========================================")
    print("CITATION VERIFICATION")
    print("========================================")

    citation_report = (
        result["citation_verification"]
    )

    print(
        f"Verified: "
        f"{citation_report['verified']}"
    )

    print(
        f"Mentioned case IDs: "
        f"{citation_report['mentioned_case_ids']}"
    )

    print(
        f"Verified case IDs: "
        f"{citation_report['verified_case_ids']}"
    )

    print(
        f"Unverified case IDs: "
        f"{citation_report['unverified_case_ids']}"
    )

    print("\n========================================")
    print("CONFLICT REPORT")
    print("========================================")

    print(
        f"Conflict detected: "
        f"{result['conflict_report']['conflict_detected']}"
    )

    print(
        f"Conflict count: "
        f"{result['conflict_report']['conflict_count']}"
    )

    # --------------------------------------------------
    # DIAGNOSTIC: SHOW TOP RETRIEVED SOURCE TEXT
    # --------------------------------------------------

    print("\n========================================")
    print("TOP RETRIEVED SOURCE TEXT")
    print("========================================")

    for index, source in enumerate(
        result["sources"][:2],
        start=1,
    ):

        print(
            f"\n--- SOURCE {index} ---"
        )

        print(
            f"Case ID: "
            f"{source.get('case_id')}"
        )

        print(
            f"Title: "
            f"{source.get('title')}"
        )

        print(
            f"Chunk Index: "
            f"{source.get('chunk_index')}"
        )

        print(
            f"Final Score: "
            f"{source.get('final_score', 0.0):.6f}"
        )

        print(
            f"Authority Score: "
            f"{source.get('authority_score', 0.0):.2f}"
        )

        print("\nText:")

        text = source.get(
            "text",
            "",
        )

        print(
            text[:2000]
        )

    # --------------------------------------------------
    # SOURCE SUMMARY
    # --------------------------------------------------

    print("\n========================================")
    print("SOURCE SUMMARY")
    print("========================================")

    for index, source in enumerate(
        result["sources"],
        start=1,
    ):

        print(
            f"\n--- SOURCE {index} ---"
        )

        print(
            f"Case ID: "
            f"{source.get('case_id')}"
        )

        print(
            f"Final Score: "
            f"{source.get('final_score', 0.0):.6f}"
        )

        print(
            f"Authority Score: "
            f"{source.get('authority_score', 0.0):.2f}"
        )

        temporal = source.get(
            "temporal_validation",
            {},
        )

        print(
            f"Temporal Status: "
            f"{temporal.get('status')}"
        )

        print(
            f"Temporally Valid: "
            f"{temporal.get('temporally_valid')}"
        )

        print(
            f"Temporal Reason: "
            f"{temporal.get('reason')}"
        )


if __name__ == "__main__":
    main()