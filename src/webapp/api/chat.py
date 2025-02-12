from typing import List

from fastapi import APIRouter, Depends
from pydantic import BaseModel

from chat import ai_assistant
from ..auth import basic_auth

from src.webapp.config import Config
from lingua import Language, LanguageDetectorBuilder

router = APIRouter(prefix="/api/chat", tags=["chat"])

languages = [Language.ENGLISH, Language.GERMAN]
detector = LanguageDetectorBuilder.from_languages(*languages).build()


class CompletionRequest(BaseModel):
    history: List
    question: str


class ChunksRetrievalRequest(BaseModel):
    question: str

@router.post("/completion")
async def answer_question(request: CompletionRequest, credentials=Depends(basic_auth)):
    language = detector.detect_language_of(request.question)
    Config.user_lang = language

    result = ai_assistant.answer(request.question, request.history, language)
    return {"answer": result}


@router.post("/retrieve")
async def retrieve_most_pertinent_chunks(request: ChunksRetrievalRequest, credentials=Depends(basic_auth)):
    result = ai_assistant.answer_with_most_pertinent_chunks(request.question)
    return {"chunks": result}
