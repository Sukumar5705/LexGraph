from retrieval.vector.embedding_model import EmbeddingModel
from retrieval.vector.vector_store import VectorStore


def main():

    query = "right to be heard under the Forest Act and reserved forest"

    print("========================================")
    print("VECTOR RETRIEVAL TEST")
    print("========================================")

    print("\nLoading embedding model...")
    embedding_model = EmbeddingModel()

    print("\nCreating query embedding...")
    query_vector = embedding_model.embed_one(query)

    print(
        f"Embedding dimension: {len(query_vector)}"
    )

    print("\nLoading vector store...")
    vector_store = VectorStore()

    print("\nSearching FAISS...")
    results = vector_store.query(
        query_vector,
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