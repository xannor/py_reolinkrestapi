"""AI Typings"""

from types import MappingProxyType
from typing import Final, ValuesView, overload
from async_reolink.api.ai.typing import AITypes

_AITYPES_MAP: Final = MappingProxyType(
    {_e: "dog_cat" if _e == AITypes.PET else _e.name.lower() for _e in AITypes}
)

for _k, _v in _AITYPES_MAP.items():
    AITypes._value2member_map_[_v] = _k


class _Missing:
    pass


_MISSING: Final = _Missing()


@overload
def ai_types_str() -> ValuesView[str]:
    ...


@overload
def ai_types_str(value: AITypes) -> str:
    ...


def ai_types_str(value: AITypes = _MISSING):
    if value is _MISSING:
        return _AITYPES_MAP.values()
    return _AITYPES_MAP[value]
