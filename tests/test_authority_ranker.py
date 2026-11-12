from retrieval.reranking.authority_ranker import AuthorityRanker


def main():

    print("========================================")
    print("AUTHORITY SCORE TEST")
    print("========================================")

    ranker = AuthorityRanker()

    # These cases are known to have citation
    # relationships in the current graph.
    test_cases = [
        "2023 INSC 1043",
        "2023 INSC 964",
        "2023 INSC 803",
        "2023 INSC 749",
        "2023 INSC 920",
        "2023 INSC 783",
        "2023 INSC 784",
        "2023 INSC 761",
        "2023 INSC 660",
        "2023 INSC 1081",
        "2023 INSC 870",
    ]

    for case_id in test_cases:

        print("\n----------------------------------------")
        print(f"CASE: {case_id}")
        print("----------------------------------------")

        result = ranker.calculate_authority_score(
            case_id
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


if __name__ == "__main__":
    main()