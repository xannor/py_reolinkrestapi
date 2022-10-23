"""REST Record Mixin"""

from typing import Sequence
from async_reolink.api.connection.typing import (
    CommandRequest,
)
from async_reolink.api.record.mixin import Record as BaseRecord
from ..connection.models import _COMMAND_KEY
from .command import GetSnapshotRequest

from .seed import Seed

from ..connection.typing import WithConnection


class Record(BaseRecord, WithConnection):
    """REST Record Mixin"""

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self._force_get_callbacks.append(self.__force_get_login)

    def __force_get_login(
        self, _: str, query: dict[str, str], commands: Sequence[CommandRequest]
    ):
        command = commands[0]
        if len(commands) > 1 or not isinstance(command, GetSnapshotRequest):
            return
        query[_COMMAND_KEY] = command.command
        query.update(command.raw_parameter)
        query["rs"] = str(Seed())
        return True
