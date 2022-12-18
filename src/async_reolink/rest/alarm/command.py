"""REST Alarm Commands"""

from typing import Final, Protocol
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
    _COMMAND_ID: Final = hash(COMMAND)

    def __init__(
        self,
        channel_id: int = 0,
        response_type: ResponseTypes = ResponseTypes.VALUE_ONLY,
    ):
        super().__init__()
        self.command = type(self).COMMAND
        self.response_type = response_type
        self.channel_id = channel_id

    @property
    def id(self):
        return self._COMMAND_ID ^ self.channel_id


class GetMotionStateResponse(ResponseWithChannel, alarm.GetMotionStateResponse):
    """REST Get Motion State Response"""

    @classmethod
    def from_response(cls, response: any, /, request: Request | None = None, **kwargs):
        if super().is_response(response, command=GetMotionStateRequest.COMMAND):
            return cls(
                response,
                request_id=request.id if request else None,
                fallback_channel_id=request.channel_id
                if isinstance(request, RequestWithChannel)
                else None,
                **kwargs,
            )
        return None

    class Value(ResponseWithChannel.Value, Protocol):
        """Value"""

        class JSON(ResponseWithChannel.Value.JSON):
            """JSON"""

            state: int

        class Keys(ResponseWithChannel.Value, Protocol):
            """Keys"""

            state: Final = "state"

    __slots__ = ()

    @property
    def state(self):
        return True if (value := self._value) and value.get(self.Value.Keys.state, 0) else False
