"""REST Record"""

from typing import Sequence
from dataclasses import asdict
from async_reolink.api.commands import (
    CommandRequest,
    COMMAND,
)
from async_reolink.api.record import Record as BaseRecord, SnapshotCommand
from .seed import Seed

from . import connection


class Record(BaseRecord):
    """REST Record Mixin"""

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        if isinstance(self, connection.Connection):
            self._force_get_callbacks.append(self.__force_get_login)

    def __force_get_login(
        self, _: str, query: dict[str, str], commands: Sequence[CommandRequest]
    ):
        command = commands[0]
        if len(commands) > 1 or not isinstance(command, SnapshotCommand):
            return
        query[COMMAND] = command.cmd
        query.update(asdict(command.param))
        query["rs"] = str(Seed())
        return True
