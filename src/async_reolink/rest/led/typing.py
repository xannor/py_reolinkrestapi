"""REST LED Typings"""

from enum import Enum
from types import MappingProxyType
from typing import Final, ValuesView, overload
from async_reolink.api.led import typing as led_typing

_LIGHTSTATES_MAP: Final = MappingProxyType(
    {
        led_typing.LightStates.AUTO: "Auto",
        led_typing.LightStates.ON: "On",
        led_typing.LightStates.OFF: "Off",
    }
)

for m, v in _LIGHTSTATES_MAP.items():
    led_typing.LightStates._value2member_map_[v] = m


@overload
def light_state_str() -> ValuesView[str]:
    ...


@overload
def light_state_str(value: led_typing.LightStates) -> str:
    ...


def light_state_str(value: led_typing.LightStates = ...):
    if value is ...:
        return _LIGHTSTATES_MAP.values()
    return _LIGHTSTATES_MAP.get(value)
