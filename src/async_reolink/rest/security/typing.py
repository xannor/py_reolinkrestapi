"""REST Securiy typings"""

from types import MappingProxyType
from typing import Final, Protocol
from async_reolink.api.security import typing

_STR_LEVELTYPE_MAP: Final = MappingProxyType(
    {
        "guest": typing.LevelTypes.GUEST,
        "user": typing.LevelTypes.USER,
        "admin": typing.LevelTypes.ADMIN,
    }
)
_LEVELTYPE_STR_MAP: Final = MappingProxyType(
    {_v: _k for _k, _v in _STR_LEVELTYPE_MAP.items()}
)


class WithSecurity(Protocol):
    """Securty Part"""

    @property
    def _auth_token(self) -> str:
        ...
