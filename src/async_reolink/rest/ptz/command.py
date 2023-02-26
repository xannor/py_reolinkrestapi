"""REST PTZ Commands"""

from typing import (
    TYPE_CHECKING,
    Callable,
    Final,
    Iterable,
    MutableSequence,
    Protocol,
    TypeAlias,
    TypedDict,
    cast,
)
from async_reolink.api.ptz import command as ptz
from async_reolink.api.ptz import typing as ptz_typing

from .._utilities.providers import value as providers
from .._utilities.dictlist import DictList

from .. import model

from ..ptz.typing import operation_str, zoom_operation_str

from . import model as local_model

from ..connection.model import (
    ChannelJSON,
    ChannelKeys,
    Request,
    RequestWithChannel,
    Response as RestCommandResponse,
    ResponseTypes,
)

# pylint:disable=missing-function-docstring

_JSONDict: TypeAlias = dict[str, any]


class GetPresetRequest(RequestWithChannel, ptz.GetPresetRequest):
    """REST Get Presets Request"""

    __slots__ = ()

    COMMAND: Final = "GetPtzPreset"
    _COMMAND_ID: Final = hash(COMMAND)

    def __init__(self, /, channel_id: int = ..., response_type: ResponseTypes = ...):
        super().__init__(
            command=type(self).COMMAND, channel_id=channel_id, response_type=response_type
        )

    @property
    def id(self):
        return self._COMMAND_ID ^ self.channel_id


class _PresetRange(providers.Value[_JSONDict]):
    class JSON(TypedDict):
        """JSON"""

        id: model.MinMaxRange.JSON
        name: model.StringRange.JSON

    class Keys(local_model.Preset.Keys):
        """Keys"""

    __get_value__: providers.FactoryValue[JSON]

    __slots__ = ()

    @property
    def id(self):
        return model.MinMaxRange(
            self.lookup_factory(self.__get_value__, self.Keys.id, default=None)
        )

    @property
    def name(self):
        return model.StringRange(
            self.lookup_factory(self.__get_value__, self.Keys.name, default=None)
        )


class GetPresetResponse(RestCommandResponse, ptz.GetPresetResponse):
    """Get Presets Response"""

    @classmethod
    def from_response(cls, response: any, /, request: Request | None = None, **kwargs):
        if super().is_response(response, GetPresetRequest.COMMAND):
            return cls(response, request_id=request.id if request else None, **kwargs)
        return None

    __slots__ = ()

    class Value(Protocol):
        """Protocol"""

        class Preset(Protocol):
            """Preset"""

            class JSON(ChannelJSON, local_model.Preset.JSON):
                """JSON"""

            class Keys(ChannelKeys, local_model.Preset.Keys, Protocol):
                """Keys"""

        class JSON(TypedDict):
            """JSON"""

            PtzPreset: list["GetPresetResponse.Value.Preset.JSON"]

        class Keys(Protocol):
            """Keys"""

            presets: Final = "PtzPreset"

    _value: Value.JSON

    @property
    def _presets(self):
        return value.get(self.Value.Keys.presets) if (value := self._value) else None

    @property
    def channel_id(self):
        if (_l := self._presets) and (value := next(iter(_l), None)):
            return value.get(self.Value.Preset.Keys.channel_id, 0)
        return 0

    @property
    def presets(self) -> DictList[int, local_model.Preset]:
        return DictList(self.Value.Preset.Keys.id, self._presets, local_model.Preset)

    @property
    def _initial_presets(self):
        return value.get(self.Value.Keys.presets) if (value := self._initial) else None

    @property
    def initial_presets(self):
        return local_model.Preset(lambda _: self._initial_presets)

    @property
    def _presets_range(self):
        return value.get(self.Value.Keys.presets) if (value := self._range) else None

    @property
    def presets_range(self):
        return _PresetRange(self._presets_range)


