"""Rest Typings"""

from types import MappingProxyType
from typing import Final, ValuesView, overload

from async_reolink.api.typing import StreamTypes

_STREAMTYPES_MAP: Final = MappingProxyType({_e: _e.name.lower() for _e in StreamTypes})


class _Missing:
    pass


_MISSING: Final = _Missing()


@overload
def stream_type_str() -> ValuesView[str]:
    ...


@overload
def stream_type_str(value: StreamTypes) -> str:
    ...


def stream_type_str(value: StreamTypes = _MISSING):
    if value is _MISSING:
        return _STREAMTYPES_MAP.values()
    return _STREAMTYPES_MAP.get(value)
