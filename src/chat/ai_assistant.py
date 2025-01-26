import os

from chat.party import Party, PartyNotFoundError
from store.vector_store import similarity_search_for
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
        retriever=vector_store.get_store_as_retriever_for(extract_party_from(question))
    )

    return qa_chain.invoke(question)["result"]


def answer_with_most_pertinent_chunks(question: str):
    best_chunks = similarity_search_for(extract_party_from(question), question)

    return best_chunks


def extract_party_from(question):
    for party in Party:
        if party.value.lower() in question.lower():
            return party
    raise PartyNotFoundError(question)
