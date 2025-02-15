from fastapi.responses import JSONResponse
from fastapi import Request

from chat.party import PartyNotFoundError
from .api.middleware import DailyLimitExceededException


async def party_not_found_exception_handler(request: Request, e: PartyNotFoundError) -> JSONResponse:
    return JSONResponse(
        status_code=404,
        content={"detail": str(e)}
    )


def daily_limit_exception_handler(request: Request, e: DailyLimitExceededException):
    return JSONResponse(
        status_code=429,
        content={"detail": e.detail},
    )
