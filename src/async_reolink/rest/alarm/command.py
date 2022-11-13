"""REST Alarm Commands"""

from typing import Final, TypeGuard
from async_reolink.api.alarm import command as alarm

from async_reolink.api.connection.model import Request

from ..connection.model import (
    RequestWithChannel,
    ResponseWithChannel,
    ResponseTypes,
)


class GetMotionStateRequest(RequestWithChannel, alarm.GetMotionStateRequest):
    """REST Get Motion State Request"""

    COMMAND: Final = "GetMdState"

    def __init__(
        self,
        channel_id: int = 0,
        response_type: ResponseTypes = ResponseTypes.VALUE_ONLY,
    ):
        super().__init__()
        self.command = type(self).COMMAND
        self.response_type = response_type
        self.channel_id = channel_id


class GetMotionStateResponse(ResponseWithChannel, alarm.GetMotionStateResponse):
    """REST Get Motion State Response"""

    @classmethod
    def from_response(cls, response: any, request: Request | None = None):
        if super().is_response(response, command=GetMotionStateRequest.COMMAND):
            return cls(
                response,
                request_id=request.id if request else None,
                fallback_channel_id=request.channel_id
                if isinstance(request, RequestWithChannel)
                else None,
            )
        return None

    __slots__ = ()

    @property
    def state(self) -> bool:
        """state"""
        return value.get("state", 0) if (value := self._get_value()) is not None else 0
