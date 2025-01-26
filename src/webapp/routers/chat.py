from fastapi import APIRouter, Depends
from pydantic import BaseModel

from chat import ai_assistant
from ..auth import basic_auth

router = APIRouter(prefix="/api/chat", tags=["chat"])


class Prompt(BaseModel):
    query: str


@router.post("/completion")
async def answer_question(prompt: Prompt, credentials=Depends(basic_auth)):
    result = ai_assistant.answer(prompt.query)
    return {"answer": result}


@router.post("/retrieve")
async def retrieve_most_pertinent(prompt: Prompt, credentials=Depends(basic_auth)):
    result = ai_assistant.answer_with_most_pertinent_chunks(prompt.query)
    return {"chunks": result}
