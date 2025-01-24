from fastapi import FastAPI
from pydantic import BaseModel

from chat.ai_assistant import answer

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


class QueryRequest(BaseModel):
    query: str


@app.post("/api/programs/chat")
async def ask_about_parties_manifest(request: QueryRequest):
    chunks = answer(request.query)
    return {"chunks": chunks}