class SetPresetRequest(Request, ptz.SetPresetRequest):
    """Set Preset Request"""

    class Parameter(Protocol):
        """Parameter"""

        class Preset(GetPresetResponse.Value.Preset, Protocol):
            """Preset"""

        class JSON(TypedDict):
            """JSON"""

            PtzPreset: "SetPresetRequest.Parameter.Preset.JSON"

        class Keys(Protocol):
            """Keys"""

            preset: Final = GetPresetResponse.Value.Keys.presets

    __slots__ = ()

    COMMAND: Final = "SetPtzPreset"
    _COMMAND_ID: Final = hash(COMMAND)

    def __init__(
        self,
        /,
        preset: ptz_typing.Preset = ...,
        channel_id: int = ...,
        response_type: ResponseTypes = ...,
    ):
        super().__init__(
            command=type(self).COMMAND, channel_id=channel_id, response_type=response_type
        )
        if preset and preset is not ...:
            self.preset = preset

    def __init__(
        self,
        channel_id: int = 0,
        response_type: ResponseTypes = ResponseTypes.VALUE_ONLY,
    ):
        super().__init__()
        self.command = type(self).COMMAND
        self.response_type = response_type
        self.channel_id = channel_id

    @property
    def id(self):
        return self._COMMAND_ID ^ self.channel_id

    _get_parameter: providers.FactoryValue[Parameter.JSON]
    _parameter: Parameter.JSON

    def _get_preset(self, create=False) -> Parameter.Preset.JSON:
        return self._get_key_value(
            self._get_parameter,
            self.Parameter.Keys.preset,
            create,
            lambda: dict() if create else None,
        )

    @property
    def _preset(self):
        return self._get_preset()

    @property
    def channel_id(self):
        if value := self._preset:
            return value.get(self.Parameter.Preset.Keys.channel_id, 0)
        return 0

    @channel_id.setter
    def channel_id(self, value):
        self._get_preset(True)[self.Parameter.Preset.Keys.channel_id] = int(value)

    @property
    def preset(self):
        return local_model.MutablePreset(self._get_preset)

    @preset.setter
    def preset(self, value):
        self.preset.update(value)


class GetPatrolRequest(RequestWithChannel, ptz.GetPatrolRequest):
    """Get Patrol"""

    __slots__ = ()

    COMMAND: Final = "GetPtzPatrol"
    _COMMAND_ID: Final = hash(COMMAND)

    @property
    def id(self):
        return self._COMMAND_ID ^ self.channel_id

    def __init__(self, /, channel_id: int = ..., response_type: ResponseTypes = ...):
        super().__init__(
            command=type(self).COMMAND, channel_id=channel_id, response_type=response_type
        )


class _PatrolPresetRange(providers.Value[_JSONDict]):
    class JSON(TypedDict):
        """JSON"""

        id: model.MinMaxRange.JSON
        dwellTime: model.MinMaxRange.JSON
        speed: model.MinMaxRange.JSON

    class Keys(Protocol):
        """Keys"""

        id: Final = "id"
        dwell_time: Final = "dwellTime"
        speed: Final = "speed"

    __slots__ = ()

    __get_value__: providers.FactoryValue[JSON]

    @property
    def id(self):
        return model.MinMaxRange(
            self.lookup_factory(self.__get_value__, self.Keys.id, default=None)
        )

    @property
    def dwell_time(self):
        return model.MinMaxRange(
            self.lookup_factory(self.__get_value__, self.Keys.dwell_time, default=None)
        )

    @property
    def speed(self):
        return model.MinMaxRange(
            self.lookup_factory(self.__get_value__, self.Keys.speed, default=None)
        )


class _PatrolRange(providers.Value[_JSONDict]):
    class JSON(TypedDict):
        """JSON"""

        id: model.MinMaxRange.JSON
        name: model.StringRange.JSON
        preset: _PatrolPresetRange.JSON

    class Keys(Protocol):
        """Keys"""

        id: Final = "id"
        name: Final = "name"
        preset: Final = "preset"

    __slots__ = ()

    __get_value__: providers.FactoryValue[JSON]

    @property
    def id(self):
        return model.MinMaxRange(
            self.lookup_factory(self.__get_value__, self.Keys.id, default=None)
        )

    @property
    def name(self):
        return model.StringRange(
            self.lookup_factory(self.__get_value__, self.Keys.name, default=None)
        )

    @property
    def preset(self):
        return _PatrolPresetRange(
            self.lookup_factory(self.__get_value__, self.Keys.preset, default=None)
        )


