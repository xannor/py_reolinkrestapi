"""Command Testing Aparatus"""

import json
from typing import Generic, TypeVar

from async_reolink.api.commands import CommandRequest, CommandResponseType


_T = TypeVar("_T", bound=dict[str, tuple[str, str]])


class MockConnection(Generic[_T]):
    """Mocked Connection"""

    JSON: _T

    def __init__(self) -> None:
        self._disconnect_callbacks = []
        super().__init__()

    def _ensure_connection(self) -> bool:
        """mocked ensure connect"""
        return True

    async def _execute2(
        self, *args: CommandRequest
    ) -> list[CommandResponseType]:
        """mocked _execue"""
        _J = type(self).JSON
        assert args[0]["cmd"] in _J
        _J = _J[args[0]["cmd"]]
        _json = json.dumps(args)
        assert _json == _J[0], "unexpected json of `%s`" % _json
        return json.loads(_J[1])
