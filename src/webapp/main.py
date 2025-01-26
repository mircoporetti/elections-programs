import logging

from fastapi import FastAPI, Depends
from pydantic import BaseModel

from chat import ai_assistant
from store import vector_store
from .auth import security, basic_auth

app = FastAPI(dependencies=[Depends(security)])

logger = logging.getLogger("uvicorn")


@app.on_event("startup")
async def load_resources():
    vector_store.init_vector_store()


class Prompt(BaseModel):
    query: str


@app.post("/api/chat/completion")
async def answer_question(prompt: Prompt, credentials=Depends(basic_auth)):
    result = ai_assistant.answer(prompt.query)
    return {"answer": result}


@app.post("/api/chat/retrieve")
async def retrieve_most_pertinent(prompt: Prompt, credentials=Depends(basic_auth)):
    result = ai_assistant.answer_with_most_pertinent_chunks(prompt.query)
    return {"chunks": result}
