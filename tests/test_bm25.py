from retrieval.bm25.bm25_retriever import BM25Retriever


def main():

    query = "right to be heard under the Forest Act and reserved forest"

    print("========================================")
    print("BM25 RETRIEVAL TEST")
    print("========================================")

    print("\nLoading BM25 retriever...")
    retriever = BM25Retriever()

    print("\nSearching BM25...")

    results = retriever.query(
        query,
        top_k=5
    )

    print("\n========================================")
    print("TOP RESULTS")
    print("========================================")

    for i, result in enumerate(
        results,
        start=1
    ):

        print(f"\n--- RESULT {i} ---")

        print(
            f"Score: {result['score']:.4f}"
        )

        print(
            f"Case ID: {result['case_id']}"
        )

        print(
            f"Title: {result['title']}"
        )

        print(
            f"Chunk index: {result['chunk_index']}"
        )

        print(
            f"Citation: {result['citation']}"
        )


if __name__ == "__main__":
    main()