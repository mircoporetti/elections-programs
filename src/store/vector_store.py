import os

from langchain_community.vectorstores import FAISS, VectorStore
from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

PROGRAMS_PATH = "./resources/manifests/"
vector_store: VectorStore
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")


def init_vector_store():
    global vector_store
    if os.path.exists("faiss") and os.listdir("faiss"):
        vector_store = FAISS.load_local("faiss", embeddings, allow_dangerous_deserialization=True)
    docs_chunks = chunk_manifests_pdfs()
    vector_store = build_from_documents(docs_chunks)


def build_from_documents(docs_chunks):
    store = FAISS.from_documents(docs_chunks, embeddings)
    store.save_local("faiss")
    return store


def similarity_search(query):
    print(vector_store)
    most_similar_results = vector_store.similarity_search_with_score(query, 4)
    return [
        {
            "text": result[0],
            "score": float(result[1])
        }
        for result in most_similar_results
    ]


def chunk_manifests_pdfs():
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    loader = PyPDFDirectoryLoader(PROGRAMS_PATH)
    docs_to_be_chunked = loader.load()
    return splitter.split_documents(docs_to_be_chunked)

