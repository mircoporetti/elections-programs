from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

from store.vectore_store import store_docs_as_vectors, similarity_search

PROGRAMS_PATH = "./resources/manifests/"


def answer(query: str):
    docs_chunks = chunk_manifests_pdfs()
    vector_store = store_docs_as_vectors(docs_chunks)
    results = similarity_search(query, vector_store)

    print(results)

    return docs_chunks


def chunk_manifests_pdfs():
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    loader = PyPDFDirectoryLoader(PROGRAMS_PATH)
    docs_to_be_chunked = loader.load()
    return splitter.split_documents(docs_to_be_chunked)