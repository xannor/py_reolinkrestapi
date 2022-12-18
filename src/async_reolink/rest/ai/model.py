"""AI Models"""

from abc import ABC, abstractmethod
from typing import (
    Callable,
    Final,
    Iterable,
    Mapping,
    MutableMapping,
    Protocol,
    TypedDict,
)
from async_reolink.api.ai import typing as ai_typing

from .._utilities import providers

from .. import model

from ..ai.typing import ai_types_str

# pylint: disable=too-few-public-methods
# pylint:disable=missing-function-docstring


class AlarmState(providers.DictProvider[str, any], ai_typing.AlarmState):
    """Alarm State"""

    class JSON(TypedDict):
        """JSON"""

        alarm_state: int
        support: int

    class Keys(Protocol):
        """Keys"""

        state: Final = "alarm_state"
        supported: Final = "support"

    __slots__ = ()

    _provided_value: JSON

    @property
    def state(self):
        return True if (value := self._provided_value) and value.get(self.Keys.state) else False

    @property
    def supported(self):
        return True if (value := self._provided_value) and value.get(self.Keys.supported) else False


class State(providers.DictProvider[str, any], Mapping[ai_typing.AITypes, AlarmState]):
    """AI State"""

    __slots__ = ()

    def __getitem__(self, __k: ai_typing.AITypes):
        def _factory(_: bool) -> dict:
            return self._provided_value.get(ai_types_str(__k), None)

        return AlarmState(_factory)

    def __contains__(self, __o: ai_typing.AITypes):
        return ai_types_str(__o) in self._provided_value

    def __iter__(self):
        for _k in ai_typing.AITypes:
            if ai_types_str(_k) in self._provided_value:
                yield _k

    def __len__(self):
        if _map := self._provided_value:
            return len(ai_types_str() & _map.keys())
        return 0


class UpdatableState(State):
    """Updatable REST AI State"""

    __slots__ = ()

    def update(self, value: State):
        if not isinstance(value, type(self)):
            raise TypeError("Can only update from another State")

        # pylint: disable=protected-access
        self._set_value(value._provided_value)
        return self


class AITypesMap(providers.DictProvider[str, any], Mapping[ai_typing.AITypes, bool]):
    """AI Types Map"""

    __slots__ = ()

    def __getitem__(self, __k: ai_typing.AITypes) -> bool:
        if _map := self._provided_value:
            return True if _map.get(ai_types_str(__k), 0) else False
        return False

    def __iter__(self):
        if not (_map := self._provided_value):
            return
        for _e in ai_typing.AITypes:
            if ai_types_str(_e) in _map:
                yield _e

    def __len__(self):
        if _map := self._provided_value:
            return len(ai_types_str() & _map.keys())
        return 0


class MutableAITypesMap(AITypesMap, MutableMapping[ai_typing.AITypes, bool]):
    """Mutable AI Types Map"""

    __slots__ = ()

    def __setitem__(self, __k: ai_typing.AITypes, __v: bool) -> None:
        if (_map := self._get_value(True)) is None:
            raise KeyError()
        _map[ai_types_str(__k)] = int(__v)

    def __delitem__(self, __v: ai_typing.AITypes) -> None:
        if (_map := self._get_value(True)) is None:
            raise KeyError()
        del _map[ai_types_str(__v)]

    def clear(self) -> None:
        if (_map := self._provided_value) is None:
            return
        _map.clear()


class Config(providers.DictProvider[str, any], ai_typing.Config):
    """AI Configuration"""

    class JSON(TypedDict):
        """JSON"""

        AiDetectType: dict[str, int]
        type: dict[str, int]
        aiTrack: int
        trackType: dict[str, int]

    class Keys(Protocol):
        """Keys"""

        detect_type: Final = "AiDetectType"
        type: Final = "type"
        ai_track: Final = "aiTrack"
        track_type: Final = "trackType"

    __slots__ = ()

    def _get_detect_type(self, create=False) -> dict:
        if value := self._get_value(create):
            return value.get(self.Keys.detect_type)
        return None

    _detect_type: dict[str, int] = property(_get_detect_type)

    def _get_type(self, create=False) -> dict:
        if value := self._get_value(create):
            return value.get(self.Keys.type)
        return None

    _type: dict[str, int] = property(_get_type)

    @property
    def detect_type(self):
        """detect type"""

        return AITypesMap(lambda _: self._detect_type)

    @property
    def ai_track(self):
        return True if (value := self.__value) and value.get(self.Keys.ai_track, 0) else False

    def _get_track_type(self, create=False) -> dict:
        if value := self._get_value(create):
            return value.get(self.Keys.track_type)
        return None

    _track_type: dict[str, int] = property(_get_track_type)

    @property
    def track_type(self):
        return AITypesMap(lambda _: self._track_type)


class MutableConfig(Config):
    """Mutable AI Configuration"""

    __slots__ = ()

    def _get_detect_type(self, create=False) -> dict:
        if (value := super()._get_detect_type(create)) or not create:
            return value
        return self._get_value(True).setdefault(self.Keys.detect_type, {})

    @property
    def detect_type(self):
        """detect type"""

        return MutableAITypesMap(lambda create: self._get_detect_type(create))

    def _update_aitypes_map(
        self,
        __map: MutableAITypesMap,
        value: Mapping[ai_typing.AITypes, bool] | Iterable[ai_typing.AITypes] | ai_typing.AITypes,
    ):
        __map.clear()
        if isinstance(value, Mapping):
            __map.update(**value)
        elif isinstance(value, ai_typing.AITypes):
            __map[value] = True
        else:
            for item in value:
                __map[ai_typing.AITypes(item)] = True

    @detect_type.setter
    def detect_type(self, value):
        self._update_aitypes_map(self.detect_type, value)

    def _get_track_type(self, create=False) -> dict:
        if (value := super()._get_track_type(create)) or not create:
            return value
        return self._get_value(True).setdefault(self.Keys.track_type, {})

    @Config.ai_track.setter
    def ai_track(self, value):
        self._get_value(True)[self.Keys.ai_track] = int(value)

    @property
    def track_type(self):
        """track type"""

        return MutableAITypesMap(lambda create: self._get_track_type(create))

    @track_type.setter
    def track_type(self, value):
        self._update_aitypes_map(self.track_type, value)

    def update(self, value: ai_typing.Config):
        if isinstance(value, Config):
            if _u := self._value_factory(True):
                _u.update({**value})
            return
        try:
            self.ai_track = value.ai_track
        except AttributeError:
            pass
        try:
            self.detect_type.update(value.detect_type)
        except AttributeError:
            pass
        try:
            self.track_type.update(value.track_type)
        except AttributeError:
            pass