class GetPatrolResponse(RestCommandResponse, ptz.GetPatrolResponse):
    """Get Patrol Response"""

    @classmethod
    def from_response(cls, response: any, /, request: Request | None = None, **kwargs):
        if super().is_response(response, GetPatrolRequest.COMMAND):
            return cls(response, request_id=request.id if request else None, **kwargs)
        return None

    class Value(Protocol):
        """Value"""

        class Patrol(Protocol):
            """Patrol"""

            class JSON(ChannelJSON, local_model.Patrol.JSON):
                """JSON"""

            class Keys(ChannelKeys, local_model.Patrol.Keys, Protocol):
                """Keys"""

        class JSON(TypedDict):
            """JSON"""

            PtzPatrol: list["GetPatrolResponse.Value.Patrol.JSON"]

        class Keys(Protocol):
            """Keys"""

            patrols: Final = "PtzPatrol"

    __slots__ = ()

    _get_value: providers.FactoryValue[Value.JSON]
    _value: Value.JSON

    def _get_patrols(self, create=False) -> list[Value.Patrol.JSON]:
        return self.lookup_value(
            self._get_value, self.Value.Keys.patrols, create=create, default=None
        )

    @property
    def _patrols(self):
        return self._get_patrols()

    @property
    def channel_id(self):
        if (_l := self._patrols) and (value := next(iter(_l), None)):
            return value.get(self.Value.Patrol.Keys.channel_id, 0)
        return 0

    @property
    def patrols(self) -> DictList[int, local_model.Patrol]:
        return DictList(self.Value.Patrol.Keys.id, self._get_patrols, local_model.Patrol)

    @property
    def initial_patrol(self):
        return local_model.Patrol(
            self.lookup_factory(self._get_initial, self.Value.Keys.patrols, default=None)
        )

    @property
    def patrol_range(self):
        return _PatrolRange(
            self.lookup_factory(self._get_range, self.Value.Keys.patrols, default=None)
        )


class SetPatrolRequest(Request, ptz.SetPatrolRequest):
    """Set  Patrol"""

    class Parameter(Protocol):
        """Parameter"""

        class Patrol(GetPatrolResponse.Value.Patrol, Protocol):
            """Patrol"""

        class JSON(TypedDict):
            """JSON"""

            PtzPatrol: "SetPatrolRequest.Parameter.Patrol.JSON"

        class Keys(Protocol):
            """Keys"""

            patrol: Final = GetPatrolResponse.Value.Keys.patrols

    __slots__ = ()

    COMMAND: Final = "SetPtzPatrol"
    _COMMAND_ID: Final = hash(COMMAND)

    def __init__(
        self,
        /,
        patrol: ptz_typing.Patrol = ...,
        channel_id: int = ...,
        response_type: ResponseTypes = ...,
    ):
        super().__init__(
            command=type(self).COMMAND, channel_id=channel_id, response_type=response_type
        )
        if patrol and patrol is not ...:
            self.patrol = patrol

    @property
    def id(self):
        return self._COMMAND_ID ^ self.channel_id

    _get_parameter: providers.FactoryValue[Parameter.JSON]
    _parameter: Parameter.JSON

    def _get_patrol(self, create=False) -> Parameter.Patrol.JSON:
        return self.lookup_value(
            self._get_parameter,
            self.Parameter.Keys.patrol,
            create=create,
            default_factory=lambda: dict() if create else None,
        )

    @property
    def _patrol(self):
        return self._get_patrol()

    @property
    def channel_id(self):
        if value := self._patrol:
            return value.get(self.Parameter.Patrol.Keys.channel_id, 0)
        return 0

    @channel_id.setter
    def channel_id(self, value):
        self._get_patrol(True)[self.Parameter.Patrol.Keys.channel_id] = int(value)

    @property
    def patrol(self):
        return local_model.MutablePatrol(self._get_patrol)

    @patrol.setter
    def patrol(self, value):
        self.patrol.update(value)


