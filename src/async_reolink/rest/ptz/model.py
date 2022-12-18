"""REST PTZ Models"""

from typing import (
    Final,
    MutableSequence,
    Protocol,
    Sequence,
    TypedDict,
)
from async_reolink.api.ptz import typing as ptz_typing

from .._utilities import providers

from .. import model

# pylint: disable=missing-function-docstring


class PositionJSON(TypedDict):
    """Position JSON"""

    pos: int


class PositionKeys(Protocol):
    """Position Keys"""

    position: Final = "pos"


class ZoomFocus(providers.DictProvider[str, any], ptz_typing.ZoomFocus):
    """REST PTZ Zoom/Focus"""

    class JSON(TypedDict):
        """JSON"""

        focus: PositionJSON
        zoom: PositionJSON

    class Keys(Protocol):
        """Keys"""

        focus: Final = "focus"
        zoom: Final = "zoom"

    __slots__ = ()

    _provided_value: JSON

    @property
    def focus(self):
        if (value := self._provided_value) and (pos := value.get(self.Keys.focus)):
            return pos.get(PositionKeys.position, 0)
        return 0

    @property
    def zoom(self):
        if (value := self._provided_value) and (pos := value.get(self.Keys.zoom)):
            return pos.get(PositionKeys.position, 0)
        return 0


class Preset(providers.DictProvider[str, any], ptz_typing.Preset):
    """REST PTZ Preset"""

    class JSON(TypedDict):
        """JSON"""

        id: int
        enable: int
        name: str

    class Keys(Protocol):
        """Keys"""

        id: Final = "id"
        enabled: Final = "enable"
        name: Final = "name"

    __slots__ = ()

    _provided_value: JSON

    @property
    def id(self):  # pylint: disable=invalid-name
        if value := self._provided_value:
            return value.get(self.Keys.id, 0)
        return 0

    @property
    def enabled(self):
        return (
            True if (value := self._provided_value) and value.get(self.Keys.enabled, 0) else False
        )

    @property
    def name(self):
        if value := self._provided_value:
            return value.get(self.Keys.name, "")
        return ""


class MutablePreset(Preset):
    """Mutable PTZ Preset"""

    __slots__ = ()

    def _get_provided_value(self, create=False):
        if (value := super()._get_provided_value(create)) or not create:
            return value
        value = {}
        self._set_provided_value(value)
        return value

    @Preset.id.setter
    def id(self, value):
        self._get_provided_value(True)[self.Keys.id] = int(value)

    @Preset.enabled.setter
    def enabled(self, value):
        self._get_provided_value(True)[self.Keys.enabled] = int(value)

    @Preset.name.setter
    def name(self, value):
        self._get_provided_value(True)[self.Keys.name] = str(value)

    def update(self, value: ptz_typing.Preset):
        if isinstance(value, Preset):
            if _d := value._provided_value:
                self._get_provided_value(True).update(_d)
            return
        try:
            self.name = value.name
        except AttributeError:
            pass
        try:
            self.channel_id = value.channel_id
        except AttributeError:
            pass
        try:
            self.id = value.id
        except AttributeError:
            pass
        try:
            self.enabled = value.enabled
        except AttributeError:
            pass


class PatrolPreset(providers.DictProvider[str, any], ptz_typing.PatrolPreset):
    """REST PTZ Patrol Preset"""

    class JSON(TypedDict):
        """JSON"""

        dwellTime: int
        preset_id: int
        speed: int

    class Keys(Protocol):
        """Keys"""

        dwell_time: Final = "dwellTime"
        preset_id: Final = "preset_id"
        speed: Final = "speed"

    __slots__ = ()

    _provided_value: JSON

    @property
    def preset_id(self) -> int:
        if value := self._provided_value:
            return value.get(self.Keys.preset_id, 0)
        return 0

    @property
    def dwell_time(self):
        if value := self._provided_value:
            return value.get(self.Keys.dwell_time, 0)
        return 0

    @property
    def speed(self):
        if value := self._provided_value:
            return value.get(self.Keys.speed, 0)
        return 0


