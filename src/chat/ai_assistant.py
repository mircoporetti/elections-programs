from store.vector_store import similarity_search


def answer(query: str):
    best_chunks = similarity_search(query)

    print(best_chunks)

    return best_chunks
