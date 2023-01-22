"""Security Models"""


# pylint: disable=too-few-public-methods
# pylint:disable=missing-function-docstring

from dataclasses import dataclass
from typing import Callable, Final, Protocol, TypeAlias, TypedDict

from async_reolink.api.security import typing as secuirty_typing
from ..security.typing import level_type_str

from .._utilities.providers import value as providers

_JSONDict: TypeAlias = dict[str, any]


@dataclass(frozen=True, slots=True)
class AuthenticationId(secuirty_typing.AuthenticationId):
    """Authentication Id"""

    weak: int = 0
    strong: int = 0


class LoginToken(providers.Value[_JSONDict]):
    """Login Token"""

    class JSON(TypedDict):
        """JSON"""

        leaseTime: int
        name: str

    class Keys(Protocol):
        """Keys"""

        lease_time: Final = "leaseTime"
        name: Final = "name"

    __slots__ = ()

    __get_value__: providers.FactoryValue[JSON]

    @property
    def lease_time(self):
        if value := self.__get_value__():
            return value.get(self.Keys.lease_time, 0)
        return 0

    @property
    def name(self):
        if value := self.__get_value__():
            return value.get(self.Keys.name, "")
        return ""


class LoginTokenV2(LoginToken):
    """Login Token V2"""

    class JSON(LoginToken.JSON):
        """JSON"""

        checkBasic: int
        countTotal: int

    class Keys(LoginToken.Keys):
        """Keys"""

        check: Final = "checkBasic"
        count: Final = "countTotal"

    __slots__ = ()

    __get_value__: providers.FactoryValue[JSON]

    @property
    def check(self):
        if value := self.__get_value__():
            return value.get(self.Keys.check, 0)
        return 0

    @property
    def count(self) -> int:
        if value := self.__get_value__():
            return value.get(self.Keys.count, 0)
        return 0


class DigestInfo(providers.Value[_JSONDict]):
    """Digest Info"""

    class JSON(TypedDict):
        """JSON"""

        Cnonce: str
        Method: str
        Nc: str
        Nonce: str
        Qop: str
        Realm: str
        Response: str
        Uri: str
        UserName: str

    class Keys(Protocol):
        """Keys"""

        cnonce: Final = "Cnonce"
        method: Final = "Method"
        nc: Final = "Nc"
        nonce: Final = "Nonce"
        qop: Final = "Qop"
        realm: Final = "Realm"
        response: Final = "Response"
        uri: Final = "Uri"
        user_name: Final = "UserName"

    __slots__ = ()

    __get_value__: providers.FactoryValue[JSON]

    @property
    def cnonce(self):
        if value := self.__get_value__():
            return value.get(self.Keys.cnonce, "")
        return ""

    @property
    def method(self):
        if value := self.__get_value__():
            return value.get(self.Keys.method, "")
        return ""

    @property
    def nc(self):  # pylint: disable=invalid-name
        if value := self.__get_value__():
            return value.get(self.Keys.nc, "")
        return ""

    @property
    def nonce(self):
        if value := self.__get_value__():
            return value.get(self.Keys.nonce, "")
        return ""

    @property
    def qop(self):
        if value := self.__get_value__():
            return value.get(self.Keys.qop, "")
        return ""

    @property
    def realm(self):
        if value := self.__get_value__():
            return value.get(self.Keys.realm, "")
        return ""

    @property
    def response(self):
        if value := self.__get_value__():
            return value.get(self.Keys.response, "")
        return ""

    @property
    def uri(self):
        if value := self.__get_value__():
            return value.get(self.Keys.uri, "")
        return ""

    @property
    def user_name(self):
        if value := self.__get_value__():
            return value.get(self.Keys.user_name, "")
        return ""


_DefaultLevelType = secuirty_typing.LevelTypes.GUEST
_DefaultLevelTypeStr = level_type_str(_DefaultLevelType)


class UserInfo(providers.Value[_JSONDict], secuirty_typing.UserInfo):
    """REST User Record"""

    class JSON(TypedDict):
        """JSON"""

        userName: str
        level: str

    class Keys(Protocol):
        """Keys"""

        user_name: Final = "userName"
        level: Final = "level"

    __slots__ = ()

    __get_value__: providers.FactoryValue[JSON]

    @property
    def user_name(self) -> str:
        if value := self.__get_value__():
            return value.get(self.Keys.user_name, "")
        return ""

    @property
    def level(self):
        if value := self.__get_value__():
            return secuirty_typing.LevelTypes(value.get(self.Keys.level, _DefaultLevelTypeStr))
        return _DefaultLevelType
