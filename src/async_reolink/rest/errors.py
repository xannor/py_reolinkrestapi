"""REST common errors"""

from typing import Final

from asyncio import TimeoutError as AsyncIOTimeoutError
from aiohttp import ClientConnectionError, ClientResponseError


CONNECTION_ERRORS: Final = (
    TimeoutError,
    AsyncIOTimeoutError,
    ClientConnectionError,
    ConnectionRefusedError
)

RESPONSE_ERRORS: Final = (
    ClientResponseError
)
