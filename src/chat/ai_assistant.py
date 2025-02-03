import os
import re
from typing import List, Dict

from chat.party import Party
from store.vector_store import similarity_search_for
from langchain_huggingface import HuggingFaceEndpoint
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.prompts import ChatPromptTemplate

from store import vector_store

huggingface_token = os.getenv("HUGGINGFACEHUB_API_TOKEN")
if not huggingface_token:
    raise ValueError("HUGGINGFACEHUB_API_TOKEN environment variable is not set.")

system_prompt = (
    "You are a concise AI assistant, expert in politics."
    "Respond in plain text without repeating the same sentence."
    "Use the given context to answer the question."
    "If you are unsure about the answer, say you don't know."
    "Limit your response to max three concise sentences."
    "The party object of the question is: {party}."
    "Context: {context}"
)
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system_prompt),
        ("human", "{input}"),
    ]
)

generative_model = HuggingFaceEndpoint(repo_id="mistralai/Mistral-7B-Instruct-v0.3", temperature=0.7)


def answer(question: str, history: List[Dict[str, str]]):
    question_answer_chain = create_stuff_documents_chain(generative_model, prompt)
    party = Party.get_from_history(history)
    retriever = vector_store.get_store_as_retriever_for(party)
    chain = create_retrieval_chain(retriever, question_answer_chain)

    llm_answer = chain.invoke({"input": question, "party": party})["answer"].strip()
    return re.sub(r'(AI|Assistant|Bot|System|Answer):\s*', '', llm_answer, flags=re.IGNORECASE)


def answer_with_most_pertinent_chunks(question: str):
    best_chunks = similarity_search_for(Party.get_from_message(question), question)

    return best_chunks
