from knowledge_graph.graph_retriever import GraphRetriever


def main():

    print("========================================")
    print("GRAPH RETRIEVER TEST")
    print("========================================")

    graph = GraphRetriever()

    # --------------------------------------------------
    # TEST CASES
    # --------------------------------------------------

    test_cases = [
        "2023 INSC 1043",   # Eldeco Housing
        "2023 INSC 964",    # Kum. Geetha
        "2023 INSC 350",
        "2023 INSC 539",
        "2023 INSC 999",    # Non-existing case for negative test
    ]

    for case_id in test_cases:

        print("\n----------------------------------------")
        print(f"CASE: {case_id}")
        print("----------------------------------------")

        result = graph.expand_case(case_id)

        # --------------------------------------------------
        # JUDGE
        # --------------------------------------------------

        print(
            f"Judge: {result['judge']}"
        )

        # --------------------------------------------------
        # COURT
        # --------------------------------------------------

        print(
            f"Court: {result['court']}"
        )

        # --------------------------------------------------
        # CITED CASES
        # --------------------------------------------------

        print(
            f"Cited cases: "
            f"{len(result['cited_cases'])}"
        )

        for case in result["cited_cases"]:

            print(
                f"  → {case['case_id']} | "
                f"{case['title']}"
            )

        # --------------------------------------------------
        # CITING CASES
        # --------------------------------------------------

        print(
            f"Citing cases: "
            f"{len(result['citing_cases'])}"
        )

        for case in result["citing_cases"]:

            print(
                f"  ← {case['case_id']} | "
                f"{case['title']}"
            )

    print("\n========================================")
    print("TEST COMPLETE")
    print("========================================")


if __name__ == "__main__":
    main()