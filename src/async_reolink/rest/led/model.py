"""LED Models"""

from typing import Callable, Final, Protocol, TypeAlias, TypedDict
from async_reolink.api.led import typing as led_typing
from async_reolink.api.typing import PercentValue, SimpleTime as SimpleTimeType
from async_reolink.api.model import SimpleTime

from .._utilities.providers import value as providers
from .._utilities import copy

from .. import model

from ..ai.model import AITypesMap, MutableAITypesMap

# pylint: disable=missing-function-docstring

_JSONDict: TypeAlias = dict[str, any]


class LightingSchedule(providers.Value[_JSONDict], led_typing.LightingSchedule):
    """Lighting Schedule"""

    __slots__ = ()

    _START_PREFIX: Final = "Start"
    _END_PREFIX: Final = "End"

    @property
    def start(self):
        return model.SimpleTime(self.__get_value__, prefix=self._START_PREFIX, titleCase=True)

    @property
    def end(self):
        return model.SimpleTime(self.__get_value__, prefix=self._END_PREFIX, titleCase=True)


class MutableLightingSchedule(LightingSchedule):
    """Mutable Lighting schedule"""

    def __default_factory__(self, create=False):
        if not create:
            return None
        value = {}
        if self is not None and not isinstance(self, type):
            self.__set_value__(value)
        return value

    @property
    def start(self):
        return model.MutableSimpleTime(
            self.__get_value__, prefix=self._START_PREFIX, titleCase=True
        )

    @start.setter
    def start(self, value):
        self.start.update(value)

    @property
    def end(self):
        return model.MutableSimpleTime(self.__get_value__, self._END_PREFIX)

    @end.setter
    def end(self, value):
        self.end.update(value)

    def update(self, value: led_typing.LightingSchedule):
        if isinstance(value, LightingSchedule):
            if _d := value.__get_value__():
                self.__get_value__(True).update(_d)
            return
        try:
            self.start = value.start
        except AttributeError:
            pass
        try:
            self.end = value.end
        except AttributeError:
            pass


class WhiteLedInfo(providers.Value[_JSONDict], led_typing.WhiteLedInfo):
    """White Led Info"""

    class JSON(TypedDict):
        """JSON"""

        bright: int
        auto: int
        mode: int
        state: int
        LightingSchedule: _JSONDict
        wlAiDetectType: _JSONDict

    class Keys(Protocol):
        """Keys"""

        brightness: Final = "bright"
        auto_mode: Final = "auto"
        brightness_state: Final = "mode"
        state: Final = "state"
        lighting_schedule: Final = "LightingSchedule"
        ai_detection_type: Final = "wlAiDetectType"

    __slots__ = ()

    __get_value__: providers.FactoryValue[JSON]

    @property
    def brightness(self):
        _default = 0
        return (
            value.get(self.Keys.brightness, _default)
            if (value := self.__get_value__())
            else _default
        )

    @property
    def auto_mode(self):
        return (
            True if (value := self.__get_value__()) and value.get(self.Keys.auto_mode, 0) else False
        )

    @property
    def brightness_state(self):
        _default = 0
        return (
            value.get(self.Keys.brightness_state, _default)
            if (value := self.__get_value__())
            else _default
        )

    @property
    def state(self):
        return True if (value := self.__get_value__()) and value.get(self.Keys.state, 0) else False

    @property
    def lighting_schedule(self):
        return LightingSchedule(
            self.lookup_factory(self.__get_value__, self.Keys.lighting_schedule, default=None)
        )

    @property
    def ai_detection_type(self):
        return AITypesMap(
            self.lookup_factory(self.__get_value__, self.Keys.ai_detection_type, default=None)
        )


class MutableWhiteLedInfo(WhiteLedInfo):
    """White Led Info"""

    __slots__ = ()

    def __default_factory__(self, create=False):
        if not create:
            return None
        value = {}
        if self is not None and not isinstance(self, type):
            self.__set_value__(value)
        return value

    @WhiteLedInfo.brightness.setter
    def brightness(self, value):
        self.__get_value__(True)[self.Keys.brightness] = int(value)

    @WhiteLedInfo.auto_mode.setter
    def auto_mode(self, value):
        self.__get_value__(True)[self.Keys.auto_mode] = int(bool(value))

    @WhiteLedInfo.brightness_state.setter
    def brightness_state(self, value):
        self.__get_value__(True)[self.Keys.brightness_state] = int(value)

    @WhiteLedInfo.state.setter
    def state(self, value):
        self.__get_value__(True)[self.Keys.state] = int(bool(value))

    @property
    def lighting_schedule(self):
        return MutableLightingSchedule(
            self.lookup_factory(
                self.__get_value__,
                self.Keys.lighting_schedule,
                default_factory=MutableLightingSchedule.__default_factory__.__get__(type),
            )
        )

    @lighting_schedule.setter
    def lighting_schedule(self, value: led_typing.LightingSchedule):
        self.lighting_schedule.update(value)

    @property
    def ai_detection_type(self):
        return MutableAITypesMap(
            self.lookup_factory(
                self.__get_value__,
                self.Keys.ai_detection_type,
                default_factory=MutableAITypesMap.__default_factory__.__get__(type),
            )
        )

    @ai_detection_type.setter
    def ai_detection_type(self, value):
        self.ai_detection_type.update(value)

    def update(self, value: led_typing.WhiteLedInfo):
        if isinstance(value, WhiteLedInfo):
            if not (_d := value.__get_value__()):
                return
            copy.update(self.__get_value__(True), _d)
            return
        try:
            self.auto_mode = value.auto_mode
        except AttributeError:
            pass
        try:
            self.ai_detection_type.update(value.ai_detection_type)
        except AttributeError:
            pass
        try:
            self.brightness = value.brightness
        except AttributeError:
            pass
        try:
            self.brightness_state = value.brightness_state
        except AttributeError:
            pass
        try:
            self.lighting_schedule.update(value.lighting_schedule)
        except AttributeError:
            pass
        try:
            self.state = value.state
        except AttributeError:
            pass
