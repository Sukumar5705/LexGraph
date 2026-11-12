from retrieval.reranking.authority_ranker import AuthorityRanker


def main():

    print("========================================")
    print("KNOWLEDGE GRAPH RELATIONSHIP TEST")
    print("========================================")

    ranker = AuthorityRanker()

    graph = ranker.graph_retriever.graph

    print("\nTotal edges:", graph.number_of_edges())

    print("\n========================================")
    print("RELATIONSHIP TYPES")
    print("========================================")

    relationship_counts = {}

    for source, target, data in graph.edges(data=True):

        relationship = data.get(
            "relationship",
            "NO_RELATIONSHIP_FIELD"
        )

        relationship_counts[relationship] = (
            relationship_counts.get(
                relationship,
                0
            ) + 1
        )

    for relationship, count in relationship_counts.items():

        print(
            f"{relationship}: {count}"
        )

    print("\n========================================")
    print("SAMPLE EDGES")
    print("========================================")

    count = 0

    for source, target, data in graph.edges(
        data=True
    ):

        print("\nSource:", source)
        print("Target:", target)
        print("Relationship:", data)

        count += 1

        if count >= 20:
            break

    print("\n========================================")
    print("CHECKING CASE 2023 INSC 527")
    print("========================================")

    case_id = "2023 INSC 527"

    node_id = (
        ranker.graph_retriever.get_case_node(
            case_id
        )
    )

    print(
        "\nCase node:",
        node_id
    )

    if node_id is not None:

        print("\nOUTGOING EDGES:")

        for source, target, data in graph.out_edges(
            node_id,
            data=True
        ):

            print(
                "Target:",
                target,
                "| Data:",
                data
            )

        print("\nINCOMING EDGES:")

        for source, target, data in graph.in_edges(
            node_id,
            data=True
        ):

            print(
                "Source:",
                source,
                "| Data:",
                data
            )


if __name__ == "__main__":
    main()