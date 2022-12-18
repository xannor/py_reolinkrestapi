"""LED Models"""

from typing import Callable, Final, Protocol, TypedDict
from async_reolink.api.led import typing as led_typing
from async_reolink.api.typing import PercentValue, SimpleTime as SimpleTimeType
from async_reolink.api.model import SimpleTime

from .._utilities import providers

from .. import model

from ..ai.model import AITypesMap, MutableAITypesMap

# pylint: disable=missing-function-docstring


class LightingSchedule(providers.DictProvider[str, any], led_typing.LightingSchedule):
    """Lighting Schedule"""

    __slots__ = ()

    _START_PREFIX: Final = "Start"
    _END_PREFIX: Final = "End"

    @property
    def start(self):
        return model.SimpleTime(self._provided_value, self._START_PREFIX)

    @property
    def end(self):
        return model.SimpleTime(self._provided_value, self._END_PREFIX)


class MutableLightingSchedule(LightingSchedule):
    """Mutable Lighting schedule"""

    @property
    def start(self):
        return model.MutableSimpleTime(self._get_value, self._START_PREFIX)

    @start.setter
    def start(self, value):
        self.start.update(value)

    @property
    def end(self):
        return model.MutableSimpleTime(self._get_value, self._END_PREFIX)

    @end.setter
    def end(self, value):
        self.end.update(value)

    def update(self, value: led_typing.LightingSchedule):
        if isinstance(value, LightingSchedule):
            if _d := value._provided_value:
                self._get_value(True).update(_d)
            return
        try:
            self.start = value.start
        except AttributeError:
            pass
        try:
            self.end = value.end
        except AttributeError:
            pass


class WhiteLedInfo(providers.DictProvider[str, any], led_typing.WhiteLedInfo):
    """White Led Info"""

    class JSON(TypedDict):
        """JSON"""

        bright: int
        auto: int
        mode: int
        state: int
        LightingSchedule: dict
        wlAiDetectType: dict

    class Keys(Protocol):
        """Keys"""

        brightness: Final = "bright"
        auto_mode: Final = "auto"
        brightness_state: Final = "mode"
        state: Final = "state"
        lighting_schedule: Final = "LightingSchedule"
        ai_detection_type: Final = "wlAiDetectType"

    __slots__ = ()

    _provided_value: JSON

    @property
    def brightness(self):
        if value := self._provided_value:
            return value.get(self.Keys.brightness)
        return None

    @property
    def auto_mode(self):
        return (
            True if (value := self._provided_value) and value.get(self.Keys.auto_mode, 0) else False
        )

    @property
    def brightness_state(self):
        if value := self._provided_value:
            return value.get(self.Keys.brightness_state, 0)
        return 0

    @property
    def state(self):
        return True if (value := self._provided_value) and value.get(self.Keys.state, 0) else False

    def _get_lighting_schedule(self, create=False) -> dict:
        if value := self._get_value(create):
            return value.get(self.Keys.lighting_schedule)
        return None

    _lighting_schedule: dict = property(_get_lighting_schedule)

    @property
    def lighting_schedule(self):
        return LightingSchedule(self._get_lighting_schedule)

    def _get_ai_detection_type(self, create=False) -> dict:
        if value := self._get_value(create):
            return value.get(self.Keys.ai_detection_type)
        return None

    _ai_detection_type: dict = property(_get_ai_detection_type)

    @property
    def ai_detection_type(self):
        return AITypesMap(self._get_ai_detection_type)


class MutableWhiteLedInfo(WhiteLedInfo):
    """White Led Info"""

    __slots__ = ()

    def _get_value(self, create=False):
        if (value := super()._get_value(create)) or not create:
            return value
        value = {}
        self._set_value(value)
        return value

    @WhiteLedInfo.brightness.setter
    def brightness(self, value):
        self._get_value(True)[self.Keys.brightness] = int(value)

    @WhiteLedInfo.auto_mode.setter
    def auto_mode(self, value):
        self._get_value(True)[self.Keys.auto_mode] = int(bool(value))

    @WhiteLedInfo.brightness_state.setter
    def brightness_state(self, value):
        self._get_value(True)[self.Keys.brightness_state] = int(value)

    @WhiteLedInfo.state.setter
    def state(self, value):
        self._get_value(True)[self.Keys.state] = int(bool(value))

    def _get_lighting_schedule(self, create=False) -> dict:
        if (value := super()._get_lighting_schedule(create)) or not create:
            return value
        return self._get_value(True).setdefault(self.Keys.lighting_schedule, {})

    @property
    def lighting_schedule(self):
        return MutableLightingSchedule(self._get_lighting_schedule)

    @lighting_schedule.setter
    def lighting_schedule(self, value: led_typing.LightingSchedule):
        self.lighting_schedule.update(value)

    def _get_ai_detection_type(self, create=False) -> dict:
        if (value := super()._get_ai_detection_type(create)) or not create:
            return value
        return self._get_value(True).setdefault(self.Keys.ai_detection_type, {})

    @property
    def ai_detection_type(self):
        return MutableAITypesMap(self._get_ai_detection_type)

    @ai_detection_type.setter
    def ai_detection_type(self, value):
        self.ai_detection_type.update(value)

    def update(self, value: led_typing.WhiteLedInfo):
        if isinstance(value, WhiteLedInfo):
            if not (_d := value._provided_value):
                return
            for _k in (self.Keys.ai_detection_type, self.Keys.lighting_schedule):
                if _k in _d:
                    _d[_k] = _d[_k].copy()

            self._get_value(True).update(_d)
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
