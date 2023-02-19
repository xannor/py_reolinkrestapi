"""REST Record Mixin"""

from datetime import datetime
from typing import Sequence
from async_reolink.api.connection.model import Request
from async_reolink.api.record.mixin import Record as BaseRecord
from async_reolink.api.record import typing
from ..connection.model import Response, RequestWithChannel
from . import command

from .seed import Seed

from ..connection.typing import WithConnection


class Record(BaseRecord, WithConnection):
    """REST Record Mixin"""

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self._force_get_callbacks.append(self.__force_get_login)

    def __force_get_login(self, _: str, query: dict[str, str], commands: Sequence[Request]):
        _command = commands[0]
        if len(commands) > 1 or not isinstance(_command, command.GetSnapshotRequest):
            return
        query[RequestWithChannel.Keys.command] = _command.command
        query.update(_command.raw_parameter)
        query["rs"] = str(Seed())
        return True

    def _create_get_snapshot(self, channel_id: int):
        return command.GetSnapshotRequest(channel_id=channel_id)

    def _create_search(
        self,
        channel_id: int,
        start_time: datetime,
        end_time: datetime,
        only_status: bool,
        stream_type: typing.StreamTypes,
    ):
        request = command.SearchRecordingsRequest(channel_id=channel_id)
        request.search.start = start_time
        request.search.end = end_time
        request.search.status_only = only_status
        request.search.stream_type = stream_type
        return request

    def _is_search_response(self, response: Response):
        return isinstance(response, command.SearchRecordingsResponse)
