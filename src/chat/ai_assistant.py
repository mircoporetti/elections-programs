import os

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
    "Provide direct answers without prefixes like 'AI:', 'Assistant:', or translations."
    "Respond in plain text, with no extra formatting."
    "Use the given context to answer the question."
    "If you are unsure about the answer, say you don't know."
    "Limit your response to three sentences."
    "Context: {context}"
)
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system_prompt),
        ("human", "{input}"),
    ]
)

generative_model = HuggingFaceEndpoint(repo_id="mistralai/Mixtral-8x7B-Instruct-v0.1", temperature=0.7)


def answer(question: str):
    question_answer_chain = create_stuff_documents_chain(generative_model, prompt)
    retriever = vector_store.get_store_as_retriever_for(Party.get_from(question))
    chain = create_retrieval_chain(retriever, question_answer_chain)

    return chain.invoke({"input": question})["answer"].strip()


def answer_with_most_pertinent_chunks(question: str):
    best_chunks = similarity_search_for(Party.get_from(question), question)

    return best_chunks

