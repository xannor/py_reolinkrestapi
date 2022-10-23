"""AI Models"""

from typing import (
    Callable,
    Final,
    Mapping,
    MutableMapping,
)
from async_reolink.api.ai import typing

from ..typing import FactoryValue
from .typing import AITYPES_STR_MAP

# pylint: disable=too-few-public-methods
# pylint:disable=missing-function-docstring


class AlarmState(typing.AlarmState):
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

    def __repr__(self):
        return f"<{self.__class__.__name__}: {repr(self._factory())}>"


class State(Mapping[typing.AITypes, AlarmState]):
    """AI State"""

    __slots__ = ("_value",)

    def __init__(self, value: dict) -> None:
        super().__init__()
        if value is None:
            value = {}
        self._value = value

    def __getitem__(self, __k: typing.AITypes):
        def _factory() -> dict:
            return self._value.get(AITYPES_STR_MAP[__k], None)

        return AlarmState(_factory)

    def __contains__(self, __o: typing.AITypes):
        return AITYPES_STR_MAP[__o] in self._value

    def __iter__(self):
        for _k, _v in AITYPES_STR_MAP.items():
            if _v in self._value:
                yield _k

    def __len__(self):
        return len(AITYPES_STR_MAP.values() & self._value.keys())

    def __repr__(self):
        return f"<{self.__class__.__name__}: {repr(self._value)}>"

    def update(self, value: "State"):
        if not isinstance(value, type(self)):
            raise TypeError("Can only update from another State")

        # pylint: disable=protected-access
        self._value = value._value


class AITypesMap(Mapping[typing.AITypes, bool]):
    """AI Types Map"""

    __slots__ = ("_factory",)

    def __init__(self, factory: FactoryValue[dict]) -> None:
        super().__init__()
        self._factory = factory

    def __getitem__(self, __k: typing.AITypes) -> bool:
        if (_map := self._factory()) is not None:
            return _map.get(AITYPES_STR_MAP[__k], 0)
        return False

    def __iter__(self):
        if (_map := self._factory()) is None:
            return
        for _e in typing.AITypes:
            if _map is not None and AITYPES_STR_MAP[_e] in _map:
                yield _e

    def __len__(self):
        if (_map := self._factory()) is not None:
            return _map.__len__()
        return 0

    def __repr__(self):
        return f"<{self.__class__.__name__}: {repr(self._factory())}>"


class MutableAITypesMap(AITypesMap, MutableMapping[typing.AITypes, bool]):
    """Mutable AI Types Map"""

    def __setitem__(self, __k: typing.AITypes, __v: bool) -> None:
        if (_map := self._factory(True)) is None:
            raise KeyError()
        _map[AITYPES_STR_MAP[__k]] = int(__v)

    def __delitem__(self, __v: typing.AITypes) -> None:
        if (_map := self._factory(True)) is None:
            raise KeyError()
        del _map[AITYPES_STR_MAP[__v]]

    def clear(self) -> None:
        if (_map := self._factory()) is None:
            return
        _map.clear()


_DETECT_TYPE_KEY: Final = "AiDetectType"
_TYPE_KEY: Final = "type"
_AI_TRACK_KEY: Final = "aiTrack"
_TRACK_TYPE_KEY: Final = "trackType"


class Config(typing.Config):
    """AI Configuration"""

    __slots__ = ("_factory",)

    def __init__(self, factory: Callable[[], dict]) -> None:
        super().__init__()
        if not callable(factory):
            value = factory
            if value is None:
                value = {}

            def _factory():
                return value

            factory = _factory
        self._factory = factory

    def _get_detect_type(self) -> dict:
        return (
            value.get(_DETECT_TYPE_KEY, None)
            if (value := self._factory()) is not None
            else None
        )

    def _get_type(self) -> dict:
        return (
            value.get(_TYPE_KEY, None)
            if (value := self._factory()) is not None
            else None
        )

    @property
    def detect_type(self):
        """detect type"""

        def _get():
            if (_dict := self._get_detect_type()) is not None:
                return _dict
            if (_dict := self._get_type()) is not None:
                return _dict
            return None

        return AITypesMap(_get)

    @property
    def ai_track(self) -> bool:
        return (
            value.get(_AI_TRACK_KEY, 0) if (value := self._factory()) is not None else 0
        )

    def _get_track_type(self) -> dict:
        return (
            value.get(_TRACK_TYPE_KEY, None)
            if (value := self._factory()) is not None
            else None
        )

    @property
    def track_type(self):
        return AITypesMap(self._get_track_type)

    def update(self, value: "Config"):
        if not isinstance(value, type(self)):
            raise TypeError("Can only update from another Config")
        # pylint: disable=protected-access
        _value = value._factory()

        def _factory():
            return _value

        self._factory = _factory
        return self

    def __repr__(self):
        return f"<{self.__class__.__name__}: {repr(self._factory())}>"


class MutableConfig(Config):
    """Mutable AI Configuration"""

    def __init__(self, factory: FactoryValue[dict]) -> None:
        super().__init__(factory)
        self._factory = factory

    def _get_dict(self, key: str, create=False) -> dict:
        if (parameter := self._factory(create)) is None:
            return None
        if create and key not in parameter:
            return parameter.setdefault(key, {})
        return parameter.get(key, None)

    @property
    def _value(self):
        return self._factory(True)

    @property
    def _detect_type(self):
        return self._get_dict(_DETECT_TYPE_KEY, True)

    @property
    def _type(self):
        return self._get_dict(_TYPE_KEY, True)

    @_type.setter
    def _type(self, value):
        self._value[_TYPE_KEY] = value

    @property
    def detect_type(self):
        """detect type"""

        def _get(ensure: bool):
            if (value := self._get_dict(_DETECT_TYPE_KEY, ensure)) is None:
                if (value := self._get_dict(_TYPE_KEY, ensure)) is None:
                    return None
            return value

        return MutableAITypesMap(_get)

    def _update_map(self, _map: MutableAITypesMap, value):
        _map.clear()
        if isinstance(value, Mapping):
            _map.update(**value)
        if isinstance(value, typing.AITypes):
            _map[value] = True
        for item in value:
            _map[typing.AITypes(item)] = True

    @detect_type.setter
    def detect_type(self, value):
        self._update_map(self.detect_type, value)

    @property
    def _has_track_type(self):
        if (parameter := self._factory()) is None:
            return False
        return _TRACK_TYPE_KEY in parameter

    @property
    def track_type(self):
        """track type"""

        def _get(ensure: bool):
            if self._has_track_type or ensure:
                return self._value.get(_TRACK_TYPE_KEY, {})
            return None

        return MutableAITypesMap(_get)

    @track_type.setter
    def track_type(self, value):
        self._update_map(self.track_type, value)
