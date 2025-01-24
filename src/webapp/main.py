from fastapi import FastAPI
from pydantic import BaseModel

from chat.ai_assistant import answer
from store import vector_store

app = FastAPI()


@app.on_event("startup")
async def load_resources():
    vector_store.init_vector_store()


@app.get("/")
async def root():
    return {"message": "Hello World"}


class QueryRequest(BaseModel):
    query: str


@app.post("/api/programs/chat")
async def ask_about_parties_manifest(request: QueryRequest):
    chunks = answer(request.query)
    return {"chunks": chunks}
