import os
from typing import List, Dict
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langchain_aws import ChatBedrock
from chat.party import Party
from store import vector_store
from store.vector_store import similarity_search_for

aws_access_key_id = os.getenv("AWS_ACCESS_KEY_ID")
aws_secret_access_key = os.getenv("AWS_SECRET_ACCESS_KEY")
if not aws_access_key_id or not aws_secret_access_key:
    raise ValueError("AWS ACCESS KEYS environment variables are not set.")

system_prompt = (
    "You are a concise AI assistant, expert in politics. "
    "Respond in plain text using a maximum of three concise sentences. "
    "Use the provided context to answer the question accurately. "
    "If you are unsure about the answer, say you don't know. "
    "Party: {party}. "
    "Context: {context}"
)


llm = ChatBedrock(model_id='mistral.mistral-7b-instruct-v0:2', region_name='us-west-2', aws_access_key_id=aws_access_key_id,
                  aws_secret_access_key=aws_secret_access_key)


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
