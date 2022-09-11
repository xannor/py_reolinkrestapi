"""AI Models"""

from typing import (
    Callable,
    Mapping,
    MutableMapping,
)
from async_reolink.api.ai.typings import AITypes, AlarmState as BaseAlarmState

from ..typings import FactoryValue
from .typings import AITYPES_STR_MAP

# pylint: disable=too-few-public-methods
# pylint:disable=missing-function-docstring


class AlarmState(BaseAlarmState):
    """Alarm State"""

    __slots__ = ("_factory",)

    def __init__(self, factory: Callable[[], dict]) -> None:
        super().__init__()
        self._factory = factory

    @property
    def state(self) -> bool:
        if (value := self._factory()) is not None:
            return value.get("alarm_state", 0)
        return False

    @property
    def supported(self) -> bool:
        if (value := self._factory()) is not None:
            return value.get("support", 0)
        return False


class AITypesMap(Mapping[AITypes, bool]):
    """AI Types Map"""

    __slots__ = ("_factory",)

    def __init__(self, factory: FactoryValue[dict]) -> None:
        super().__init__()
        self._factory = factory

    def __getitem__(self, __k: AITypes) -> bool:
        if (_map := self._factory()) is not None:
            return _map.get(AITYPES_STR_MAP[__k], 0)
        return False

    def __iter__(self):
        if (_map := self._factory()) is None:
            return
        for _e in AITypes:
            if _map is not None and AITYPES_STR_MAP[_e] in _map:
                yield _e

    def __len__(self):
        if (_map := self._factory()) is not None:
            return _map.__len__()
        return 0


class MutableAITypesMap(AITypesMap, MutableMapping[AITypes, bool]):
    """Mutable AI Types Map"""

    def __setitem__(self, __k: AITypes, __v: bool) -> None:
        if (_map := self._factory(True)) is None:
            raise KeyError()
        _map[AITYPES_STR_MAP[__k]] = int(__v)

    def __delitem__(self, __v: AITypes) -> None:
        if (_map := self._factory(True)) is None:
            raise KeyError()
        del _map[AITYPES_STR_MAP[__v]]

    def clear(self) -> None:
        if (_map := self._factory()) is None:
            return
        _map.clear()
