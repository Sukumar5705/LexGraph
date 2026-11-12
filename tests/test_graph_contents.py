from retrieval.reranking.authority_ranker import AuthorityRanker


def main():

    print("========================================")
    print("KNOWLEDGE GRAPH CONTENT TEST")
    print("========================================")

    ranker = AuthorityRanker()

    graph = ranker.graph_retriever.graph

    print("\nTotal nodes:", graph.number_of_nodes())
    print("Total edges:", graph.number_of_edges())

    print("\n========================================")
    print("NODE TYPE COUNTS")
    print("========================================")

    node_type_counts = {}

    for node_id, data in graph.nodes(data=True):

        node_type = data.get("node_type", "UNKNOWN")

        node_type_counts[node_type] = (
            node_type_counts.get(node_type, 0) + 1
        )

    for node_type, count in node_type_counts.items():

        print(
            f"{node_type}: {count}"
        )

    print("\n========================================")
    print("SAMPLE CASE NODES")
    print("========================================")

    count = 0

    for node_id, data in graph.nodes(data=True):

        if data.get("node_type") == "case":

            print("\nNode ID:", node_id)
            print("Case ID:", data.get("case_id"))
            print("Title:", data.get("title"))
            print("Citation:", data.get("citation"))

            count += 1

            if count >= 10:
                break

    print("\n========================================")
    print("CHECKING OUR TEST CASES")
    print("========================================")

    test_cases = [
        "2023 INSC 527",
        "2023 INSC 303",
        "2023 INSC 154",
        "2023 INSC 618",
        "2023 INSC 324",
        "2023 INSC 975",
        "2023 INSC 42",
        "2023 INSC 809",
        "2023 INSC 868",
    ]

    for case_id in test_cases:

        node_id = (
            ranker.graph_retriever.get_case_node(
                case_id
            )
        )

        print(
            f"{case_id} -> {node_id}"
        )


if __name__ == "__main__":
    main()