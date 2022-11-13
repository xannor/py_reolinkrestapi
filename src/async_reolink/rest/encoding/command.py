"""Encoding REST Commands"""

from typing import Final, TypeGuard
from async_reolink.api.encoding import command as encoding
from async_reolink.api.connection.model import Request


from .model import EncodingInfo

from ..connection.model import (
    _CHANNEL_KEY,
    ResponseTypes,
    RequestWithChannel,
    Response as RestCommandResponse,
)

# pylint: disable=missing-function-docstring


class GetEncodingRequest(RequestWithChannel, encoding.GetEncodingRequest):
    """Get Encoding REST Request"""

    COMMAND: Final = "GetEnc"

    def __init__(
        self,
        channel_id: int = 0,
        response_type: ResponseTypes = ResponseTypes.VALUE_ONLY,
    ):
        super().__init__()
        self.command = type(self).COMMAND
        self.response_type = response_type
        self.channel_id = channel_id


class GetEncodingResponse(RestCommandResponse, encoding.GetEncodingResponse):
    """Get Encoding REST Response"""

    @classmethod
    def from_response(cls, response: any, request: Request | None = None):
        if super().is_response(response, GetEncodingRequest.COMMAND):
            return cls(response, request_id=request.id if request else None)
        return None

    __slots__ = ()

    def _get_info(self) -> dict:
        if (value := self._get_value()) is None:
            return None
        return value.get("Enc", None)

    @property
    def channel_id(self) -> int:
        if (info := self._get_info()) is not None:
            return info.get(_CHANNEL_KEY, 0)
        return 0

    @property
    def info(self):
        return EncodingInfo(self._get_info)
