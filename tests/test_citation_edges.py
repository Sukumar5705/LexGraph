from retrieval.reranking.authority_ranker import AuthorityRanker


def main():

    print("========================================")
    print("CITATION EDGE TEST")
    print("========================================")

    ranker = AuthorityRanker()

    graph = ranker.graph_retriever.graph

    print("\n========================================")
    print("ALL CITATION EDGES")
    print("========================================")

    citation_count = 0

    for source, target, data in graph.edges(
        data=True
    ):

        if data.get("relationship") != "cites":
            continue

        source_data = graph.nodes[source]
        target_data = graph.nodes[target]

        print("\n----------------------------------------")

        print(
            f"Source Case ID: "
            f"{source_data.get('case_id')}"
        )

        print(
            f"Source Title: "
            f"{source_data.get('title')}"
        )

        print(
            f"Target Case ID: "
            f"{target_data.get('case_id')}"
        )

        print(
            f"Target Title: "
            f"{target_data.get('title')}"
        )

        print(
            f"Relationship: "
            f"{data.get('relationship')}"
        )

        print(
            f"Confidence: "
            f"{data.get('confidence')}"
        )

        citation_count += 1

    print("\n========================================")
    print(
        f"TOTAL CITATION EDGES: {citation_count}"
    )
    print("========================================")


if __name__ == "__main__":
    main()