class GetTatternRequest(RequestWithChannel, ptz.GetTatternRequest):
    """Get Tattern"""

    __slots__ = ()

    COMMAND: Final = "GetPtzTattern"
    _COMMAND_ID: Final = hash(COMMAND)

    @property
    def id(self):
        return self._COMMAND_ID ^ self.channel_id

    def __init__(self, /, channel_id: int = ..., response_type: ResponseTypes = ...):
        super().__init__(
            command=type(self).COMMAND, channel_id=channel_id, response_type=response_type
        )


class _TrackRange(providers.Value[_JSONDict]):
    class JSON(TypedDict):
        """JSON"""

        id: model.MinMaxRange.JSON
        name: model.StringRange.JSON

    class Keys(Protocol):
        """Keys"""

        id: Final = "id"
        name: Final = "name"

    __slots__ = ()

    __get_value__: providers.FactoryValue[JSON]

    @property
    def id(self):
        return model.MinMaxRange(
            self.lookup_factory(self.__get_value__, self.Keys.id, default=None)
        )

    @property
    def name(self):
        return model.StringRange(
            self.lookup_factory(self.__get_value__, self.Keys.name, default=None)
        )


class _TracksRange(providers.Value[_JSONDict]):
    class JSON(TypedDict):
        """JSON"""

        track: _TrackRange.JSON

    class Keys(Protocol):
        """Keys"""

        track: Final = "track"

    __slots__ = ()

    __get_value__: providers.FactoryValue[JSON]

    @property
    def track(self):
        return _TrackRange(self.lookup_factory(self.__get_value__, self.Keys.track, default=None))


class GetTatternResponse(RestCommandResponse, ptz.GetTatternResponse):
    """Get Tattern Response"""

    @classmethod
    def from_response(cls, response: any, /, request: Request | None = None, **kwargs):
        if super().is_response(response, GetTatternRequest.COMMAND):
            return cls(response, request_id=request.id if request else None, **kwargs)
        return None

    class Value(Protocol):
        """Value"""

        class Tattern(Protocol):
            """Track"""

            class JSON(ChannelJSON):
                """JSON"""

                track: list[local_model.Track.JSON]

            class Keys(ChannelKeys, Protocol):
                """Keys"""

                tracks: Final = "track"

        class JSON(TypedDict):
            """JSON"""

            PtzTattern: "GetTatternResponse.Value.Tattern.JSON"

        class Keys(Protocol):
            """Keys"""

            tattern: Final = "PtzTattern"

    class Range(Protocol):
        """Range"""

        class Tattern(Protocol):
            """Tattern"""

            class JSON(TypedDict):
                """JSON"""

                track: _TrackRange.JSON

        class JSON(TypedDict):
            """JSON"""

            PtzTattern: "GetTatternResponse.Range.Tattern.JSON"

    __slots__ = ()

    _get_value: providers.FactoryValue[Value.JSON]
    _value: Value.JSON

    def _get_tattern(self, create=False) -> Value.Tattern.JSON:
        return self.lookup_value(
            self._get_value, self.Value.Keys.tattern, create=create, default=None
        )

    @property
    def _tattern(self):
        return self._get_tattern()

    @property
    def channel_id(self):
        if value := self._tattern:
            return value.get(self.Value.Tattern.Keys.channel_id, 0)
        return 0

    @property
    def tracks(self) -> DictList[int, local_model.Track]:
        return DictList(
            local_model.Track.Keys.id,
            self.lookup_factory(self._get_tattern, self.Value.Tattern.Keys.tracks, default=None),
            local_model.Track,
        )

    _get_initial: providers.FactoryValue[Value.JSON]
    _initial: Value.JSON

    @property
    def initial_tracks(self) -> DictList[int, local_model.Track]:
        return DictList(
            local_model.Track.Keys.id,
            self.lookup_factory(
                self.lookup_factory(self._get_initial, self.Value.Keys.tattern, default=None),
                self.Value.Tattern.Keys.tracks,
                default=None,
            ),
            local_model.Track,
        )

    _get_range: providers.FactoryValue[Range.JSON]
    _range: Range.JSON

    @property
    def tracks_range(self):
        return _TracksRange(
            self.lookup_factory(
                self.lookup_factory(self._get_range, self.Value.Keys.tattern, default=None),
                self.Value.Tattern.Keys.tracks,
                default=None,
            ),
        )


