import os

from store.vector_store import similarity_search
from langchain_huggingface import HuggingFaceEndpoint
from langchain.chains import RetrievalQA

from store import vector_store

huggingface_token = os.getenv("HUGGINGFACEHUB_API_TOKEN")
if not huggingface_token:
    raise ValueError("HUGGINGFACEHUB_API_TOKEN environment variable is not set.")

generative_model = HuggingFaceEndpoint(repo_id="mistralai/Mixtral-8x7B-Instruct-v0.1", temperature=0.7)


def answer(question: str):
    qa_chain = RetrievalQA.from_chain_type(
        llm=generative_model,
        chain_type="stuff",
        retriever=vector_store.get_store_as_retriever()
    )

    return qa_chain.invoke(question)["result"]


def answer_with_most_pertinent_chunks(query: str):
    best_chunks = similarity_search(query)

    print(best_chunks)

    return best_chunks
