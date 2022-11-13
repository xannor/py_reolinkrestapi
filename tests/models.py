""""Models"""

from abc import ABC, abstractmethod
import logging
from typing import AsyncIterable, TypedDict

from async_reolink.api.connection.mixin import Connection
from async_reolink.api.connection.model import Request, Response


class MockConnectionValues(TypedDict):

    is_connected: bool
    connection_id: int
    hostname: str


_MOCK_DEFAULTS: MockConnectionValues = {
    "connection_id": 1,
    "hostname": "Mock Host",
    "is_connected": True,
}


class MockConnection(Connection, ABC):
    """Mocked Connection"""

    def __init__(self, *args, logger: logging.Logger = None, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self._mocked: MockConnectionValues = {}.update(_MOCK_DEFAULTS)
        self._logger = logger

    @property
    def is_connected(self) -> bool:
        return self._mocked["is_connected"]

    @property
    def connection_id(self) -> int:
        return self._mocked["connection_id"]

    @property
    def hostname(self):
        return self._mocked["hostname"]

    async def connect(self, hostname: str, port: int = None, timeout: float = ...):
        if self._logger is not None:
            self._logger.info("connect fired")
        return

    async def disconnect(self):
        if self._logger is not None:
            self._logger.info("disconnect fired")
        return


class MockConnection_SingleExecute(MockConnection, ABC):
    """Mocked Single execute response"""

    @abstractmethod
    async def _mocked_execute(self, request: Request) -> Response | bytes:
        ...

    def _execute(self, *args: Request) -> AsyncIterable[Response | bytes]:
        if self._logger is not None:
            self._logger.info("_execute fired")

        async def _mock_iterable():
            for request in args:
                yield await self._mocked_execute(request)

        return _mock_iterable()