class _MutableTracks(providers.Value[list[_JSONDict]], MutableSequence[ptz_typing.Track]):
    __slots__ = ()

    def __default_factory__(self, create=False):
        if not create:
            return None
        value = []
        if self is not None and not isinstance(self, type):
            self.__set_value__(value)
        return value

    def __getitem__(self, __k: int):
        return local_model.MutableTrack(
            self.lookup_factory(
                self.__get_value__,
                __k,
                default_factory=local_model.MutableTrack.__default_factory__.__get__(type),
            )
        )

    def __setitem__(self, __k: int, __v: ptz_typing.Track):
        self.__getitem__(__k).update(__v)

    def __delitem__(self, __k: int):
        if _list := self.__get_value__():
            del _list[__k]

    def clear(self) -> None:
        if value := self.__get_value__():
            value.clear()

    def __len__(self) -> int:
        if value := self.__get_value__():
            return value.__len__()
        return 0


class SetTatternRequest(Request, ptz.SetTatternRequest):
    """Set PTZ Tattern"""

    class Parameter(GetTatternResponse.Value, Protocol):
        """Parameter"""

    __slots__ = ()

    COMMAND: Final = "SetPtzTattern"
    _COMMAND_ID: Final = hash(COMMAND)

    @property
    def id(self):
        return self._COMMAND_ID ^ self.channel_id

    def __init__(
        self,
        /,
        tracks: Iterable[ptz_typing.Track] = ...,
        channel_id: int = ...,
        response_type: ResponseTypes = ...,
    ):
        super().__init__(
            command=type(self).COMMAND, channel_id=channel_id, response_type=response_type
        )
        if tracks and tracks is not ...:
            self.tracks = tracks

    def _get_tattern(self, create=False) -> Parameter.Tattern.JSON:
        return self.lookup_value(
            self._get_parameter,
            self.Parameter.Keys.tattern,
            create=create,
            default_factory=lambda: dict() if create else None,
        )

    @property
    def _tattern(self):
        return self._get_tattern()

    def _get_tracks(self, create=False) -> list[local_model.Track.JSON]:
        return self.lookup_value(
            self._get_tattern,
            self.Parameter.Tattern.Keys.tracks,
            create=create,
            default_factory=lambda: list() if create else None,
        )

    @property
    def _tracks(self):
        return self._get_tracks()

    @GetTatternResponse.channel_id.setter
    def channel_id(self, value):
        self._get_tattern(True)[self.Parameter.Tattern.Keys.channel_id] = int(value)

    @property
    def tracks(self):
        return _MutableTracks(self._get_tracks)

    @tracks.setter
    def tracks(self, value: Iterable[ptz_typing.Track]):
        _tracks = self.tracks
        _tracks.clear()
        for track in value:
            _tracks.append(track)


class GetAutoFocusRequest(RequestWithChannel, ptz.GetAutoFocusRequest):
    """Get PTZ AutoFocus"""

    __slots__ = ()

    COMMAND: Final = "GetAutoFocus"
    _COMMAND_ID: Final = hash(COMMAND)

    @property
    def id(self):
        return self._COMMAND_ID ^ self.channel_id

    def __init__(self, /, channel_id: int = ..., response_type: ResponseTypes = ...):
        super().__init__(
            command=type(self).COMMAND, channel_id=channel_id, response_type=response_type
        )


