import os
import re
from typing import List, Dict

from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import AIMessage, HumanMessage
from langchain_huggingface import HuggingFaceEndpoint

from chat.party import Party
from store import vector_store
from store.vector_store import similarity_search_for


huggingface_token = os.getenv("HUGGINGFACEHUB_API_TOKEN")
if not huggingface_token:
    raise ValueError("HUGGINGFACEHUB_API_TOKEN environment variable is not set.")

system_prompt = (
    "You are a concise AI assistant, expert in politics. "
    "Respond in plain text without repeating the same sentence or adding labels like 'AI:', 'Assistant:', or 'Human: "
    "Use the given context to answer the question. "
    "If you are unsure about the answer, say you don't know. "
    "Limit your response to max three concise sentences. "
    "The party object of the question is: {party}. "
    "Context: {context}"
)


generative_model = HuggingFaceEndpoint(repo_id="mistralai/Mistral-7B-Instruct-v0.3", temperature=0.7)


def answer(question: str, history: List[Dict[str, str]]):
    recent_history = [
        AIMessage(content=msg["content"]) if msg["role"].lower() == "ai" else HumanMessage(content=msg["content"])
        for msg in history[-4:]
    ]

    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        MessagesPlaceholder(variable_name="chat_history"),
        ("human", "{input}"),
    ])
    party = Party.get_from_history(history)

    question_answer_chain = create_stuff_documents_chain(generative_model, prompt)
    retriever = vector_store.get_store_as_retriever_for(party)
    chain = create_retrieval_chain(retriever, question_answer_chain)

    response = chain.invoke({"input": question, "party": party.name, "chat_history": recent_history})
    llm_answer = response["answer"].strip()
    return re.sub(r'(AI|Assistant|Bot|System|Human|):\s*', '', llm_answer, flags=re.IGNORECASE)


def answer_with_most_pertinent_chunks(question: str):
    best_chunks = similarity_search_for(Party.get_from_message(question), question)

    return best_chunks


