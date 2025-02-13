from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware

from chat.party import PartyNotFoundError
from store import vector_store
from .auth import security
from .exception_handlers import party_not_found_exception_handler
from .api.chat import router as chat_router
from .api.store import router as store_router


app = FastAPI(dependencies=[Depends(security)])

allowed_origins = [
    "http://localhost:3000",
    "https://elections.mircoporetti.me",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(chat_router)
app.include_router(store_router)
app.add_exception_handler(PartyNotFoundError, party_not_found_exception_handler)


@app.on_event("startup")
async def load_resources():
    vector_store.init()
