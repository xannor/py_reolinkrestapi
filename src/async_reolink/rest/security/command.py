"""Secuirty REST Commands"""

from typing import TYPE_CHECKING, Callable, Final, Sequence, cast
from async_reolink.api.security import command as security, typing

from ..connection.model import (
    Request,
    ResponseTypes,
    Response as RestResponse,
)


from .model import LoginToken, UserInfo
from .typing import _STR_LEVELTYPE_MAP

from ..models import StringRange

# pylint:disable=missing-function-docstring


class LoginRequest(Request, security.LoginRequest):
    """REST Login Request"""

    __slots__ = ()

    COMMAND: Final = "Login"

    def __init__(
        self,
        user_name: str,
        password: str,
        response_type: ResponseTypes = ResponseTypes.VALUE_ONLY,
    ) -> None:
        super().__init__()
        self.command = type(self).COMMAND
        self.response_type = response_type
        self.user_name = user_name
        self.password = password

    def _get_login(self, create=False) -> dict:
        _key: Final = "User"
        if (parameter := self._get_parameter(create)) is None:
            return None
        if _key in parameter or not create:
            return parameter.get(_key, None)
        return parameter.setdefault(_key, {})

    @property
    def _login(self):
        return self._get_login(True)

    @property
    def user_name(self) -> str:
        return value.get("userName", "") if (value := self._get_login()) is not None else ""

    @user_name.setter
    def user_name(self, value):
        self._login["userName"] = value

    @property
    def password(self) -> str:
        return value.get("password", "") if (value := self._get_login()) is not None else ""

    @password.setter
    def password(self, value):
        self._login["password"] = value


class LoginResponse(RestResponse, security.LoginResponse):
    """REST Login Response"""

    @classmethod
    def from_response(cls, response: any, request: Request | None = None):
        if super().is_response(response, LoginRequest.COMMAND):
            return cls(response, request_id=request.id if request else None)
        return None

    __slots__ = ()

    def _get_token(self) -> dict:
        return value.get("Token", None) if (value := self._get_value()) is not None else None

    @property
    def token(self):
        return LoginToken(self._get_token)


class LogoutRequest(Request, security.LogoutRequest):
    """REST Logut Request"""

    __slots__ = ()

    COMMAND: Final = "Logout"

    def __init__(self, response_type: ResponseTypes = ResponseTypes.VALUE_ONLY) -> None:
        super().__init__()
        self.command = type(self).COMMAND
        self.response_type = response_type


class _UserInitial:

    __slots__ = ("_factory",)

    def __init__(self, factory: Callable[[], dict]) -> None:
        self._factory = factory

    @property
    def level(self):
        if (value := self._factory()) is None:
            return None
        return _STR_LEVELTYPE_MAP.get(value.get("level", None), None)


class _UserRange:
    __slots__ = ("_factory",)

    def __init__(self, factory: Callable[[], dict]) -> None:
        self._factory = factory

    @property
    def levels(self) -> list[typing.LevelTypes]:
        if (value := self._factory()) is None:
            return []
        if (_list := value.get("level", None)) is None:
            return []
        if TYPE_CHECKING:
            _list = cast(_list, list)
        return list(
            filter(
                lambda _e: _e is not None,
                map(lambda s: _STR_LEVELTYPE_MAP.get(s, None), _list),
            )
        )

    def _get_keyed(self, key: str):
        def _factory() -> dict:
            if (value := self._factory()) is None:
                return None
            return value.get(key, None)

        return _factory

    @property
    def user_name(self):
        return StringRange(self._get_keyed("userName"))

    @property
    def password(self):
        return StringRange(self._get_keyed("password"))


class GetUserRequest(Request, security.GetUserRequest):
    """REST Get User(s) Request"""

    __slots__ = ()

    COMMAND: Final = "GetUser"

    def __init__(self, response_type: ResponseTypes = ResponseTypes.VALUE_ONLY) -> None:
        super().__init__()
        self.command = type(self).COMMAND
        self.response_type = response_type


class _Users(Sequence[UserInfo]):
    __slots__ = ("_value",)

    def __init__(self, value: list) -> None:
        super().__init__()
        self._value = value

    def _factory(self):
        return self._value

    def _get_item(self, __index: int):
        def _factory() -> dict:
            return self._value[__index]

        return _factory

    def __getitem__(self, __index: int):
        return UserInfo(self._get_item(__index))

    def __len__(self):
        return len(self._value)


class GetUserResponse(RestResponse, security.GetUserResponse):
    """REST Get Users(s) Response"""

    @classmethod
    def from_response(cls, response: any, request: Request | None = None):
        if super().is_response(response, GetUserRequest.COMMAND):
            return cls(response, request_id=request.id if request else None)
        return None

    __slots__ = ()

    def _get_user(self, factory: Callable[[], dict]) -> dict:
        def _factory():
            return value.get("User", None) if (value := factory()) is not None else None

        return _factory

    @property
    def users(self):
        return _Users(self._get_user(self._get_value))

    @property
    def initial(self):
        return _UserInitial(self._get_user(self._get_initial))

    @property
    def range(self):
        return _UserRange(self._get_user(self._get_range))
