"""REST PTZ Commands"""

from typing import (
    TYPE_CHECKING,
    Callable,
    Final,
    Iterable,
    MutableSequence,
    Protocol,
    TypedDict,
    cast,
)
from async_reolink.api.ptz import command as ptz
from async_reolink.api.ptz import typing as ptz_typing

from .._utilities import providers
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


class GetPresetRequest(RequestWithChannel, ptz.GetPresetRequest):
    """REST Get Presets Request"""

    __slots__ = ()

    COMMAND: Final = "GetPtzPreset"
    _COMMAND_ID: Final = hash(COMMAND)

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


class _PresetRange(providers.DictProvider):
    class JSON(TypedDict):
        """JSON"""

        id: model.MinMaxRange.JSON
        name: model.StringRange.JSON

    class Keys(local_model.Preset.Keys):
        """Keys"""

    __slots__ = ()

    @property
    def id(self):
        return model.MinMaxRange(
            lambda _: self._get_key_value(self._get_provided_value, self.Keys.id, default=None)
        )

    @property
    def name(self):
        return model.StringRange(
            lambda _: self._get_key_value(self._get_provided_value, self.Keys.name, default=None)
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

    def __init__(
        self,
        channel_id: int = 0,
        response_type: ResponseTypes = ResponseTypes.VALUE_ONLY,
    ):
        super().__init__()
        self.command = type(self).COMMAND
        self.response_type = response_type
        self.channel_id = channel_id


class _PatrolPresetRange(providers.DictProvider[str, any]):
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

    _provided_value: JSON

    @property
    def id(self):
        return model.MinMaxRange(
            lambda _: value.get(self.Keys.id) if (value := self._provided_value) else None
        )

    @property
    def dwell_time(self):
        return model.MinMaxRange(
            lambda _: value.get(self.Keys.dwell_time) if (value := self._provided_value) else None
        )

    @property
    def speed(self):
        return model.MinMaxRange(
            lambda _: value.get(self.Keys.speed) if (value := self._provided_value) else None
        )


class _PatrolRange(providers.DictProvider[str, any]):
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

    _provided_value: JSON

    @property
    def id(self):
        return model.MinMaxRange(
            lambda _: value.get(self.Keys.id) if (value := self._provided_value) else None
        )

    @property
    def name(self):
        return model.StringRange(
            lambda _: value.get(self.Keys.name) if (value := self._provided_value) else None
        )

    @property
    def preset(self):
        return _PatrolPresetRange(
            lambda _: value.get(self.Keys.preset) if (value := self._provided_value) else None
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

    _value: Value.JSON

    @property
    def _patrols(self):
        return value.get(self.Value.Keys.patrols) if (value := self._value) else None

    @property
    def channel_id(self):
        if (_l := self._patrols) and (value := next(iter(_l), None)):
            return value.get(self.Value.Patrol.Keys.channel_id, 0)
        return 0

    @property
    def patrols(self) -> DictList[int, local_model.Patrol]:
        return DictList(self.Value.Patrol.Keys.id, self._patrols, local_model.Patrol)

    @property
    def initial_patrol(self):
        return local_model.Patrol(
            lambda _: value.get(self.Value.Keys.patrols) if (value := self._initial) else None
        )

    @property
    def patrol_range(self):
        return _PatrolRange(
            lambda _: value.get(self.Value.Keys.patrols) if (value := self._range) else None
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

    _parameter: Parameter.JSON

    def _get_patrol(self, create=False) -> Parameter.Patrol.JSON:
        if (value := self._get_parameter(create)) is None:
            return None
        return value.setdefault(self.Parameter.Keys.patrol, {})

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

    def __init__(
        self,
        channel_id: int = 0,
        response_type: ResponseTypes = ResponseTypes.VALUE_ONLY,
    ):
        super().__init__()
        self.command = type(self).COMMAND
        self.response_type = response_type
        self.channel_id = channel_id


class _TrackRange(providers.DictProvider[str, any]):
    class JSON(TypedDict):
        """JSON"""

        id: model.MinMaxRange.JSON
        name: model.StringRange.JSON

    class Keys(Protocol):
        """Keys"""

        id: Final = "id"
        name: Final = "name"

    __slots__ = ()

    _provided_value: JSON

    @property
    def id(self):
        return model.MinMaxRange(
            lambda _: value.get(self.Keys.id) if (value := self._provided_value) else None
        )

    @property
    def name(self):
        return model.StringRange(
            lambda _: value.get(self.Keys.name) if (value := self._provided_value) else None
        )


class _TracksRange(providers.DictProvider[str, any]):
    class JSON(TypedDict):
        """JSON"""

        track: _TrackRange.JSON

    class Keys(Protocol):
        """Keys"""

        track: Final = "track"

    __slots__ = ()

    _provided_value: JSON

    @property
    def track(self):
        return _TrackRange(
            lambda _: value.get(self.Keys.track) if (value := self._provided_value) else None
        )


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

    _value: Value.JSON

    def _get_tattern(self, create=False):
        if value := self._value:
            return value.get(self.Value.Keys.tattern)
        return None

    @property
    def _tattern(self):
        return value.get(self.Value.Keys.tattern) if (value := self._value) else None

    @property
    def _tracks(self):
        return value.get(self.Value.Tattern.Keys.tracks) if (value := self._tattern) else None

    @property
    def channel_id(self):
        if value := self._tattern:
            return value.get(self.Value.Tattern.Keys.channel_id, 0)
        return 0

    @property
    def tracks(self):
        return DictList(local_model.Track.Keys.id, self._tracks, local_model.Track)

    _initial: Value.JSON

    @property
    def _initial_tattern(self):
        return value.get(self.Value.Keys.tattern) if (value := self._initial) else None

    @property
    def _inital_tracks(self):
        return (
            value.get(self.Value.Tattern.Keys.tracks) if (value := self._initial_tattern) else None
        )

    @property
    def initial_tracks(self) -> DictList[int, local_model.Track]:
        return DictList(
            local_model.Track.Keys.id,
            self._inital_tracks,
            local_model.Track,
        )

    _range: Range.JSON

    @property
    def _tattern_range(self):
        return value.get(self.Value.Keys.tattern) if (value := self._range) else None

    @property
    def _track_range(self):
        return value.get(self.Value.Tattern.Keys.track) if (value := self._tattern_range) else None

    @property
    def tracks_range(self):
        return _TracksRange(self._track_range)


class _MutableTracks(providers.ListProvider[dict[str, any]], MutableSequence[ptz_typing.Track]):
    __slots__ = ()

    def __getitem__(self, __k: int):
        return local_model.MutableTrack(
            lambda create: self._get_index_value(
                __k, create, default=lambda: dict() if create else None
            )
        )

    def __setitem__(self, __k: int, __v: ptz_typing.Track):
        self.__getitem__(__k).update(__v)

    def __delitem__(self, __k: int):
        if _list := self._provided_value:
            del _list[__k]

    def clear(self) -> None:
        if value := self._provided_value:
            value.clear()

    def __len__(self) -> int:
        if value := self._provided_value:
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
        channel_id: int = 0,
        response_type: ResponseTypes = ResponseTypes.VALUE_ONLY,
    ):
        super().__init__()
        self.command = type(self).COMMAND
        self.response_type = response_type
        self.channel_id = channel_id

    def _get_tattern(self, create=False) -> Parameter.Tattern.JSON:
        return self._get_key_value(
            self._get_parameter,
            self.Parameter.Keys.tattern,
            create,
            lambda: dict() if create else None,
        )

    @property
    def _tattern(self):
        return self._get_tattern()

    def _get_tracks(self, create=False) -> list[local_model.Track.JSON]:
        return self._get_key_value(
            self._get_tattern,
            self.Parameter.Tattern.Keys.tracks,
            create,
            lambda: list() if create else None,
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

    def __init__(
        self,
        channel_id: int = 0,
        response_type: ResponseTypes = ResponseTypes.VALUE_ONLY,
    ):
        super().__init__()
        self.command = type(self).COMMAND
        self.response_type = response_type
        self.channel_id = channel_id


class GetAutoFocusResponse(RestCommandResponse, ptz.GetAutoFocusResponse):
    """Get PTZ AutoFocus Response"""

    class Value(Protocol):
        """Value"""

        class AutoFocus(Protocol):
            """Auto Focus"""

            class JSON(TypedDict):
                """JSON"""

                disable: int

            class Keys(Protocol):
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

    _value: Value.JSON

    @property
    def _info(self):
        if value := self._value:
            return value.get(self.Value.Keys.info)
        return None

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
        self,
        disabled: bool,
        channel_id: int = 0,
        response_type: ResponseTypes = ResponseTypes.VALUE_ONLY,
    ):
        super().__init__()
        self.command = type(self).COMMAND
        self.response_type = response_type
        self.channel_id = channel_id
        self.disabled = disabled

    def _get_info(self, create=False) -> Parameter.AutoFocus.JSON:
        return self._get_key_value(
            self._get_parameter,
            self.Parameter.Keys.info,
            create,
            lambda: dict() if create else None,
        )

    @property
    def _info(self):
        return self._get_info()

    channel_id = SetTatternRequest.channel_id.setter(None)

    @GetAutoFocusResponse.disabled.setter
    def disabled(self, value):
        self._get_info(True)[self.Parameter.AutoFocus.Keys.disabled] = int(bool(value))


class GetZoomFocusRequest(RequestWithChannel, ptz.GetZoomFocusRequest):
    """Get Zoom and Focus"""

    __slots__ = ()

    COMMAND: Final = "GetZoomFocus"
    _COMMAND_ID: Final = hash(COMMAND)

    @property
    def id(self):
        return self._COMMAND_ID ^ self.channel_id

    def __init__(
        self,
        channel_id: int = 0,
        response_type: ResponseTypes = ResponseTypes.VALUE_ONLY,
    ):
        super().__init__()
        self.command = type(self).COMMAND
        self.response_type = response_type
        self.channel_id = channel_id


class _ZoomFocusRange(providers.DictProvider[str, any]):
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

    _provided_value: JSON

    @property
    def _zoom(self) -> Position.JSON:
        return self._get_key_value(self._get_provided_value, self.Keys.zoom, default=None)

    def _get_pos(self, source: Position.JSON):
        if source:
            return source.get(self.Position.Keys.value)
        return None

    @property
    def zoom(self):
        return model.MinMaxRange(self._get_pos(self._zoom))

    @property
    def _focus(self) -> Position.JSON:
        return self._get_key_value(self._get_provided_value, self.Keys.focus, default=None)

    @property
    def focus(self):
        return model.MinMaxRange(self._get_pos(self._focus))


class GetZoomFocusResponse(RestCommandResponse, ptz.GetZoomFocusResponse):
    """Get Zoom/Focus Response"""

    @classmethod
    def from_response(cls, response: any, /, request: Request | None = None, **kwargs):
        if super().is_response(response, GetZoomFocusRequest.COMMAND):
            return cls(response, request_id=request.id if request else None, **kwargs)
        return None

    class Value(Protocol):
        """Value"""

        class JSON(TypedDict):
            """JSON"""

            ZoomFocus: local_model.ZoomFocus.JSON

        class Keys(Protocol):
            """Keys"""

            state: Final = "ZoomFocus"

    class Range(Protocol):
        """Range"""

        class JSON(TypedDict):
            """JSON"""

            ZoomFocus: _ZoomFocusRange.JSON

    __slots__ = ()

    _value: Value.JSON

    channel_id = GetTatternResponse.channel_id

    @property
    def _state(self):
        if value := self._value:
            return value.get(self.Value.Keys.state)
        return None

    @property
    def state(self):
        return local_model.ZoomFocus(self._state)

    _initial: Value.JSON

    @property
    def _initial_state(self):
        if value := self._initial:
            return value.get(self.Value.Keys.state)
        return None

    @property
    def inital_state(self):
        return local_model.ZoomFocus(self._initial)

    _range: Range.JSON

    @property
    def _state_range(self):
        if value := self._range:
            return value.get(self.Value.Keys.state)
        return None

    @property
    def state_range(self):
        return _ZoomFocusRange(self._state_range)


_DefaultZoomOperation: Final = ptz_typing.ZoomOperation.ZOOM
_DefaultZoomOperationStr: Final = zoom_operation_str(_DefaultZoomOperation)


class SetZoomFocusRequest(Request, ptz.SetZoomFocusRequest):
    """Set Zoom or Focus"""

    class Parameter(Protocol):
        """Parameter"""

        class Operation(Protocol):
            """Operation"""

            class JSON(TypedDict):
                """JSON"""

                op: str
                pos: int

            class Keys(Protocol):
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
        channel_id: int = 0,
        response_type: ResponseTypes = ResponseTypes.VALUE_ONLY,
    ):
        super().__init__()
        self.command = type(self).COMMAND
        self.response_type = response_type
        self.channel_id = channel_id

    _parameter: Parameter.JSON

    def _get_state(self, create=False) -> Parameter.Operation.JSON:
        return self._get_key_value(
            self._get_parameter,
            self.Parameter.Keys.state,
            create,
            lambda: dict() if create else None,
        )

    @property
    def _state(self):
        return self._get_state()

    channel_id = SetTatternRequest.channel_id.setter(None)

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

        class Operation(Protocol):
            """Operation"""

            class JSON(TypedDict):
                """JSON"""

                op: str
                id: int
                speed: int

            class Keys(Protocol):
                """Keys"""

                operation: Final = "op"
                preset_id: Final = "id"
                speed: Final = "speed"

        class JSON(TypedDict):
            """JSON"""

            Control: "SetControlRequest.Parameter.Operation.JSON"

        class Keys(Protocol):
            """Keys"""

            state: Final = "Control"

    __slots__ = ()

    COMMAND: Final = "PtzCtrl"
    _COMMAND_ID: Final = hash(COMMAND)

    @property
    def id(self):
        return self._COMMAND_ID ^ self.channel_id

    def __init__(
        self,
        channel_id: int = 0,
        response_type: ResponseTypes = ResponseTypes.VALUE_ONLY,
    ):
        super().__init__()
        self.command = type(self).COMMAND
        self.response_type = response_type
        self.channel_id = channel_id

    _parameter: Parameter.JSON

    def _get_state(self, create=False) -> Parameter.Operation.JSON:
        return self._get_key_value(
            self._get_parameter,
            self.Parameter.Keys.state,
            create,
            lambda: dict() if create else None,
        )

    @property
    def _state(self):
        return self._get_state()

    channel_id = SetTatternRequest.channel_id.setter(None)

    @property
    def operation(self):
        if value := self._state:
            return ptz_typing.Operation(
                value.get(self.Parameter.Operation.Keys.operation, _DefaultOperationStr)
            )
        return _DefaultOperation

    @operation.setter
    def operation(self, value):
        self._get_state(True)[self.Parameter.Operation.Keys.operation] = operation_str(value)

    @property
    def speed(self):
        if value := self._state:
            return value.get(self.Parameter.Operation.Keys.speed, 0)
        return 0

    @speed.setter
    def speed(self, value):
        self._get_state(True)[self.Parameter.Operation.Keys.speed] = int(value)

    @property
    def preset_id(self):
        if value := self._state:
            return value.get(self.Parameter.Operation.Keys.preset_id, 0)
        return 0

    @preset_id.setter
    def preset_id(self, value):
        self._get_state(True)[self.Parameter.Operation.Keys.preset_id] = int(value)
