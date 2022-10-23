"""REST Alarm Commands"""

from typing import Final, TypeGuard
from async_reolink.api.alarm import command as alarm

from async_reolink.api.connection.typing import CommandResponse

from ..connection.models import (
    CommandRequestWithChannel,
    CommandResponseWithChannel,
    CommandResponseTypes,
)


class GetMotionStateRequest(CommandRequestWithChannel, alarm.GetMotionStateRequest):
    """REST Get Motion State Request"""

    COMMAND: Final = "GetMdState"

    def __init__(
        self,
        channel_id: int = 0,
        response_type: CommandResponseTypes = CommandResponseTypes.VALUE_ONLY,
    ):
        super().__init__()
        self.command = type(self).COMMAND
        self.response_type = response_type
        self.channel_id = channel_id


class GetMotionStateResponse(
    CommandResponseWithChannel, alarm.GetMotionStateResponse, test="is_response"
):
    """REST Get Motion State Response"""

    __slots__ = ()

    def __init__(
        self, response: dict, *_, request: CommandRequestWithChannel = None, **kwargs
    ) -> None:
        # currently channel_id is not part of the response so we hack in a fallback
        if request is not None and request.command == GetMotionStateRequest.COMMAND:
            kwargs["fallback_channel_id"] = request.channel_id
        super().__init__(response, *_, **kwargs)

    @classmethod
    def is_response(cls, value: any, /):  # pylint: disable=signature-differs
        return super().is_response(value, GetMotionStateRequest.COMMAND)

    @property
    def state(self) -> bool:
        """state"""
        return value.get("state", 0) if (value := self._get_value()) is not None else 0


class CommandFactory(alarm.CommandFactory):
    """REST Alarm Command Factory"""

    def create_get_md_state(self, channel_id: int):
        return GetMotionStateRequest(channel_id)

    def is_get_md_response(
        self, response: CommandResponse
    ) -> TypeGuard[GetMotionStateResponse]:
        return isinstance(response, GetMotionStateResponse)
