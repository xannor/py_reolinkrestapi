"""REST Commands"""

from abc import ABC
from enum import IntEnum
import json
from typing import (
    Final,
    Protocol,
    TypeGuard,
    TypeVar,
    TypedDict,
)
from typing_extensions import NotRequired

from async_reolink.api.connection import model as connection_model, typing as connection_typing

from .._utilities.json import SupportsJSON

from .._utilities import providers

# pylint: disable=missing-function-docstring


class ResponseTypes(IntEnum):
    """Response Types"""

    VALUE_ONLY = 0
    DETAILED = 1


_DefaultResponseType: Final = ResponseTypes.VALUE_ONLY


class CommandJSON(TypedDict):
    """Command JSON"""

    cmd: str


class CommandKeys(Protocol):
    """Keys"""

    command: Final = "cmd"


class Request(providers.DictProvider[str, any], connection_model.Request, SupportsJSON):
    """Rest Request"""

    class JSON(CommandJSON):
        """JSON"""

        action: int
        param: dict

    class Keys(CommandKeys, Protocol):
        """Keys"""

        response_type: Final = "action"
        parameter: Final = "param"

    __slots__ = ()

    id = property(id)

    def __init__(self, /, **kwargs: any):
        super().__init__(None)

    def __json__(self, _encoder: json.JSONEncoder):
        return self._provided_value

    def _get_provided_value(self, create=False):
        if (value := super()._get_provided_value(create)) is not None or not create:
            return value
        value = {}
        self._set_provided_value(value)
        return value

    _value: JSON

    @property
    def command(self):
        if value := self._value:
            return value.get(self.Keys.command, "")
        return ""

    @command.setter
    def command(self, value):
        self._get_provided_value(True)[self.Keys.command] = str(value)

    @property
    def response_type(self):
        if value := self._value:
            return ResponseTypes(value.get(Request.Keys.response_type, _DefaultResponseType))
        return _DefaultResponseType

    @response_type.setter
    def response_type(self, value):
        self._get_provided_value(True)[self.Keys.response_type] = ResponseTypes(value)

    def _get_parameter(self, create=False) -> dict[str, any]:
        return self._get_key_value(
            self._get_provided_value,
            self.Keys.parameter,
            create,
            default=lambda: dict() if create else None,
        )

    @property
    def _parameter(self):
        return self._get_parameter()


class ChannelJSON(TypedDict):

    channel: int


class ChannelKeys(Protocol):

    channel_id: Final = "channel"


class RequestWithChannel(Request, connection_typing.ChannelValue):
    """Rest Request with Channel Parameter"""

    class Parameter(Protocol):
        """Parameter"""

        class JSON(ChannelJSON):
            """JSON"""

        class Keys(ChannelKeys, Protocol):
            """Keys"""

    _parameter: Parameter.JSON

    __slots__ = ()

    @property
    def channel_id(self):
        if value := self._parameter:
            return value.get(self.Parameter.Keys.channel_id, 0)
        return 0

    @channel_id.setter
    def channel_id(self, value):
        self._get_parameter(True)[self.Parameter.Keys.channel_id] = int(value)


T = TypeVar("T")


