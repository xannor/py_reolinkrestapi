"""LED Models"""

from typing import Callable, Final
from async_reolink.api.led import typing
from async_reolink.api.typing import PercentValue, SimpleTime as SimpleTimeType
from async_reolink.api.model import SimpleTime

from .. import model
from ..typing import FactoryValue

from ..ai.model import AITypesMap, MutableAITypesMap

# pylint: disable=missing-function-docstring


class LightingSchedule(typing.LightingSchedule):
    """Lighting Schedule"""

    __slots__ = ("_factory",)

    _START_PFX: Final = "Start"
    _END_PFX: Final = "End"

    def __init__(self, factory: Callable[[], dict]) -> None:
        super().__init__()
        self._factory = factory

    @property
    def start(self):
        return model.SimpleTime(self._factory, self._START_PFX)

    @property
    def end(self):
        return model.SimpleTime(self._factory, self._END_PFX)

    def _copy(self):
        _s = self.start._copy()
        _e = self.end._copy()
        if not _s and not _e:
            return None
        if _s and _e:
            return _s.update(_e)
        if _s:
            return _s
        return _e


class MutableLightingSchedule(LightingSchedule):
    """Mutable Lighting schedule"""

    def __init__(self, factory: FactoryValue[dict]) -> None:
        super().__init__(factory)
        self._factory = factory

    @property
    def start(self):
        return model.MutableSimpleTime(self._factory, self._START_PFX)

    @start.setter
    def start(self, value):
        self.start.update(value)

    @property
    def end(self):
        return model.MutableSimpleTime(self._factory, self._END_PFX)

    @end.setter
    def end(self, value):
        self.end.update(value)

    def update(self, value: typing.LightingSchedule):
        if isinstance(value, LightingSchedule):
            if (_d := value._copy()) and (_u := self._factory(True)):
                _u.update(_d)
            return
        try:
            self.start = value.start
        except AttributeError:
            pass
        try:
            self.end = value.end
        except AttributeError:
            pass


class WhiteLedInfo(typing.WhiteLedInfo):
    """White Led Info"""

    _BRIGHT_KEY: Final = "bright"
    _AUTO_KEY: Final = "auto"
    _MODE_KEY: Final = "mode"
    _STATE_KEY: Final = "state"
    _SCHED_KEY: Final = "LightingSchedule"
    _AI_KEY: Final = "wlAiDetectType"

    __slots__ = ("_factory",)

    def __init__(self, factory: Callable[[], dict]) -> None:
        super().__init__()
        self._factory = factory

    @property
    def brightness(self) -> PercentValue:
        if (value := self._factory()) is None:
            return 100
        return value.get(self._BRIGHT_KEY, 100)

    @property
    def auto_mode(self) -> bool:
        if (value := self._factory()) is None:
            return 0
        return value.get(self._AUTO_KEY, 0)

    @property
    def brightness_state(self) -> int:
        if (value := self._factory()) is None:
            return 0
        return value.get(self._MODE_KEY, 0)

    @property
    def state(self) -> bool:
        if (value := self._factory()) is None:
            return 0
        return value.get(self._STATE_KEY, 0)

    def _get_sched(self) -> dict:
        if (value := self._factory()) is None:
            return None
        return value.get(self._SCHED_KEY, None)

    @property
    def lighting_schedule(self):
        return LightingSchedule(self._get_sched)

    def _get_ai(self) -> dict:
        if (value := self._factory()) is None:
            return None
        return value.get(self._AI_KEY, None)

    @property
    def ai_detection_type(self):
        return AITypesMap(self._get_ai)

    def _copy(self):
        if not (_d := self._factory()):
            return None
        _d = _d.copy()
        if _d2 := self.lighting_schedule._copy():
            _d[self._SCHED_KEY] = _d2
        if _d2 := self.ai_detection_type._copy():
            _d[self._AI_KEY] = _d2
        return _d


class MutableWhiteLedInfo(WhiteLedInfo):
    """White Led Info"""

    def __init__(self, factory: FactoryValue[dict]) -> None:
        super().__init__(factory)
        self._factory = factory

    @WhiteLedInfo.brightness.setter
    def brightness(self, value):
        if (_d := self._factory(True)) is not None:
            _d[self._BRIGHT_KEY] = int(value)

    @WhiteLedInfo.auto_mode.setter
    def auto_mode(self, value):
        if (_d := self._factory(True)) is not None:
            _d[self._AUTO_KEY] = int(value)

    @WhiteLedInfo.brightness_state.setter
    def brightness_state(self, value):
        if (_d := self._factory(True)) is not None:
            _d[self._MODE_KEY] = int(value)

    @WhiteLedInfo.state.setter
    def state(self, value):
        if (_d := self._factory(True)) is not None:
            _d[self._STATE_KEY] = int(value)

    def _get_sched(self, create=False) -> dict:
        if not create:
            return super()._get_sched()
        if (value := self._factory(True)) is None:
            return None
        return value.setdefault(self._SCHED_KEY, {})

    @property
    def lighting_schedule(self):
        return MutableLightingSchedule(self._get_sched)

    @lighting_schedule.setter
    def lighting_schedule(self, value: typing.LightingSchedule):
        self.lighting_schedule.update(value)

    def _get_ai(self, create=False) -> dict:
        if not create:
            return super()._get_ai()
        if (value := self._factory(True)) is None:
            return None
        return value.setdefault(self._AI_KEY, {})

    @property
    def ai_detection_type(self):
        return MutableAITypesMap(self._get_ai)

    @ai_detection_type.setter
    def ai_detection_type(self, value):
        self.ai_detection_type.update(value)

    def update(self, value: typing.WhiteLedInfo):
        if isinstance(value, WhiteLedInfo):
            if (_d := value._copy()) and (_u := self._factory(True)):
                _u.update(_d)
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
