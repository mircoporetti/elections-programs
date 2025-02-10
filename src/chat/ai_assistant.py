import os
from typing import List, Dict
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langchain_huggingface import ChatHuggingFace
from langchain_huggingface import HuggingFaceEndpoint
from chat.party import Party
from store import vector_store
from store.vector_store import similarity_search_for


huggingface_token = os.getenv("HUGGINGFACEHUB_API_TOKEN")
if not huggingface_token:
    raise ValueError("HUGGINGFACEHUB_API_TOKEN environment variable is not set.")

system_prompt = (
    "Du bist ein präziser KI-Assistent, spezialisiert auf Politik. "
    "Antworte in Klartext mit maximal drei knappen Sätzen. "
    "Nutze den gegebenen Kontext, um die Frage genau zu beantworten. "
    "Falls du die Antwort nicht kennst, sage, dass du es nicht weißt. "
    "Beantworte diese Frage auf Deutsch. "
    "Partei: {party}. "
    "Kontext: {context}"
)

llm_endpoint = HuggingFaceEndpoint(
    repo_id="mistralai/Mixtral-8x7B-Instruct-v0.1",
    temperature=0.7,
    max_new_tokens=256,
    stop_sequences=["</s>", "Human:", "AI:"],
)
llm = ChatHuggingFace(llm=llm_endpoint)


def answer(question: str, history: List[Dict[str, str]]):
    party = Party.get_from_history(history)
    retriever = vector_store.get_store_as_retriever_for(party)
    context_docs = retriever.invoke(question)
    context = "\n".join([doc.page_content for doc in context_docs])

    conversation = [SystemMessage(content=system_prompt.format(context=context, party=party.name))]
    for message in history[-5:]:
        if message["role"].lower() != "ai":
            conversation.append(HumanMessage(content=message["content"]))
        else:
            conversation.append(AIMessage(content=message["content"]))

    return llm.invoke(conversation).content


def answer_with_most_pertinent_chunks(question: str):
    best_chunks = similarity_search_for(Party.get_from_message(question), question)

    return best_chunks
