"""AI Models"""

from typing import (
    Final,
    Iterable,
    Mapping,
    MutableMapping,
    Protocol,
    TypeAlias,
    TypedDict,
)
from async_reolink.api.ai import typing as ai_typing

from .._utilities.providers import value as providers

from ..ai.typing import ai_types_str

# pylint: disable=too-few-public-methods
# pylint:disable=missing-function-docstring

_JSONDict: TypeAlias = dict[str, any]


class AlarmState(providers.Value[_JSONDict], ai_typing.AlarmState):
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

    __get_value__: providers.FactoryValue[JSON]

    @property
    def state(self):
        return True if (value := self.__get_value__()) and value.get(self.Keys.state, 0) else False

    @property
    def supported(self):
        return (
            True if (value := self.__get_value__()) and value.get(self.Keys.supported, 0) else False
        )


class State(providers.Value[_JSONDict], Mapping[ai_typing.AITypes, AlarmState]):
    """AI State"""

    __slots__ = ()

    __get_value__: providers.FactoryValue[dict[str, AlarmState.JSON]]

    def __getitem__(self, __k: ai_typing.AITypes):
        return AlarmState(self.lookup_factory(self.__get_value__, ai_types_str(__k)))

    def __contains__(self, __o: ai_typing.AITypes):
        if not (value := self.__get_value__()):
            return False
        return ai_types_str(__o) in value

    def __iter__(self):
        if not (value := self.__get_value__()):
            return
        for _k in ai_typing.AITypes:
            if ai_types_str(_k) in value:
                yield _k

    def __len__(self):
        if not (value := self.__get_value__()):
            return 0
        return len(ai_types_str() & value.keys())


class UpdatableState(State):
    """Updatable REST AI State"""

    __slots__ = ()

    def update(self, value: State):
        if not isinstance(value, State):
            raise TypeError("Can only update from another State")

        self.__set_value__(value.__get_value__())
        return self


class AITypesMap(providers.Value[_JSONDict], Mapping[ai_typing.AITypes, bool]):
    """AI Types Map"""

    __slots__ = ()

    def __getitem__(self, __k: ai_typing.AITypes):
        if not (value := self.__get_value__()):
            return False

        return True if value.get(ai_types_str(__k), 0) else False

    def __iter__(self):
        if not (value := self.__get_value__()):
            return
        for _e in ai_typing.AITypes:
            if ai_types_str(_e) in value:
                yield _e

    def __len__(self):
        if not (value := self.__get_value__()):
            return 0

        return len(ai_types_str() & value.keys())


class MutableAITypesMap(AITypesMap, MutableMapping[ai_typing.AITypes, bool]):
    """Mutable AI Types Map"""

    __slots__ = ()

    def __default_factory__(self, create=False):
        if not create:
            return None
        value = {}
        if self is not None and not isinstance(self, type):
            self.__set_value__(value)
        return value

    def __init__(
        self, get_value: providers.FactoryValue[_JSONDict] = None, /, **kwargs: any
    ) -> None:
        super().__init__(
            get_value if get_value is not None else self.create_factory(default_factory=dict),
            **kwargs,
        )

    def __setitem__(self, __k: ai_typing.AITypes, __v: bool) -> None:
        if not (value := self.__get_value__(True)):
            raise KeyError()

        value[ai_types_str(__k)] = int(bool(__v))

    def __delitem__(self, __v: ai_typing.AITypes) -> None:
        if not (value := self.__get_value__()):
            return
        del value[ai_types_str(__v)]

    def clear(self) -> None:
        if not (value := self.__get_value__()):
            return
        value.clear()


class Config(providers.Value[_JSONDict], ai_typing.Config):
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

    __get_value__: providers.FactoryValue[JSON]

    @property
    def _detect_type(self, create=False) -> _JSONDict:
        return self.lookup_value(self.__get_value__, self.Keys.detect_type, create, default=None)

    @property
    def detect_type(self):
        """detect type"""

        return AITypesMap(type(self)._detect_type.fget.__get__(self))

    # @property
    # def type(self):
    #     """old type"""

    #     return AITypesMap(self._key_value_factory(self.__get_value__, self.Keys.type))

    @property
    def ai_track(self):
        return (
            True if (value := self.__get_value__()) and value.get(self.Keys.ai_track, 0) else False
        )

    @property
    def _track_type(self, create=False) -> _JSONDict:
        return self.lookup_value(self.__get_value__, self.Keys.track_type, create, default=None)

    @property
    def track_type(self):
        return AITypesMap(type(self)._track_type.fget.__get__(self))

    def __copy_values__(self):
        if (value := self.__get_value__()) is None:
            return None
        copy = value.copy()
        for _k in {self.Keys.detect_type, self.Keys.track_type, self.Keys.type} & copy.keys():
            _d: dict = copy[_k]
            copy[_k] = _d.copy()
        return copy


class MutableConfig(Config):
    """Mutable AI Configuration"""

    __slots__ = ()

    def __default_factory__(self, create=False):
        if not create:
            return None
        value = {}
        if self is not None and not isinstance(self, type):
            self.__set_value__(value)
        return value

    @property
    def _detect_type(self, create=False) -> _JSONDict:
        return self.lookup_value(
            self.__get_value__,
            self.Keys.detect_type,
            create,
            default_factory=lambda: dict() if create else None,
        )

    @property
    def detect_type(self):
        """detect type"""

        return MutableAITypesMap(type(self)._detect_type.fget.__get__(self))

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

    @Config.ai_track.setter
    def ai_track(self, value):
        self.__get_value__(True)[self.Keys.ai_track] = int(bool(value))

    @property
    def _track_type(self, create=False) -> _JSONDict:
        return self.lookup_value(
            self.__get_value__,
            self.Keys.track_type,
            create,
            default_factory=lambda: dict() if create else None,
        )

    @property
    def track_type(self):
        """track type"""

        return MutableAITypesMap(type(self)._track_type.fget.__get__(self))

    @track_type.setter
    def track_type(self, value):
        self._update_aitypes_map(self.track_type, value)

    def update(self, value: ai_typing.Config):
        if isinstance(value, Config):
            _d: Config.JSON
            if (_d := value.__copy_values__()) is not None:
                if _u := self.__get_value__(True):
                    _u.update(_d)
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
