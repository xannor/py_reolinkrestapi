"""REST Securiy typings"""

from types import MappingProxyType
from typing import Final, Protocol, ValuesView, overload
from async_reolink.api.security.typing import LevelTypes

_LEVELTYPE_MAP: Final = MappingProxyType(
    {LevelTypes.GUEST: "guest", LevelTypes.USER: "user", LevelTypes.ADMIN: "admin"}
)

for _k, _v in _LEVELTYPE_MAP.items():
    LevelTypes._value2member_map_[_v] = _k


class _Missing:
    pass


_MISSING: Final = _Missing()


@overload
def level_type_str() -> ValuesView[str]:
    ...


@overload
def level_type_str(value: LevelTypes) -> str:
    ...


def level_type_str(value: LevelTypes = _Missing):
    if value is _MISSING:
        return _LEVELTYPE_MAP.values()
    return _LEVELTYPE_MAP.get(value)


class WithSecurity(Protocol):
    """Securty Part"""

    @property
    def _auth_token(self) -> str:
        ...