class GetAutoFocusResponse(RestCommandResponse, ptz.GetAutoFocusResponse):
    """Get PTZ AutoFocus Response"""

    class Value(Protocol):
        """Value"""

        class AutoFocus(Protocol):
            """Auto Focus"""

            class JSON(ChannelJSON):
                """JSON"""

                disable: int

            class Keys(ChannelKeys, Protocol):
                """Keys"""

                disabled: Final = "disable"

        class JSON(TypedDict):
            """JSON"""

            AutoFocus: "GetAutoFocusResponse.Value.AutoFocus.JSON"

        class Keys(Protocol):
            """Keys"""

            info: Final = "AutoFocus"

    @classmethod
    def from_response(cls, response: any, /, request: Request | None = None, **kwargs):
        if super().is_response(response, GetAutoFocusRequest.COMMAND):
            return cls(response, request_id=request.id if request else None, **kwargs)
        return None

    __slots__ = ()

    _get_value: providers.FactoryValue[Value.JSON]
    _value: Value.JSON

    def _get_info(self, create=False) -> Value.AutoFocus.JSON:
        return self.lookup_value(self._get_value, self.Value.Keys.info, create=create, default=None)

    @property
    def _info(self):
        return self._get_info()

    @property
    def channel_id(self):
        if value := self._info:
            return value.get(self.Value.AutoFocus.Keys.channel_id, 0)
        return 0

    channel_id = GetTatternResponse.channel_id.setter(None)

    @property
    def disabled(self):
        return (
            True
            if (value := self._info) and value.get(self.Value.AutoFocus.Keys.disabled)
            else False
        )


class SetAutoFocusRequest(RequestWithChannel, ptz.SetAutoFocusRequest):
    """Set PTZ AutoFocus"""

    class Parameter(GetAutoFocusResponse.Value, Protocol):
        """Parameter"""

    __slots__ = ()

    COMMAND: Final = "AutoFocus"
    _COMMAND_ID: Final = hash(COMMAND)

    @property
    def id(self):
        return self._COMMAND_ID ^ self.channel_id

    def __init__(
        self, /, disabled: bool = ..., channel_id: int = ..., response_type: ResponseTypes = ...
    ):
        super().__init__(
            command=type(self).COMMAND, channel_id=channel_id, response_type=response_type
        )
        if disabled and disabled is not ...:
            self.disabled = disabled

    def _get_info(self, create=False) -> Parameter.AutoFocus.JSON:
        return self.lookup_value(
            self._get_parameter,
            self.Parameter.Keys.info,
            create=create,
            default_factory=lambda: dict() if create else None,
        )

    @property
    def _info(self):
        return self._get_info()

    @GetAutoFocusResponse.disabled.setter
    def disabled(self, value):
        self._get_info(True)[self.Parameter.AutoFocus.Keys.disabled] = int(bool(value))

    @GetAutoFocusResponse.channel_id.setter
    def channel_id(self, value):
        self._get_info(True)[self.Parameter.AutoFocus.Keys.channel_id] = int(value or 0)


class GetZoomFocusRequest(RequestWithChannel, ptz.GetZoomFocusRequest):
    """Get Zoom and Focus"""

    __slots__ = ()

    COMMAND: Final = "GetZoomFocus"
    _COMMAND_ID: Final = hash(COMMAND)

    @property
    def id(self):
        return self._COMMAND_ID ^ self.channel_id

    def __init__(self, /, channel_id: int = ..., response_type: ResponseTypes = ...):
        super().__init__(
            command=type(self).COMMAND, channel_id=channel_id, response_type=response_type
        )


