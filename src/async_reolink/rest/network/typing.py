"""REST Network Typings"""

from types import MappingProxyType
from typing import Final, ValuesView, overload

from async_reolink.api.network.typing import LinkTypes

_LINKTYPES_MAP: Final = MappingProxyType(
    {_e: "Static" if _e == LinkTypes.STATIC else _e.name.upper() for _e in LinkTypes}
)

for _k, _v in _LINKTYPES_MAP.items():
    LinkTypes._value2member_map_[_v] = _k


class _Missing:
    pass


_MISSING: Final = _Missing()


@overload
def link_types_str() -> ValuesView[str]:
    ...


@overload
def link_types_str(value: LinkTypes) -> str:
    ...


def link_types_str(value: LinkTypes = _MISSING):
    if value is _MISSING:
        return _LINKTYPES_MAP.values()
    return _LINKTYPES_MAP.get(value)
