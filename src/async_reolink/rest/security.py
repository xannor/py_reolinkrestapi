"""REST Security"""

from __future__ import annotations
from typing import Sequence

from async_reolink.api.commands import CommandRequest

from async_reolink.api.security import Security as BaseSecurity, LoginCommand
from . import connection


class Security(BaseSecurity):
    """REST security mixin"""

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        if isinstance(self, connection.Connection):
            self._force_get_callbacks.append(self.__force_get_login)

    def __force_get_login(
        self, url: str, _: dict[str, str], commands: Sequence[CommandRequest]
    ):
        if len(commands) > 1 or not isinstance(commands[0], LoginCommand):
            if self.__token:
                return (False, url + f"?token={self.__token}")
            return
        return url + f"?cmd={commands[0].cmd}"
