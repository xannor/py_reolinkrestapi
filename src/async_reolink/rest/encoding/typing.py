"""Encoding typings"""

from types import MappingProxyType
from typing import Final, ValuesView, overload

from async_reolink.api.typing import StreamTypes


_STREAMTYPES_MAP: Final = MappingProxyType({_e: _e.name.lower() + "Stream" for _e in StreamTypes})

for _k, _v in _STREAMTYPES_MAP.items():
    StreamTypes._value2member_map_[_v] = _k


class _Missing:
    pass


_MISSING: Final = _Missing()


@overload
def stream_types_str() -> ValuesView[str]:
    ...


@overload
def stream_types_str(value: StreamTypes) -> str:
    ...


def stream_types_str(value: StreamTypes = _MISSING):
    if value is _MISSING:
        return _STREAMTYPES_MAP.values()
    return _STREAMTYPES_MAP.get(value)
