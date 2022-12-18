"""Secuirty REST Commands"""

from typing import TYPE_CHECKING, Callable, Final, Protocol, Sequence, TypedDict, cast
from async_reolink.api.security import command as security, typing as security_typing

from ..connection.model import (
    Request,
    ResponseTypes,
    Response as RestResponse,
)

from ..security.typing import level_type_str

from .._utilities import providers

from .model import LoginToken, UserInfo

from ..model import StringRange

# pylint:disable=missing-function-docstring


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
                version: Final = "Version"

        class JSON(TypedDict):
            """JSON"""

            User: "LoginRequest.Parameter.Login.JSON"

        class Keys(Protocol):
            """Keys"""

            login: Final = "User"

    __slots__ = ()

    _parameter: Parameter.JSON

    COMMAND: Final = "Login"
    _COMMAND_ID: Final = hash(COMMAND)

    @property
    def id(self):
        return self._COMMAND_ID

    def __init__(
        self,
        user_name: str,
        password: str,
        version: int = 0,
        response_type: ResponseTypes = ResponseTypes.VALUE_ONLY,
    ) -> None:
        super().__init__()
        self.command = type(self).COMMAND
        self.response_type = response_type
        self.user_name = user_name
        self.password = password
        self.version = version

    def _get_login(self, create=False):
        if not (value := self._get_parameter(create)):
            return None
        if not (login := value.get(self.Parameter.Keys.login)) and create:
            login: dict = value.setdefault(self.Parameter.Keys.login, {})
        return login

    _login: Parameter.Login.JSON = property(_get_login)

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
    def version(self):
        if value := self._login:
            return value.get(self.Parameter.Login.Keys.version, 0)
        return 0

    @version.setter
    def version(self, value):
        self._get_login(True)[self.Parameter.Login.Keys.version] = int(value)


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

    _value: Value.JSON

    @property
    def _token(self):
        if value := self._value:
            return value.get(self.Value.Keys.token)
        return None

    @property
    def token(self):
        return LoginToken(lambda: self._token)


class LogoutRequest(Request, security.LogoutRequest):
    """REST Logut Request"""

    __slots__ = ()

    COMMAND: Final = "Logout"
    _COMMAND_ID: Final = hash(COMMAND)

    @property
    def id(self):
        return self._COMMAND_ID

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

    def __init__(self, response_type: ResponseTypes = ResponseTypes.VALUE_ONLY) -> None:
        super().__init__()
        self.command = type(self).COMMAND
        self.response_type = response_type


class _Users(providers.ListProvider[dict[str, any]], Sequence[UserInfo]):
    __slots__ = ()

    def __getitem__(self, __index: int):
        return UserInfo(lambda _: self._get_index_value(self._get_provided_value, __index))

    def __len__(self):
        if value := self._provided_value:
            return len(value)
        return 0


class _UserRange(providers.DictProvider[str, any]):

    __slots__ = ()

    @property
    def levels(self):
        if not (value := self._provided_value.get(UserInfo.Keys.level)):
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
        return StringRange(lambda _: self._provided_value.get(UserInfo.Keys.user_name))

    @property
    def password(self):
        return StringRange(
            lambda _: self._provided_value.get(LoginRequest.Parameter.Login.Keys.password)
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
        return _Users(lambda _: self._provided_value.get(LoginRequest.Parameter.Keys.login))

    @property
    def initial(self):
        return UserInfo(lambda _: self._initial.get(LoginRequest.Parameter.Keys.login))

    @property
    def range(self):
        return _UserRange(lambda _: self._range.get(LoginRequest.Parameter.Keys.login))
