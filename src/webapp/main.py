import logging

from fastapi import FastAPI
from pydantic import BaseModel
from completion import ai_assistant
from store import vector_store

app = FastAPI()

logger = logging.getLogger("uvicorn")


@app.on_event("startup")
async def load_resources():
    logger.info("Initializing Vector Store...")
    vector_store.init_vector_store()
    logger.info("Vector Store has been initialized.")


class Prompt(BaseModel):
    query: str


@app.post("/api/chat/completion")
async def answer_question(prompt: Prompt):
    result = ai_assistant.answer(prompt.query)
    return {"answer": result}


@app.post("/api/chat/retrieve")
async def retrieve_most_pertinent(prompt: Prompt):
    result = ai_assistant.answer_with_most_pertinent_chunks(prompt.query)
    return {"chunks": result}
