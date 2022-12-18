"""REST System Typings"""

# ISO Starts with Monday as 0 but cameras follow Sunday = 0 for time
from types import MappingProxyType
from typing import Final, ValuesView, overload

from async_reolink.api.typing import WeekDays
from async_reolink.api.system.typing import StorageTypes, HourFormat

from .._utilities.missing import MISSING

_WEEKDAY_MAP: Final = MappingProxyType({_e: (int(_e.value) + 1) % 7 for _e in WeekDays})
_REV_WEEKDAY_MAP: Final = MappingProxyType({_v: _k for (_k, _v) in _WEEKDAY_MAP.items()})


@overload
def weekday_int() -> ValuesView[int]:
    ...


@overload
def weekday_int(value: WeekDays) -> int:
    ...


def weekday_int(value: WeekDays = MISSING):
    if value is MISSING:
        return _WEEKDAY_MAP.values()
    return _WEEKDAY_MAP.get(value)


def int_weekday(value: int):
    return _REV_WEEKDAY_MAP[value]


_STORAGETYPE_MAP: Final = MappingProxyType({StorageTypes.HDD: 1, StorageTypes.SDC: 2})
_REV_STORAGETYPE_MAP: Final = MappingProxyType({_v: _k for (_k, _v) in _STORAGETYPE_MAP.items()})


@overload
def storage_type_int() -> ValuesView[int]:
    ...


@overload
def storage_type_int(value: StorageTypes) -> int:
    ...


def storage_type_int(value: StorageTypes = MISSING):
    if value is MISSING:
        return _STORAGETYPE_MAP.values()
    return _STORAGETYPE_MAP.get(value)


def int_storage_type(value: int):
    return _REV_STORAGETYPE_MAP[value]


HOURFORMAT_MAP: Final = MappingProxyType({HourFormat.HR_12: 0, HourFormat.HR_24: 1})
_REV_HOURFORMAT_MAP: Final = MappingProxyType({_v: _k for (_k, _v) in HOURFORMAT_MAP.items()})


@overload
def hour_format_int() -> ValuesView[int]:
    ...


@overload
def hour_format_int(value: HourFormat) -> int:
    ...


def hour_format_int(value: HourFormat = MISSING):
    if value is MISSING:
        return HOURFORMAT_MAP.values()
    return HOURFORMAT_MAP.get(value)


def int_hour_format(value: int):
    return _REV_HOURFORMAT_MAP[value]
