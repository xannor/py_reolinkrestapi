"""REST Commands"""

from abc import ABC
from enum import IntEnum
from typing import (
    Callable,
    Final,
    TypeGuard,
    TypeVar,
)

from async_reolink.api.connection import model, typing

_COMMAND_KEY: Final = "cmd"
_ACTION_KEY: Final = "action"

# pylint: disable=missing-function-docstring


class ResponseTypes(IntEnum):
    """Response Types"""

    VALUE_ONLY = 0
    DETAILED = 1


class Request(model.Request):
    """Rest Request"""

    __slots__ = ("_request",)

    id = property(id)

    def __init__(self):
        super().__init__()
        self._request = {}

    def _get_request(self):
        return self._request

    def _get_parameter(self, create=False) -> dict:
        _key: Final = "param"

        if _key in self._request or not create:
            return self._request.get(_key, None)
        return self._request.setdefault(_key, {})

    @property
    def _parameter(self):
        return self._get_parameter(True)

    @property
    def command(self) -> str:
        return self._request.get(_COMMAND_KEY, "")

    @command.setter
    def command(self, value):
        self._request[_COMMAND_KEY] = value

    @property
    def response_type(self) -> ResponseTypes:
        return self._request.get(_ACTION_KEY, ResponseTypes.VALUE_ONLY)

    @response_type.setter
    def response_type(self, value):
        self._request[_ACTION_KEY] = value


_CHANNEL_KEY: Final = "channel"


class RequestWithChannel(Request, typing.ChannelValue):
    """Rest Request with Channel Parameter"""

    __slots__ = ()

    @property
    def channel_id(self):
        return (
            parameter.get(_CHANNEL_KEY, 0)
            if (parameter := self._get_parameter()) is not None
            else 0
        )

    @channel_id.setter
    def channel_id(self, value):
        self._parameter[_CHANNEL_KEY] = value


_VALUE_KEY: Final = "value"
_CODE_KEY: Final = "code"
_ERROR_KEY: Final = "error"

T = TypeVar("T")


class Response(model.Response, ABC):
    """Rest Response"""

    @classmethod
    def is_response(cls, value: any, /, command: str | None = None) -> TypeGuard[dict]:
        """value is command response json"""
        return (
            isinstance(value, dict)
            and _COMMAND_KEY in value
            and _CODE_KEY in value
            and (command is None or command == value[_COMMAND_KEY])
        )

    @classmethod
    def is_value(cls, response: dict):
        """response is a command value response"""
        return _VALUE_KEY in response and isinstance(response[_VALUE_KEY], dict)

    __slots__ = ("_response", "_request_id")

    def __init__(self, response: dict, /, request_id: int | None = None) -> None:
        super().__init__()
        self._response = response
        self._request_id = request_id

    @property
    def request_id(self):
        return self._request_id

    def _underlying_value(self):
        return self._response

    @property
    def is_detailed(self):
        return self._get_initial() is not None or self._get_range() is not None

    @property
    def command(self) -> str:
        return self._response.get(_COMMAND_KEY, "")

    @property
    def code(self) -> int:
        return self._response.get(_CODE_KEY, 0)

    def _get_value(self) -> dict:
        return self._response.get(_VALUE_KEY, None)

    def _get_initial(self) -> dict:
        return self._response.get("initial", None)

    def _get_range(self) -> dict:
        return self._response.get("range", None)

    def _get_error(self) -> dict:
        return self._response.get(_ERROR_KEY, None)

    def _get_sub_key(
        self, key: str, factory: Callable[[], dict], __type: Callable[[any], T] = None
    ):
        def get() -> T:
            return _d.get(key, None) if (_d := factory()) else None

        return get

    def _get_sub_value(
        self, key: str, factory: Callable[[], dict], __type: Callable[[any], T] = None
    ):
        return self._get_sub_key(key, factory, __type)()


class UnhandledResponse(Response):
    """Unhandled/Unknown REST Command Response"""

    __slots__ = ()


_RSP_CODE_KEY: Final = "rspCode"


class ResponseWithCode(Response, typing.ResponseCode):
    """REST Command Response with code"""

    @classmethod
    def from_response(cls, response: any, /, request: Request | None = None):
        if (
            cls.is_response(response, command=request.command if request else None)
            and cls.is_value(response)
            and _RSP_CODE_KEY in response[_VALUE_KEY]
        ):
            return cls(response, request.id if request else None)
        return None

    __slots__ = ()

    @property
    def response_code(self):
        return value.get(_RSP_CODE_KEY, 0) if (value := self._get_value()) is not None else 0


class ResponseWithChannel(Response, typing.ChannelValue, ABC):
    """Rest Response Value with Channel"""

    __slots__ = ("_fallback_channel_id",)

    def __init__(
        self,
        response: dict,
        /,
        request_id: int | None = None,
        fallback_channel_id: int | None = None,
    ) -> None:
        super().__init__(response, request_id)
        self._fallback_channel_id = fallback_channel_id or 0

    @property
    def channel_id(self):
        return (
            value.get(_CHANNEL_KEY, self._fallback_channel_id)
            if (value := self._get_value()) is not None
            else self._fallback_channel_id
        )


class ErrorResponse(Response, model.ErrorResponse):
    """Rest Error Response"""

    __slots__ = ()

    @classmethod
    def from_response(cls, response: any, request: Request | None = None):
        if cls.is_response(response) and cls.is_error(response):
            return cls(response, request.id if request else None)
        return None

    @classmethod
    def is_error(cls, response: dict):
        """response is a command error response"""
        return _ERROR_KEY in response and isinstance(response[_ERROR_KEY], dict)

    @property
    def error_code(self) -> int:
        return value.get(_RSP_CODE_KEY, 0) if (value := self._get_error()) is not None else 0

    @property
    def details(self) -> str | None:
        return value.get("detail", 0) if (value := self._get_error()) is not None else 0