class _ZoomFocusRange(providers.Value[_JSONDict]):
    class Position(Protocol):
        """Position"""

        class JSON(TypedDict):
            """JSON"""

            pos: model.MinMaxRange.JSON

        class Keys(Protocol):
            """Keys"""

            value: Final = "pos"

    class JSON(TypedDict):
        """JSON"""

        zoom: "_ZoomFocusRange.Position.JSON"
        focus: "_ZoomFocusRange.Position.JSON"

    class Keys(Protocol):
        """Keys"""

        zoom: Final = "zoom"
        focus: Final = "focus"

    __slots__ = ()

    __get_value__: providers.FactoryValue[JSON]

    def _make_get_pos(self, source: providers.FactoryValue[Position.JSON]):
        def factory(create=False) -> model.MinMaxRange.JSON:
            return self.lookup_value(source, self.Position.Keys.value, create=create, default=None)

        return factory

    def _get_zoom(self, create=False) -> Position.JSON:
        return self.lookup_value(self.__get_value__, self.Keys.zoom, create=create, default=None)

    @property
    def zoom(self):
        return model.MinMaxRange(self._make_get_pos(self._get_zoom))

    def _get_focus(self, create=False) -> Position.JSON:
        return self.lookup_value(self.__get_value__, self.Keys.focus, create=create, default=None)

    @property
    def focus(self):
        return model.MinMaxRange(self._make_get_pos(self._get_focus))


class GetZoomFocusResponse(RestCommandResponse, ptz.GetZoomFocusResponse):
    """Get Zoom/Focus Response"""

    @classmethod
    def from_response(cls, response: any, /, request: Request | None = None, **kwargs):
        if super().is_response(response, GetZoomFocusRequest.COMMAND):
            return cls(response, request_id=request.id if request else None, **kwargs)
        return None

    class Value(Protocol):
        """Value"""

        class ZoomFocus(Protocol):
            """Zoom/Focus"""

            class JSON(local_model.ZoomFocus.JSON, ChannelJSON):
                """JSON"""

            class Keys(local_model.ZoomFocus.Keys, ChannelKeys, Protocol):
                """Keys"""

        class JSON(TypedDict):
            """JSON"""

            ZoomFocus: "GetZoomFocusResponse.Value.ZoomFocus.JSON"

        class Keys(Protocol):
            """Keys"""

            state: Final = "ZoomFocus"

    class Range(Protocol):
        """Range"""

        class JSON(TypedDict):
            """JSON"""

            ZoomFocus: _ZoomFocusRange.JSON

    __slots__ = ()

    _get_value: providers.FactoryValue[Value.JSON]
    _value: Value.JSON

    def _get_state(self, create=False) -> Value.ZoomFocus.JSON:
        return self.lookup_value(
            self._get_value, self.Value.Keys.state, create=create, default=None
        )

    @property
    def state(self):
        return local_model.ZoomFocus(self._get_state)

    @property
    def channel_id(self):
        if value := self._get_state():
            return value.get(self.Value.ZoomFocus.Keys.channel_id, 0)
        return 0

    _get_initial: providers.FactoryValue[Value.JSON]
    _initial: Value.JSON

    @property
    def inital_state(self):
        return local_model.ZoomFocus(
            self.lookup_factory(self._get_initial, self.Value.Keys.state, default=None)
        )

    _get_range: providers.FactoryValue[Range.JSON]
    _range: Range.JSON

    @property
    def state_range(self):
        return _ZoomFocusRange(
            self.lookup_factory(self._get_range, self.Value.Keys.state, default=None)
        )


_DefaultZoomOperation: Final = ptz_typing.ZoomOperation.ZOOM
_DefaultZoomOperationStr: Final = zoom_operation_str(_DefaultZoomOperation)


