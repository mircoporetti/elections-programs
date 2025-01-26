from fastapi import APIRouter, Depends

from store import vector_store
from ..auth import basic_auth

router = APIRouter(prefix="/api/store", tags=["store"])


@router.post("/clean")
async def answer_question(credentials=Depends(basic_auth)):
    vector_store.clean()