class Response(connection_model.Response, providers.DictProvider[str, any]):
    """Rest Response"""

    class JSON(CommandJSON):
        """JSON"""

        code: int
        value: NotRequired[dict[str, any]]
        initial: NotRequired[dict[str, any]]
        range: NotRequired[dict[str, any]]
        error: NotRequired[dict[str, any]]

    class Keys(CommandKeys, Protocol):
        """Keys"""

        code: Final = "code"
        value: Final = "value"
        initial: Final = "initial"
        range: Final = "range"
        error: Final = "error"

    @classmethod
    def is_response(cls, value: any, /, command: str | None = None) -> TypeGuard[JSON]:
        """value is command response json"""
        return (
            isinstance(value, dict)
            and cls.Keys.command in value
            and cls.Keys.code in value
            and (command is None or command == value[cls.Keys.command])
        )

    @classmethod
    def is_value(cls, response: dict):
        """response is a command value response"""
        return cls.Keys.value in response and isinstance(response[cls.Keys.value], dict)

    __slots__ = ("__request_id",)

    def __init__(self, response: JSON, /, request_id: int = None, **kwargs: any) -> None:
        super().__init__(**kwargs)
        providers.DictProvider.__init__(self, response)
        self.__request_id = request_id

    @property
    def _response(self) -> JSON:
        return self._provided_value

    @property
    def request_id(self):
        return self.__request_id

    @property
    def _value(self):
        return value.get(self.Keys.value) if (value := self._response) else None

    @property
    def _initial(self):
        return value.get(self.Keys.initial) if (value := self._response) else None

    @property
    def _range(self):
        return value.get(self.Keys.range) if (value := self._response) else None

    @property
    def is_detailed(self):
        if not (value := self._response):
            return False
        return any(k in value for k in (self.Keys.initial, self.Keys.range))

    @property
    def command(self):
        if value := self._response:
            return value.get(self.Keys.command, "")
        return ""

    @property
    def code(self):
        if value := self._response:
            return value.get(self.Keys.code, 0)
        return 0

    @property
    def _error(self):
        return value.get(self.Keys.error) if (value := self._response) else None


class UnhandledResponse(Response):
    """Unhandled/Unknown REST Command Response"""

    __slots__ = ()


# _RSP_CODE_KEY: Final = "rspCode"


class ResponseCodeJSON(TypedDict):
    """Response Code JSON"""

    rspCode: int


class ResponseCodeKeys(Protocol):
    """Response Code Keys"""

    response_code: Final = "rspCode"


class ResponseWithCode(Response, connection_typing.ResponseCode):
    """REST Command Response with code"""

    class Value(Protocol):
        """Value"""

        class JSON(ResponseCodeJSON):
            """JSON"""

        class Keys(ResponseCodeKeys, Protocol):
            """Keys"""

    _value: Value.JSON

    @classmethod
    def from_response(cls, response: any, /, request: Request | None = None, **kwargs):
        if (
            cls.is_response(response, command=request.command if request else None)
            and cls.is_value(response)
            and cls.Value.Keys.response_code in response[cls.Keys.value]
        ):
            return cls(response, request.id if request else None, **kwargs)
        return None

    __slots__ = ()

    @property
    def response_code(self):
        if value := self._value:
            return value.get(self.Value.Keys.response_code, 0)
        return 0


class ResponseWithChannel(Response, connection_typing.ChannelValue, ABC):
    """Rest Response Value with Channel"""

    class Value(Protocol):
        """Value"""

        class JSON(ChannelJSON):
            """JSON"""

        class Keys(ChannelKeys, Protocol):
            """Keys"""

    __slots__ = ("_fallback_channel_id",)

    def __init__(
        self, response: dict, /, fallback_channel_id: int | None = None, **kwargs: any
    ) -> None:
        super().__init__(response, **kwargs)
        self._fallback_channel_id = fallback_channel_id or 0

    _value: Value.JSON

    @property
    def channel_id(self):
        if value := self._value:
            return value.get(self.Value.Keys.channel_id, 0)
        return 0


class ErrorResponse(Response, connection_model.ErrorResponse):
    """Rest Error Response"""

    class Error(Protocol):
        """Error"""

        class JSON(ResponseCodeJSON):
            """JSON"""

            detail: str

        class Keys(Protocol):
            """Keys"""

            error_code: Final = ResponseCodeKeys.response_code
            details: Final = "detail"

    _error: Error.JSON

    __slots__ = ()

    @classmethod
    def from_response(cls, response: any, /, request: Request | None = None, **kwargs):
        if cls.is_response(response) and cls.is_error(response):
            return cls(response, request.id if request else None, **kwargs)
        return None

    @classmethod
    def is_error(cls, response: dict):
        """response is a command error response"""
        return cls.Keys.error in response and isinstance(response[cls.Keys.error], dict)

    @property
    def error_code(self):
        if value := self._error:
            return value.get(self.Error.Keys.error_code, 0)
        return 0

    @property
    def details(self):
        if value := self._error:
            return value.get(self.Error.Keys.details)
        return None
