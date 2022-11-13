""""REST Connection Typings"""


from enum import IntEnum
from ssl import SSLContext
from typing import Callable, Literal, Protocol, Sequence

import aiohttp

from async_reolink.api.connection.model import Request


class Encryption(IntEnum):
    """Connection Encryption"""

    NONE = 0
    HTTPS = 1


class SSLContextFactory(Protocol):
    """
    SSL Context Factory

    Return False for no verify SSL or None for default SSL
    otherwise return a Fignerprint or full SSLContext
    """

    def __call__(self, base_url: str) -> Literal[False] | aiohttp.Fingerprint | SSLContext:
        ...


class SessionFactory(Protocol):
    """Session Factory"""

    def __call__(
        self, base_url: str, timeout: int, ssl: SSLContextFactory | None = None
    ) -> aiohttp.ClientSession:
        ...


class WithConnection(Protocol):
    """Connection Part"""

    _force_get_callbacks: list[Callable[[str, dict[str, str], Sequence[Request]], any]]
