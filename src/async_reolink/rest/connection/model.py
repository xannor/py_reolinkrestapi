"""REST Commands"""

from abc import ABC
from enum import IntEnum
import json
from typing import (
    Final,
    Protocol,
    TypeAlias,
    TypeGuard,
    TypeVar,
    TypedDict,
)
from typing_extensions import NotRequired, Unpack

from async_reolink.api.connection import model as connection_model, typing as connection_typing

from .._utilities.json import SupportsJSON

from .._utilities.providers import value as providers

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


_JSONDict: TypeAlias = dict[str, any]


class Request(providers.Value[_JSONDict], connection_model.Request, SupportsJSON):
    """Rest Request"""

    class KwArgs(TypedDict):
        """Keyword Args"""

        command: str
        response_type: NotRequired[ResponseTypes]

    class JSON(CommandJSON):
        """JSON"""

        action: int
        param: _JSONDict

    class Keys(CommandKeys, Protocol):
        """Keys"""

        response_type: Final = "action"
        parameter: Final = "param"

    __slots__ = ()

    @property
    def id(self):
        return id(self)

    def __init__(self, /, command: str, response_type: ResponseTypes = ..., **kwargs: any):
        super().__init__(self.JSON(cmd=command), **kwargs)
        self.response_type = response_type

    __get_value__: providers.FactoryValue[JSON]

    def __json__(self, _encoder: json.JSONEncoder):
        return self.__get_value__()

    @property
    def command(self):
        _default = ""
        return (
            value.get(self.Keys.command, _default) if (value := self.__get_value__()) else _default
        )

    @property
    def response_type(self):
        return (
            ResponseTypes(value.get(self.Keys.response_type, _DefaultResponseType))
            if (value := self.__get_value__())
            else _DefaultResponseType
        )

    @response_type.setter
    def response_type(self, value):
        if value is None or value is ...:
            value = ResponseTypes.VALUE_ONLY
        self.__get_value__(True)[self.Keys.response_type] = ResponseTypes(value)

    def _get_parameter(self, create=False) -> _JSONDict:
        return self.lookup_value(
            self.__get_value__,
            self.Keys.parameter,
            create=create,
            default_factory=lambda: dict() if create else None,
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

    class KwArgs(Request.KwArgs):
        """Keyword Args"""

        channel: NotRequired[int]

    class Parameter(Protocol):
        """Parameter"""

        class JSON(ChannelJSON):
            """JSON"""

        class Keys(ChannelKeys, Protocol):
            """Keys"""

    DEFAULT_CHANNEL: Final = 0

    _get_parameter: providers.FactoryValue[Parameter.JSON]
    _parameter: Parameter.JSON

    __slots__ = ()

    def __init__(self, /, channel_id: int = ..., **kwargs: Unpack[Request.KwArgs]):
        super().__init__(**kwargs)
        if channel_id is not ...:
            self.channel_id = channel_id

    @property
    def channel_id(self):
        if value := self._parameter:
            return value.get(self.Parameter.Keys.channel_id, self.DEFAULT_CHANNEL)
        return self.DEFAULT_CHANNEL

    @channel_id.setter
    def channel_id(self, value):
        if not value:
            value = self.DEFAULT_CHANNEL
        self._get_parameter(True)[self.Parameter.Keys.channel_id] = int(value)


T = TypeVar("T")


class Response(connection_model.Response, providers.Value[_JSONDict], ABC):
    """Rest Response"""

    class JSON(CommandJSON):
        """JSON"""

        code: int
        value: NotRequired[_JSONDict]
        initial: NotRequired[_JSONDict]
        range: NotRequired[_JSONDict]
        error: NotRequired[_JSONDict]

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
        super().__init__(response, **kwargs)
        self.__request_id = request_id

    __get_value__: providers.FactoryValue[JSON]

    @property
    def request_id(self):
        return self.__request_id

    def _get_value(self, create=False) -> _JSONDict:
        return self.lookup_value(self.__get_value__, self.Keys.value, create=create, default=None)

    @property
    def _value(self):
        return self._get_value()

    def _get_initial(self, create=False) -> _JSONDict:
        return self.lookup_value(self.__get_value__, self.Keys.initial, create=create, default=None)

    @property
    def _initial(self):
        return self._get_initial()

    def _get_range(self, create=False) -> _JSONDict:
        return self.lookup_value(self.__get_value__, self.Keys.range, create=create, default=None)

    @property
    def _range(self):
        return self._get_range()

    def _get_error(self, create=False) -> _JSONDict:
        return self.lookup_value(self.__get_value__, self.Keys.error, create=create, default=None)

    @property
    def _error(self):
        return self._get_error()

    @property
    def is_detailed(self):
        if not (value := self.__get_value__()):
            return False
        return any(k in value for k in (self.Keys.initial, self.Keys.range))

    @property
    def command(self):
        if value := self.__get_value__():
            return value.get(self.Keys.command, "")
        return ""

    @property
    def code(self):
        if value := self.__get_value__():
            return value.get(self.Keys.code, 0)
        return 0


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

    _get_value: providers.FactoryValue[Value.JSON]
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
        if fallback_channel_id is None or fallback_channel_id is ...:
            fallback_channel_id = RequestWithChannel.DEFAULT_CHANNEL
        self._fallback_channel_id = int(fallback_channel_id)

    _get_value: providers.FactoryValue[Value.JSON]
    _value: Value.JSON

    @property
    def channel_id(self):
        if value := self._value:
            return value.get(self.Value.Keys.channel_id, self._fallback_channel_id)
        return self._fallback_channel_id


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

    _get_error: providers.FactoryValue[Error.JSON]
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
