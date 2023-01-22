"""Encoding REST Commands"""

from typing import Final, Protocol, TypeGuard, TypedDict
from async_reolink.api.encoding import command as encoding
from async_reolink.api.connection.model import Request

from .._utilities.providers import value as providers

from .model import EncodingInfo

from ..connection.model import (
    ResponseTypes,
    RequestWithChannel,
    Response as RestCommandResponse,
    ResponseWithChannel,
)

# pylint: disable=missing-function-docstring


class GetEncodingRequest(RequestWithChannel, encoding.GetEncodingRequest):
    """Get Encoding REST Request"""

    COMMAND: Final = "GetEnc"
    _COMMAND_ID: Final = hash(COMMAND)

    def __init__(self, /, channel_id: int = ..., response_type: ResponseTypes = ...):
        super().__init__(
            command=type(self).COMMAND, channel_id=channel_id, response_type=response_type
        )

    @property
    def id(self):
        return self._COMMAND_ID ^ self.channel_id


class GetEncodingResponse(RestCommandResponse, encoding.GetEncodingResponse):
    """Get Encoding REST Response"""

    @classmethod
    def from_response(cls, response: any, /, request: Request | None = None, **kwargs):
        if super().is_response(response, GetEncodingRequest.COMMAND):
            return cls(response, request_id=request.id if request else None, **kwargs)
        return None

    class Value(Protocol):
        """Value"""

        class Encoding(Protocol):
            """Encoding"""

            class JSON(ResponseWithChannel.Value.JSON, EncodingInfo.JSON):
                """JSON"""

            class Keys(ResponseWithChannel.Value.Keys, EncodingInfo.Keys, Protocol):
                """Keys"""

        class JSON(TypedDict):
            """JSON"""

            Enc: "GetEncodingResponse.Value.Encoding.JSON"

        class Keys(Protocol):
            """Keys"""

            info: Final = "Enc"

    __slots__ = ()

    _value: Value.JSON

    def _get_info(self, create=False) -> Value.Encoding.JSON:
        return self.lookup_value(self._get_value, self.Value.Keys.info, create=create, default=None)

    @property
    def _info(self):
        return self._get_info()

    @property
    def info(self):
        return EncodingInfo(self._get_info)

    @property
    def channel_id(self):
        if value := self._info:
            return value.get(self.Value.Encoding.Keys.channel_id, 0)
        return 0
