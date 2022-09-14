"""Security Models"""


# pylint: disable=too-few-public-methods
# pylint:disable=missing-function-docstring

from typing import Callable


class LoginToken:
    """Login Token"""

    __slots__ = ("_factory",)

    def __init__(self, factory: Callable[[], dict]) -> None:
        super().__init__()
        self._factory = factory

    @property
    def lease_time(self) -> int:
        if (value := self._factory()) is None:
            return 0
        return value.get("leaseTime", 0)

    @property
    def name(self) -> str:
        if (value := self._factory()) is None:
            return ""
        return value.get("name", "")


class LoginTokenV2(LoginToken):
    """Login Token V2"""

    __slots__ = ()

    @property
    def check(self) -> int:
        if (value := self._factory()) is None:
            return 0
        return value.get("checkBasic", 0)

    @property
    def count(self) -> int:
        if (value := self._factory()) is None:
            return 0
        return value.get("countTotal", 0)


class DigestInfo:
    """Digest Info"""

    __slots__ = ("_factory",)

    def __init__(self, factory: Callable[[], dict]) -> None:
        super().__init__()
        self._factory = factory

    @property
    def cnonce(self):
        if (value := self._factory()) is None:
            return ""
        return value.get("Cnonce", "")

    @property
    def method(self):
        if (value := self._factory()) is None:
            return ""
        return value.get("Method", "")

    @property
    def nc(self):  # pylint: disable=invalid-name
        if (value := self._factory()) is None:
            return ""
        return value.get("Nc", "")

    @property
    def nonce(self):
        if (value := self._factory()) is None:
            return ""
        return value.get("Nonce", "")

    @property
    def qop(self):
        if (value := self._factory()) is None:
            return ""
        return value.get("Qop", "")

    @property
    def realm(self):
        if (value := self._factory()) is None:
            return ""
        return value.get("Realm", "")

    @property
    def response(self):
        if (value := self._factory()) is None:
            return ""
        return value.get("Response", "")

    @property
    def uri(self):
        if (value := self._factory()) is None:
            return ""
        return value.get("Uri", "")

    @property
    def user_name(self):
        if (value := self._factory()) is None:
            return ""
        return value.get("UserName", "")
