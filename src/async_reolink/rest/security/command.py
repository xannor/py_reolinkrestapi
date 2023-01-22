"""Secuirty REST Commands"""

from typing import TYPE_CHECKING, Callable, Final, Protocol, Sequence, TypedDict, cast
from async_reolink.api.security import command as security, typing as security_typing

from ..connection.model import (
    Request,
    ResponseTypes,
    Response as RestResponse,
)

from ..security.typing import LoginType, level_type_str

from .._utilities.providers import value as providers

from .model import LoginToken, UserInfo

from ..model import StringRange

# pylint:disable=missing-function-docstring

_DefaultLoginType: Final = LoginType.NORMAL
_DefaultLoginTypeValue: Final = _DefaultLoginType.value


class LoginRequest(Request, security.LoginRequest):
    """REST Login Request"""

    class Parameter(Protocol):
        """Parameter"""

        class Login(Protocol):
            """Login"""

            class JSON(TypedDict):
                """JSON"""

                userName: str
                password: str
                Version: int

            class Keys(Protocol):
                """Keys"""

                user_name: Final = "userName"
                password: Final = "password"
                login_type: Final = "Version"

        class JSON(TypedDict):
            """JSON"""

            User: "LoginRequest.Parameter.Login.JSON"

        class Keys(Protocol):
            """Keys"""

            login: Final = "User"

    __slots__ = ()

    _get_parameter: providers.FactoryValue[Parameter.JSON]
    _parameter: Parameter.JSON

    COMMAND: Final = "Login"
    _COMMAND_ID: Final = hash(COMMAND)

    @property
    def id(self):
        return self._COMMAND_ID

    def __init__(
        self,
        /,
        user_name: str = ...,
        password: str = ...,
        login_type: LoginType = ...,
        response_type: ResponseTypes = ...,
    ):
        super().__init__(command=type(self).COMMAND, response_type=response_type)
        if user_name and user_name is not ...:
            self.user_name = user_name
        if password and password is not ...:
            self.password = password
        if login_type is None or login_type is ...:
            login_type = _DefaultLoginType
        self.login_type = login_type

    def _get_login(self, create=False) -> Parameter.Login.JSON:
        return self.lookup_value(
            self._get_parameter,
            self.Parameter.Keys.login,
            create=create,
            default_factory=lambda: dict() if create else None,
        )

    @property
    def _login(self):
        return self._get_login()

    @property
    def user_name(self):
        if value := self._login:
            return value.get(self.Parameter.Login.Keys.user_name, "")
        return ""

    @user_name.setter
    def user_name(self, value):
        self._get_login(True)[self.Parameter.Login.Keys.user_name] = str(value)

    @property
    def password(self):
        if value := self._login:
            return value.get(self.Parameter.Login.Keys.password, "")
        return ""

    @password.setter
    def password(self, value):
        self._get_login(True)[self.Parameter.Login.Keys.password] = str(value)

    @property
    def login_type(self):
        if value := self._login:
            return LoginType(
                value.get(self.Parameter.Login.Keys.login_type, _DefaultLoginTypeValue)
            )
        return _DefaultLoginType

    @login_type.setter
    def login_type(self, value):
        self._get_login(True)[self.Parameter.Login.Keys.login_type] = LoginType(value).value


class LoginResponse(RestResponse, security.LoginResponse):
    """REST Login Response"""

    @classmethod
    def from_response(cls, response: any, /, request: Request | None = None, **kwargs):
        if super().is_response(response, LoginRequest.COMMAND):
            return cls(response, request_id=request.id if request else None, **kwargs)
        return None

    class Value(Protocol):
        """Value"""

        class JSON(TypedDict):
            """JSON"""

            Token: LoginToken.JSON

        class Keys(Protocol):
            """Keys"""

            token: Final = "Token"

    __slots__ = ()

    _get_value: providers.FactoryValue[Value.JSON]
    _value: Value.JSON

    @property
    def token(self):
        return LoginToken(self.lookup_factory(self._get_value, self.Value.Keys.token, default=None))


class LogoutRequest(Request, security.LogoutRequest):
    """REST Logut Request"""

    __slots__ = ()

    COMMAND: Final = "Logout"
    _COMMAND_ID: Final = hash(COMMAND)

    @property
    def id(self):
        return self._COMMAND_ID

    def __init__(self, /, response_type: ResponseTypes = ...):
        super().__init__(command=type(self).COMMAND, response_type=response_type)

    def __init__(self, response_type: ResponseTypes = ResponseTypes.VALUE_ONLY) -> None:
        super().__init__()
        self.command = type(self).COMMAND
        self.response_type = response_type


class GetUserRequest(Request, security.GetUserRequest):
    """REST Get User(s) Request"""

    __slots__ = ()

    COMMAND: Final = "GetUser"
    _COMMAND_ID: Final = hash(COMMAND)

    @property
    def id(self):
        return self._COMMAND_ID

    def __init__(self, /, response_type: ResponseTypes = ...):
        super().__init__(command=type(self).COMMAND, response_type=response_type)


class _Users(providers.Value[list[dict[str, any]]], Sequence[UserInfo]):
    __slots__ = ()

    def __getitem__(self, __index: int):
        return UserInfo(self.lookup_factory(self.__get_value__, __index, default=None))

    def __len__(self):
        if value := self.__get_value__:
            return len(value)
        return 0


class _UserRange(providers.Value[dict[str, any]]):

    __slots__ = ()

    @property
    def levels(self):
        value: any
        if not isinstance(
            value := self.lookup_value(self.__get_value__, UserInfo.Keys.level, default=None), list
        ):
            return []

        return list(
            filter(
                lambda i: i is not None,
                map(
                    security_typing.LevelTypes,
                    value,
                ),
            )
        )

    @property
    def user_name(self):
        return StringRange(
            self.lookup_factory(self.__get_value__, UserInfo.Keys.user_name, default=None)
        )

    @property
    def password(self):
        return StringRange(
            self.lookup_factory(
                self.__get_value__, LoginRequest.Parameter.Login.Keys.password, default=None
            )
        )


class GetUserResponse(RestResponse, security.GetUserResponse):
    """REST Get Users(s) Response"""

    @classmethod
    def from_response(cls, response: any, /, request: Request | None = None, **kwargs):
        if super().is_response(response, GetUserRequest.COMMAND):
            return cls(response, request_id=request.id if request else None, **kwargs)
        return None

    __slots__ = ()

    @property
    def users(self):
        return _Users(
            self.lookup_factory(self._get_value, LoginRequest.Parameter.Keys.login, default=None)
        )

    @property
    def initial(self):
        return UserInfo(
            self.lookup_factory(self._get_initial, LoginRequest.Parameter.Keys.login, default=None)
        )

    @property
    def range(self):
        return _UserRange(
            self.lookup_factory(self._get_range, LoginRequest.Parameter.Keys.login, default=None)
        )