class SetZoomFocusRequest(RequestWithChannel, ptz.SetZoomFocusRequest):
    """Set Zoom or Focus"""

    class Parameter(Protocol):
        """Parameter"""

        class Operation(Protocol):
            """Operation"""

            class JSON(ChannelJSON):
                """JSON"""

                op: str
                pos: int

            class Keys(ChannelKeys, Protocol):
                """Keys"""

                operation: Final = "op"
                position: Final = "pos"

        class JSON(TypedDict):
            """JSON"""

            ZoomFocus: "SetZoomFocusRequest.Parameter.Operation.JSON"

        class Keys(Protocol):
            """Keys"""

            state: Final = "ZoomFocus"

    __slots__ = ()

    COMMAND: Final = "StartZoomFocus"
    _COMMAND_ID: Final = hash(COMMAND)

    @property
    def id(self):
        return self._COMMAND_ID ^ self.channel_id

    def __init__(
        self,
        /,
        operation: ptz_typing.ZoomOperation = ...,
        position: int = ...,
        channel_id: int = ...,
        response_type: ResponseTypes = ...,
    ):
        super().__init__(
            command=type(self).COMMAND, channel_id=channel_id, response_type=response_type
        )
        if operation is not None and operation is not ...:
            self.operation = operation
        if position is not None and position is not ...:
            self.position = position

    _get_parameter: providers.FactoryValue[Parameter.JSON]
    _parameter: Parameter.JSON

    def _get_state(self, create=False) -> Parameter.Operation.JSON:
        return self.lookup_value(
            self._get_parameter,
            self.Parameter.Keys.state,
            create=create,
            default_factory=lambda: dict() if create else None,
        )

    @property
    def _state(self):
        return self._get_state()

    @property
    def channel_id(self):
        if value := self._state:
            return value.get(self.Parameter.Operation.Keys.channel_id, 0)
        return 0

    @channel_id.setter
    def channel_id(self, value):
        self._get_state(True)[self.Parameter.Operation.Keys.channel_id] = int(value)

    @property
    def operation(self):
        if value := self._state:
            return ptz_typing.ZoomOperation(
                value.get(self.Parameter.Operation.Keys.operation, _DefaultZoomOperationStr)
            )
        return _DefaultZoomOperation

    @operation.setter
    def operation(self, value):
        self._get_state(True)[self.Parameter.Operation.Keys.operation] = zoom_operation_str(value)

    @property
    def position(self):
        if value := self._state:
            return value.get(self.Parameter.Operation.Keys.position, 0)
        return 0

    @position.setter
    def position(self, value):
        self._get_state(True)[self.Parameter.Operation.Keys.position] = int(value)


_DefaultOperation: Final = ptz_typing.Operation.AUTO
_DefaultOperationStr: Final = operation_str(_DefaultOperation)


class SetControlRequest(RequestWithChannel, ptz.SetControlRequest):
    """PTZ Control"""

    class Parameter(Protocol):
        """Parameter"""

        class JSON(RequestWithChannel.Parameter.JSON):
            """JSON"""

            op: str
            id: int
            speed: int

        class Keys(RequestWithChannel.Parameter.Keys, Protocol):
            """Keys"""

            operation: Final = "op"
            preset_id: Final = "id"
            speed: Final = "speed"

    __slots__ = ()

    COMMAND: Final = "PtzCtrl"
    _COMMAND_ID: Final = hash(COMMAND)

    @property
    def id(self):
        return self._COMMAND_ID ^ self.channel_id

    def __init__(
        self,
        /,
        operation: ptz_typing.Operation = ...,
        speed: int = ...,
        preset_id: int = ...,
        channel_id: int = ...,
        response_type: ResponseTypes = ...,
    ):
        super().__init__(
            command=type(self).COMMAND, channel_id=channel_id, response_type=response_type
        )
        if operation is not None and operation is not ...:
            self.operation = operation
        if speed is not None and speed is not ...:
            self.speed = speed
        if preset_id is not None and preset_id is not ...:
            self.preset_id = preset_id

    _get_parameter: providers.FactoryValue[Parameter.JSON]
    _parameter: Parameter.JSON

    @property
    def operation(self):
        if value := self._parameter:
            return ptz_typing.Operation(
                value.get(self.Parameter.Keys.operation, _DefaultOperationStr)
            )
        return _DefaultOperation

    @operation.setter
    def operation(self, value):
        self._get_parameter(True)[self.Parameter.Keys.operation] = operation_str(value)

    @property
    def speed(self):
        if value := self._parameter:
            return value.get(self.Parameter.Keys.speed, 0)
        return 0

    @speed.setter
    def speed(self, value):
        self._get_parameter(True)[self.Parameter.Keys.speed] = int(value)

    @property
    def preset_id(self):
        if value := self._parameter:
            return value.get(self.Parameter.Keys.preset_id, 0)
        return 0

    @preset_id.setter
    def preset_id(self, value):
        self._get_parameter(True)[self.Parameter.Keys.preset_id] = int(value)
