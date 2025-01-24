from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings


def store_docs_as_vectors(docs_chunks):
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

    vector_store = FAISS.from_documents(docs_chunks, embeddings)
    vector_store.save_local("faiss")
    return vector_store


def similarity_search(query, vector_store):
    return vector_store.similarity_search_with_score(query, 5)
