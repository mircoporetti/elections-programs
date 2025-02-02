from typing import List

from fastapi import APIRouter, Depends
from pydantic import BaseModel

from chat import ai_assistant
from ..auth import basic_auth

router = APIRouter(prefix="/api/chat", tags=["chat"])


class Question(BaseModel):
    history: List
    query: str

@router.post("/completion")
async def answer_question(prompt: Question, credentials=Depends(basic_auth)):
    result = ai_assistant.answer(prompt.query, prompt.history)
    return {"answer": result}


@router.post("/retrieve")
async def retrieve_most_pertinent_chunks(prompt: Question, credentials=Depends(basic_auth)):
    result = ai_assistant.answer_with_most_pertinent_chunks(prompt.query)
    return {"chunks": result}