class MutablePatrolPreset(PatrolPreset):
    """REST Mutable PTZ Patrol Preset"""

    __slots__ = ()

    def _get_provided_value(self, create=False):
        if (value := super()._get_provided_value(create)) or not create:
            return value
        value = {}
        self._set_provided_value(value)
        return value

    @PatrolPreset.preset_id.setter
    def preset_id(self, value):
        self._get_provided_value(True)[self.Keys.preset_id] = int(value)

    @PatrolPreset.dwell_time.setter
    def dwell_time(self, value):
        self._get_provided_value(True)[self.Keys.dwell_time] = int(value)

    @PatrolPreset.speed.setter
    def speed(self, value):
        self._get_provided_value(True)[self.Keys.speed] = int(value)

    def update(self, value: ptz_typing.PatrolPreset):
        if isinstance(value, PatrolPreset):
            if _d := value._provided_value:
                self._get_provided_value(True).update(_d)
            return
        try:
            self.dwell_time = value.dwell_time
        except AttributeError:
            pass
        try:
            self.preset_id = value.preset_id
        except AttributeError:
            pass
        try:
            self.speed = value.speed
        except AttributeError:
            pass


class _PatrolPresets(providers.ListProvider[dict[str, any]], Sequence[PatrolPreset]):
    __slots__ = ()

    def __getitem__(self, __k: int):
        return PatrolPreset(lambda _: self._get_index_value(self._get_provided_value, __k))

    def __len__(self) -> int:
        if (value := self._provided_value) is None:
            return 0
        return len(value)


class _MutablePatrolPresets(_PatrolPresets, MutableSequence[MutablePatrolPreset]):
    __slots__ = ()

    def _get_provided_value(self, create=False):
        if (value := super()._get_provided_value(create)) or not create:
            return value
        value = []
        self._set_provided_value(value)
        return value

    def __getitem__(self, __k: int):
        return MutablePatrolPreset(
            lambda create: self._get_index_value(
                self._get_provided_value, __k, create, lambda: dict() if create else None
            )
        )

    def __setitem__(self, __k: int, __v: ptz_typing.PatrolPreset):
        if not isinstance(__v, PatrolPreset):
            value = MutablePatrolPreset()
            value.update(__v)
            __v = value
        _d = __v._get_provided_value(True)
        if _d is None:
            _d = {}
        self._get_provided_value(True)[__k] = _d

    def append(self, value: ptz_typing.PatrolPreset) -> None:
        self[len(self)] = value

    def insert(self, index: int, value: ptz_typing.PatrolPreset):
        if (__list := self._get_provided_value(True)) is None:
            raise AttributeError()
        if not isinstance(value, PatrolPreset):
            __provided_value = MutablePatrolPreset()
            __provided_value.update(value)
            value = __provided_value
        _d = value._get_provided_value(True)
        if _d is None:
            _d = {}
        __list.insert(index, _d)

    def clear(self) -> None:
        if _l := self._provided_value:
            _l.clear()

    def update(self, value: Sequence[ptz_typing.PatrolPreset]):
        if not (_u := self._get_provided_value(True)):
            return
        if isinstance(value, _PatrolPresets):
            if _l := value._provided_value:
                _u[:] = _l[:]
            return
        for i, _p in enumerate(value):
            if isinstance(_p, PatrolPreset):
                if not (_d := _p._get_provided_value(True)):
                    _d = {}
                _u[i] = _d
                continue
            try:
                if _u[i] is None:
                    _u[i] = {}
            except IndexError:
                _u[i] = {}
            MutablePatrolPreset(lambda _: _u[i]).update(_p)
        i = len(value)
        if len(_u) > i:
            del _u[i:]


class Patrol(providers.DictProvider[str, any], ptz_typing.Patrol):
    """REST PTZ Patrol"""

    class JSON(Preset.JSON):
        """JSON"""

        preset: list[PatrolPreset.JSON]
        running: int

    class Keys(Preset.Keys, Protocol):
        """Keys"""

        presets: Final = "preset"
        running: Final = "running"

    __slots__ = ()

    _provided_value: JSON

    @property
    def id(self):  # pylint: disable=invalid-name
        if value := self._provided_value:
            return value.get(self.Keys.id, 0)
        return 0

    @property
    def enabled(self):
        return (
            True if (value := self._provided_value) and value.get(self.Keys.enabled, 0) else False
        )

    @property
    def name(self):
        if value := self._provided_value:
            return value.get(self.Keys.name, "")
        return ""

    def _get_presets(self, create=False) -> list[dict[str, any]]:
        return self._get_key_value(self._get_provided_value, self.Keys.presets, default=None)

    @property
    def presets(self):
        return _PatrolPresets(self._get_presets)

    @property
    def running(self):
        return (
            True if (value := self._provided_value) and value.get(self.Keys.running, 0) else False
        )


