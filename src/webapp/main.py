from fastapi import FastAPI, Depends
from store import vector_store
from .auth import security
from .routers.chat import router as chat_router

app = FastAPI(dependencies=[Depends(security)])
app.include_router(chat_router)


@app.on_event("startup")
async def load_resources():
    vector_store.init()
