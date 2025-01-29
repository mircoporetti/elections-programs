import shutil

from filelock import FileLock
import logging
import os

from langchain_community.vectorstores import FAISS, VectorStore
from langchain_community.document_loaders import PyPDFLoader
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

from chat.party import Party

logger = logging.getLogger("uvicorn")

PROGRAMS_PATH = "resources/manifests/"
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

faiss_vector_indexes = {}


def faiss_folder_is_empty_except_lockfile():
    return os.path.exists("faiss") and not any(file for file in os.listdir("faiss") if file not in "init.lock")


def init():
    global faiss_vector_indexes
    lock = FileLock("./faiss/init.lock", timeout=120)
    with (lock):
        logger.info("Initializing Vector Store...")
        if faiss_folder_is_empty_except_lockfile():
            logger.info("Creating new Vector Store from parties' programs docs...")
            for doc in os.listdir(f"./{PROGRAMS_PATH}"):
                party_name = os.path.splitext(doc)[0]
                logger.info(f"Creating FAISS index for party: {party_name}")
                loader = PyPDFLoader(f"./{PROGRAMS_PATH}/{doc}")
                pages_to_be_chunked = loader.load()
                splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
                chunks = splitter.split_documents(pages_to_be_chunked)
                logger.info(f"Chunks: {len(chunks)}")
                store = FAISS.from_documents(chunks, embeddings)
                store.save_local(f"faiss/{party_name}")
                faiss_vector_indexes[party_name] = store
        else:
            logger.info("Loading existing Vector Store indexes...")
            for party_store_dir in os.listdir("./faiss"):
                if "." not in party_store_dir:
                    party_name = party_store_dir
                    logger.info(f"Loading FAISS index for party: {party_name}")
                    faiss_vector_indexes[party_name] = FAISS.load_local(
                        f"faiss/{party_name}", embeddings,
                        allow_dangerous_deserialization=True)
            logger.info("Vector Store has been initialized.")


def clean():
    lock = FileLock("./faiss/init.lock", timeout=120)
    with lock:
        logger.info("Cleaning up Vector Store...")
        for filename in os.listdir('faiss'):
            file_path = os.path.join('faiss', filename)
            if os.path.isdir(file_path):
                shutil.rmtree(file_path)
            elif os.path.isfile(file_path):
                os.remove(file_path)
        logger.info("Vector Store cleanup successful.")


def get_store_as_retriever_for(party: Party):
    return faiss_vector_indexes[party.name].as_retriever(search_type="similarity",
                                                         search_kwargs={"k": 3})


def similarity_search_for(party: Party, query: str):
    store: VectorStore = faiss_vector_indexes[party.name]
    most_similar_results = store.similarity_search_with_score(query, k=4)
    print(most_similar_results)
    return [
        {
            "text": result[0],
            "score": float(result[1])
        }
        for result in most_similar_results
    ]