class MutablePatrol(Patrol):
    """Mutable REST PTZ Patrol"""

    __slots__ = ()

    def _get_provided_value(self, create=False):
        if (value := super()._get_provided_value(create)) is not None or not create:
            return value
        value = {}
        self._set_provided_value(value)
        return value

    @Patrol.id.setter
    def id(self, value):
        self._get_provided_value(True)[self.Keys.id] = int(value)

    @Patrol.enabled.setter
    def enabled(self, value):
        self._get_provided_value(True)[self.Keys.enabled] = int(value)

    @Patrol.name.setter
    def name(self, value):
        self._get_provided_value(True)[self.Keys.name] = str(value)

    def _get_presets(self, create=False) -> list[dict[str, any]]:
        return self._get_key_value(
            self._get_provided_value, self.Keys.presets, create, lambda: list() if create else None
        )

    @property
    def presets(self):
        return _MutablePatrolPresets(self._get_presets)

    @presets.setter
    def presets(self, value):
        self.presets.update(value)

    @Patrol.running.setter
    def running(self, value):
        self._get_provided_value(True)[self.Keys.running] = int(value)

    def update(self, value: ptz_typing.Patrol):
        if isinstance(value, Patrol):
            if _d := value._provided_value:
                self._get_provided_value(True).update(_d)
            return
        try:
            self.id = value.id
        except AttributeError:
            pass
        try:
            self.enabled = value.enabled
        except AttributeError:
            pass
        try:
            self.name = value.name
        except AttributeError:
            pass
        try:
            self.running = value.running
        except AttributeError:
            pass
        try:
            self.presets.update(value.presets)
        except AttributeError:
            pass


class Track(providers.DictProvider[str, any], ptz_typing.Track):
    """REST Track (Tattern)"""

    class JSON(Preset.JSON):
        """JSON"""

        running: int

    class Keys(Preset.Keys, Protocol):
        """Keys"""

        running: Final = "running"

    __slots__ = ()

    _provided_value: JSON

    @property
    def id(self):  # pylint: disable=invalid-name
        if value := self._provided_value:
            return value.get(self.Keys.id, 0)
        return 0

    @property
    def enabled(self):
        return (
            True if (value := self._provided_value) and value.get(self.Keys.enabled, 0) else False
        )

    @property
    def name(self):
        if value := self._provided_value:
            return value.get(self.Keys.name, "")
        return ""

    @property
    def running(self):
        return (
            True if (value := self._provided_value) and value.get(self.Keys.running, 0) else False
        )


class MutableTrack(Track):
    """Mutable REST Track (Tattern)"""

    __slots__ = ()

    def _get_provided_value(self, create=False):
        if (value := super()._get_provided_value(create)) is not None or not create:
            return value
        value = {}
        self._set_provided_value(value)
        return value

    @Patrol.id.setter
    def id(self, value):
        self._get_provided_value(True)[self.Keys.id] = int(value)

    @Patrol.enabled.setter
    def enabled(self, value):
        self._get_provided_value(True)[self.Keys.enabled] = int(value)

    @Patrol.name.setter
    def name(self, value):
        self._get_provided_value(True)[self.Keys.name] = str(value)

    @Patrol.running.setter
    def running(self, value):
        self._get_provided_value(True)[self.Keys.running] = int(value)

    def update(self, value: ptz_typing.Track):
        if isinstance(value, Track):
            if _d := value._provided_value:
                self._get_provided_value(True).update(_d)
            return
        try:
            self.id = value.id
        except AttributeError:
            pass
        try:
            self.enabled = value.enabled
        except AttributeError:
            pass
        try:
            self.name = value.name
        except AttributeError:
            pass
        try:
            self.running = value.running
        except AttributeError:
            pass
