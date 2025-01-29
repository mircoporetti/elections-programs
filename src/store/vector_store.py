from filelock import FileLock
import logging
import os

from langchain_community.vectorstores import FAISS, VectorStore
from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

from chat.party import Party

logger = logging.getLogger("uvicorn")

PROGRAMS_PATH = "resources/manifests/"
vector_store: VectorStore
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")


def faiss_folder_is_empty_except_lockfile():
    return os.path.exists("faiss") and not any(file for file in os.listdir("faiss") if file not in "init.lock")


def init():
    global vector_store
    lock = FileLock("./faiss/init.lock", timeout=120)
    with lock:
        logger.info("Initializing Vector Store...")
        if faiss_folder_is_empty_except_lockfile():
            logger.info("Creating new Vector Store from parties' programs docs...")
            docs_chunks = chunk_manifests_pdfs()
            vector_store = build_from_documents(docs_chunks)
        else:
            logger.info("Loading existing Vector Store...")
            vector_store = FAISS.load_local("faiss", embeddings, allow_dangerous_deserialization=True)
        logger.info("Vector Store has been initialized.")


def build_from_documents(docs_chunks):
    store = FAISS.from_documents(docs_chunks, embeddings)
    store.save_local("faiss")
    return store


def chunk_manifests_pdfs():
    splitter = RecursiveCharacterTextSplitter(chunk_size=2200, chunk_overlap=200)
    loader = PyPDFDirectoryLoader(f"./{PROGRAMS_PATH}")
    docs_to_be_chunked = loader.load()
    return splitter.split_documents(docs_to_be_chunked)


def clean():
    lock = FileLock("./faiss/init.lock", timeout=120)
    with lock:
        if faiss_folder_is_empty_except_lockfile():
            logger.info("Nothing to clean...")
        else:
            logger.info("Cleaning up Vector Store...")
            for filename in os.listdir("faiss"):
                file_path = os.path.join("faiss", filename)
                if os.path.isfile(file_path):
                    os.remove(file_path)
        logger.info("Vector Store cleanup successful.")


def get_store_as_retriever_for(party: Party):
    party_filter = {"source": f"{PROGRAMS_PATH}{party.name}.pdf"}
    return vector_store.as_retriever(search_type="similarity", search_kwargs={"k": 4, "filter": party_filter})


def similarity_search_for(party: Party, query: str):
    party_filter = {"source": f"{PROGRAMS_PATH}{party.name}.pdf"}
    most_similar_results = vector_store.similarity_search_with_score(query, k=4, filter=party_filter)
    return [
        {
            "text": result[0],
            "score": float(result[1])
        }
        for result in most_similar_results
    ]
