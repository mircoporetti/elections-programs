import os
import re
from typing import List, Dict

from chat.party import Party
from store.vector_store import similarity_search_for
from langchain_huggingface import HuggingFaceEndpoint
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import AIMessage, HumanMessage

from store import vector_store

huggingface_token = os.getenv("HUGGINGFACEHUB_API_TOKEN")
if not huggingface_token:
    raise ValueError("HUGGINGFACEHUB_API_TOKEN environment variable is not set.")

system_prompt = (
    "You are a concise AI assistant, expert in politics. "
    "Respond in plain text with no formatting. "
    "Use this context: {context} "
    "If the context is empty, try to understand based on the old messages. "
    "If unsure, say you don't know. Keep responses to max 3 sentences."
)

prompt_template = ChatPromptTemplate.from_messages([
    ("system", system_prompt),
    MessagesPlaceholder("chat_history"),
    ("human", "{input}"),
])

generative_model = HuggingFaceEndpoint(repo_id="mistralai/Mixtral-8x7B-Instruct-v0.1", temperature=0.7)


def answer(question: str, history: List[Dict[str, str]]):
    converted_history = []
    for msg in history:
        if msg["role"] == "AI":
            converted_history.append(AIMessage(content=msg["content"]))
        else:
            converted_history.append(HumanMessage(content=msg["content"]))

    recent_history = converted_history[-2:]

    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        *recent_history,
        ("human", question),
    ])
    party = Party.get_from_history(history)
    question_answer_chain = create_stuff_documents_chain(generative_model, prompt)
    retriever = vector_store.get_store_as_retriever_for(party)
    chain = create_retrieval_chain(retriever, question_answer_chain)

    response = chain.invoke({"input": question, "party": party.name})
    llm_answer = response["answer"].strip()
    return re.sub(r'^(AI|Assistant|Bot|System):\s*', '', llm_answer, flags=re.IGNORECASE)


def answer_with_most_pertinent_chunks(question: str):
    best_chunks = similarity_search_for(Party.get_from_message(question), question)

    return best_chunks

