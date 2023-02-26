"""System capabilities"""

from enum import Enum, Flag
from typing import (
    Callable,
    ClassVar,
    Final,
    Mapping,
    Protocol,
    TypeAlias,
    TypedDict,
)
from typing_extensions import TypeVar, Self

from async_reolink.api.system import capabilities

from .._utilities.providers import value as providers

_JSONDict: TypeAlias = dict[str, any]

_NO_JSON: Final[_JSONDict] = None

# pylint: disable=too-few-public-methods
# pylint: disable=missing-function-docstring

_CT = TypeVar("_CT", infer_variance=True, default=int)


class Capability(capabilities.Capability[_CT], Protocol):
    """Capability"""

    Type: ClassVar[type[_CT]] = int

    class JSON(TypedDict):
        """JSON"""

        ver: int
        permit: int

    class Keys(Protocol):
        """Keys"""

        value: Final = "ver"
        permission: Final = "permit"


_defaults: dict[type, any] = {
    bool: False,
    int: 0,
    str: "",
}

_attempts: dict[any, bool] = {}


class SimpleCapability(providers.Value[_JSONDict], Capability[_CT]):
    """Capability"""

    __slots__ = ("__factory", "__default", "__type")

    def __init__(
        self,
        value: providers.FactoryValue[_JSONDict] | _JSONDict | None,
        value_factory: Callable[[int], _CT],
        /,
        default: _CT = ...,
        _type: type[_CT] | None = None,
    ) -> None:
        super().__init__(value)
        if value_factory is None:
            value_factory = _type
        self.__factory = value_factory
        if _type is None and isinstance(value_factory, type):
            _type = value_factory
        self.__default = None
        if default is ...:
            if (default := _defaults.get(_type)) is None and (
                _type or self.__factory
            ) not in _attempts:
                _attempts[_type or self.__factory] = True
                try:
                    if _type is None:
                        default = self.__factory(0)
                    else:
                        default = _type(0)
                except Exception:
                    default = None
                if default is not None:
                    if _type is None:
                        _type = type(default)
                    _defaults[_type] = default
        self.__default = default
        if _type is not None:
            self.__type = _type
        elif default is not None:
            self.__type = type(default)

    def _get_value(self, create=False) -> int:
        return self.lookup_value(self.__get_value__, self.Keys.value, create, default=None)

    def _get_permissions(self, create=False) -> int:
        return self.lookup_value(self.__get_value__, self.Keys.permission, create, default=None)

    def __getattribute__(self, __name: str):
        if __name == "Type" and self.__type is not None:
            return self.__type
        return super().__getattribute__(__name)

    @property
    def _default(self) -> _CT:
        return self.__default

    @property
    def _factory(self):
        return self.__factory

    @property
    def permissions(self):
        if (value := self._get_permissions()) is ... or value == 0:
            return None
        return capabilities.Permissions(value)

    @property
    def _raw_value(self):
        if (value := self._get_value()) is ...:
            return None
        return value

    def __bool__(self):
        return bool(self._raw_value)

    def __index__(self):
        return self._raw_value or 0

    def __int__(self):
        return self._raw_value or 0

    def __eq__(self, __o: object) -> bool:
        if hasattr(__o, "__index__"):
            return self._raw_value == __o.__index__()
        return self.value == __o

    @property
    def value(self):
        if (value := self._get_value()) is ...:
            return self._default
        return self._factory(value)

    def __str__(self):
        return str(self.value)

    def __hash__(self) -> int:
        return self.value.__hash__()


_CE = TypeVar("_CE", bound=Enum, default=Enum, infer_variance=True)


class EnumCapability(SimpleCapability[_CE]):
    """Capability"""

    __slots__ = ()

    def __init__(
        self,
        value: providers.FactoryValue[_JSONDict] | _JSONDict | None,
        _map: Mapping[int, _CE],
        /,
        _zero: _CE = ...,
        _type: type[_CE] | None = None,
    ) -> None:
        if _zero is ... and 0 in _map:
            _zero = _map[0]
        if _type is None:
            _type = next(map(type, iter(_map.values())), None)

        def value_factory(value: int) -> _CE:
            return self._value_factory(self, _map, value)

        super().__init__(value, value_factory, default=_zero, _type=_type)

    @classmethod
    def _value_factory(cls, self: Self, __map: Mapping[int, Enum], value: int):
        if (enum := __map.get(value)) is None:
            return self._default
        return enum


_CF = TypeVar("_CF", bound=Flag, default=Flag, infer_variance=True)


class FlagCapability(EnumCapability[_CF]):
    """Capability"""

    __slots__ = ("__cache",)

    def __init__(
        self,
        value: providers.FactoryValue[_JSONDict] | _JSONDict | None,
        _map: Mapping[int, _CF],
    ) -> None:
        super().__init__(value, _map, _zero=None)
        self.__cache: dict[int, _CF] = {}

    def __contains__(self, value: _CF):
        if (flag := self.value) is None:
            return False
        return flag.__contains__(value)

    def __iter__(self):
        if (flag := self.value) is None:
            return
        for f in flag:
            yield f

    def __len__(self):
        if (flag := self.value) is None:
            return 0
        return flag.__len__()

    def __or__(self, other: _CF):
        if (flag := self.value) is None:
            return other
        return flag | other

    def __and__(self, other: _CF):
        if (flag := self.value) is None:
            return self._default
        return flag & other

    def __xor__(self, other: _CF):
        if (flag := self.value) is None:
            return other
        return flag ^ other

    def __invert__(self):
        if (flag := self.value) is None:
            __type = self.Type
            if not issubclass(__type, Flag):
                return self._default
            return __type(0).__invert()
        return flag.__invert__()

    @classmethod
    def _value_factory(cls, self: Self, __map: Mapping[int, Flag], value: int):
        if (flag := __map.get(value)) is None and (flag := self.__cache.get(value)) is None:
            if not value:
                return self._default
            flag_value: int = 0
            for v, f in __map.items():
                if value & v == v:
                    if flag_value == 0:
                        flag = f
                        flag_value = v
                    else:
                        flag = flag | f
                        flag_value = flag_value | v
            if not flag_value:
                flag = self._default
            self.__cache[value] = flag

        return flag


_K = TypeVar("_K", infer_variance=True)
_V = TypeVar("_V", infer_variance=True)


def _inverse_map(map: Mapping[_K, _V]) -> Mapping[_V, _K]:
    return {v: k for k, v in map.items()}


_CLOUDSTORAGE: Final = _inverse_map(
    {
        capabilities.CloudStorage.UPLOAD: 1 << 0,
        capabilities.CloudStorage.CONFIG: 1 << 1,
        capabilities.CloudStorage.DEPLOY: 1 << 3,
    }
)

_DAYNIGHT: Final = _inverse_map(
    {
        capabilities.DayNight.DAY_NIGHT: 1,
        capabilities.DayNight.THRESHOLD: 2,
    }
)

_DDNS: Final = _inverse_map(
    {
        capabilities.DDns.SWAN: 1,
        capabilities.DDns.THREE322: 2,
        capabilities.DDns.DYNDNS: 3,
        capabilities.DDns.SWAN_3322: 4,
        capabilities.DDns.SWAN_DYNDNS: 5,
        capabilities.DDns.DYNDNS_3322: 6,
        capabilities.DDns.SWAN_DYNDNS_3322: 7,
        capabilities.DDns.NOIP: 8,
        capabilities.DDns.DYNDNS_NOIP: 9,
    }
)

_EMAIL: Final = _inverse_map(
    {
        capabilities.Email.JPEG: 1,
        capabilities.Email.VIDEO_JPEG: 2,
        capabilities.Email.VIDEO_JPEG_NICK: 3,
    }
)

_ENCODING_TYPE: Final = _inverse_map(
    {
        capabilities.EncodingType.H264: 0,
        capabilities.EncodingType.H265: 1,
    }
)

_FLOODLIGHT: Final = _inverse_map(
    {
        capabilities.FloodLight.WHITE: 1,
        capabilities.FloodLight.AUTO: 2,
    }
)

_FTP: Final = _inverse_map(
    {
        capabilities.Ftp.STREAM: 1,
        capabilities.Ftp.JPEG_STREAM: 2,
        capabilities.Ftp.MODE: 3,
        capabilities.Ftp.JPEG_STREAM_MODE: 4,
        capabilities.Ftp.STREAM_MODE_TYPE: 5,
        capabilities.Ftp.JPEG_STREAM_MODE_TYPE: 6,
    }
)

_LIVE: Final = _inverse_map(
    {
        capabilities.Live.MAIN_EXTERN_SUB: 1,
        capabilities.Live.MAIN_SUB: 2,
    }
)

_OSD: Final = _inverse_map(
    {
        capabilities.Osd.SUPPORTED: 1,
        capabilities.Osd.DISTINCT: 2,
    }
)

_PTZ_CONTROL: Final = _inverse_map(
    {
        capabilities.PTZControl.ZOOM: 1,
        capabilities.PTZControl.ZOOM_FOCUS: 2,
    }
)

_PTZ_DIRECTION: Final = _inverse_map(
    {
        capabilities.PTZDirection.EIGHT_AUTO: 0,
        capabilities.PTZDirection.FOUR_NO_AUTO: 1,
    }
)

_PTZ_TYPE: Final = _inverse_map(
    {
        capabilities.PTZType.AF: 1,
        capabilities.PTZType.PTZ: 2,
        capabilities.PTZType.PT: 3,
        capabilities.PTZType.BALL: 4,
        capabilities.PTZType.PTZ_NO_SPEED: 5,
    }
)

_RECORD_SCHEDULE: Final = _inverse_map(
    {
        capabilities.RecordSchedule.MOTION: 1,
        capabilities.RecordSchedule.MOTION_LIVE: 2,
    }
)

_SCHEDULE_VERSION: Final = _inverse_map(
    {
        capabilities.ScheduleVersion.BASIC: 0,
        capabilities.ScheduleVersion.V20: 1,
    }
)


_TIME: Final = _inverse_map(
    {
        capabilities.Time.SUNDAY: 1,
        capabilities.Time.ANYDAY: 2,
    }
)


_UPGRADE: Final = _inverse_map(
    {
        capabilities.Upgrade.MANUAL: 1,
        capabilities.Upgrade.ONLINE: 2,
    }
)


_VIDEO_CLIP: Final = _inverse_map(
    {
        capabilities.VideoClip.FIXED: 1,
        capabilities.VideoClip.MOD: 2,
    }
)


class ChannelCapabilities(providers.Value[_JSONDict], capabilities.ChannelCapabilities):
    """Channel Capabilities"""

    class AI(providers.Value[_JSONDict], capabilities.ChannelCapabilities.AI):
        """AI"""

        class Track(SimpleCapability[bool], capabilities.ChannelCapabilities.AI.Track):
            """Track"""

            class JSON(TypedDict):
                """JSON"""

                aiTrack: Capability.JSON
                aiTrackDogCat: Capability.JSON

            class Keys(Protocol):
                """Keys"""

                value: Final = "aiTrack"
                pet: Final = "aiTrackDogCat"

            __slots__ = ()

            def _get_capability(self, create=False) -> Capability.JSON:
                return self.lookup_value(
                    self.__get_value__, self.Keys.value, create, default=_NO_JSON
                )

            def _get_permissions(self, create=False) -> int:
                return self.lookup_value(
                    self._get_capability, Capability.Keys.permission, create, default=None
                )

            def _get_value(self, create=False) -> int:
                return self.lookup_value(
                    self._get_capability, Capability.Keys.value, create, default=None
                )

            def __init__(self, value: providers.FactoryValue[_JSONDict] | _JSONDict | None):
                super().__init__(value, bool)

            @property
            def pet(self):
                return SimpleCapability(
                    self.lookup_factory(self.__get_value__, self.Keys.pet, default=_NO_JSON),
                    bool,
                )

        class JSON(Track.JSON, TypedDict):
            """JSON"""

        class Keys(Protocol):
            """Keys"""

            track: "ChannelCapabilities.AI.Track.Keys"

        __slots__ = ()

        @property
        def track(self):
            return self.Track(self.__get_value__)

    class Alarm(providers.Value[_JSONDict], capabilities.ChannelCapabilities.Alarm):
        """Alarm"""

        class JSON(TypedDict):
            """JSON"""

            alarmAudio: Capability.JSON
            alarmIoIn: Capability.JSON
            alarmIoOut: Capability.JSON
            alarmMd: Capability.JSON
            alarmRf: Capability.JSON

        class Keys(Protocol):
            """Keys"""

            audio: Final = "alarmAudio"
            io_in: Final = "alarmIoIn"
            io_out: Final = "alarmIoOut"
            motion: Final = "alarmMd"
            rf: Final = "alarmRf"

        __slots__ = ()

        @property
        def audio(self):
            return SimpleCapability(
                self.lookup_factory(self.__get_value__, self.Keys.audio, default=_NO_JSON),
                bool,
            )

        @property
        def io_in(self):
            return SimpleCapability(
                self.lookup_factory(self.__get_value__, self.Keys.io_in, default=_NO_JSON),
                bool,
            )

        @property
        def io_out(self):
            return SimpleCapability(
                self.lookup_factory(self.__get_value__, self.Keys.io_out, default=_NO_JSON),
                bool,
            )

        @property
        def motion(self):
            return SimpleCapability(
                self.lookup_factory(self.__get_value__, self.Keys.motion, default=_NO_JSON),
                bool,
            )

        @property
        def rf(self):
            return SimpleCapability(
                self.lookup_factory(self.__get_value__, self.Keys.rf, default=_NO_JSON),
                bool,
            )

    class ISP(SimpleCapability[bool], capabilities.ChannelCapabilities.ISP):
        """ISP"""

        class JSON(TypedDict):
            """JSON"""

            isp: Capability.JSON
            isp3Dnr: Capability.JSON
            ispAntiFlick: Capability.JSON
            ispBackLight: Capability.JSON
            ispBright: Capability.JSON
            ispContrast: Capability.JSON
            ispDayNight: Capability.JSON
            ispExposureMode: Capability.JSON
            ispFlip: Capability.JSON
            ispHue: Capability.JSON
            ispMirror: Capability.JSON
            ispSatruation: Capability.JSON
            ispSharpen: Capability.JSON
            ispWhiteBalance: Capability.JSON

        class Keys(Protocol):
            """Keys"""

            value: Final = "isp"
            threeDnr: Final = "isp3Dnr"
            antiflicker: Final = "ispAntiFlick"
            backlight: Final = "ispBackLight"
            bright: Final = "ispBright"
            contrast: Final = "ispContrast"
            day_night: Final = "ispDayNight"
            exposure_mode: Final = "ispExposureMode"
            flip: Final = "ispFlip"
            hue: Final = "ispHue"
            mirror: Final = "ispMirror"
            satruation: Final = "ispSatruation"
            sharpen: Final = "ispSharpen"
            white_balance: Final = "ispWhiteBalance"

        __slots__ = ()

        def _get_capability(self, create=False) -> Capability.JSON:
            return self.lookup_value(self.__get_value__, self.Keys.value, create, default=_NO_JSON)

        def _get_permissions(self, create=False) -> int:
            return self.lookup_value(
                self._get_capability, Capability.Keys.permission, create, default=None
            )

        def _get_value(self, create=False) -> int:
            return self.lookup_value(
                self._get_capability, Capability.Keys.value, create, default=None
            )

        def __init__(self, value: providers.FactoryValue[_JSONDict] | _JSONDict | None):
            super().__init__(value, bool)

        @property
        def threeDnr(self):
            return SimpleCapability(
                self.lookup_factory(self.__get_value__, self.Keys.threeDnr, default=_NO_JSON),
                bool,
            )

        @property
        def antiflicker(self):
            return SimpleCapability(
                self.lookup_factory(self.__get_value__, self.Keys.antiflicker, default=_NO_JSON),
                bool,
            )

        @property
        def backlight(self):
            return SimpleCapability(
                self.lookup_factory(self.__get_value__, self.Keys.backlight, default=_NO_JSON),
                bool,
            )

        @property
        def bright(self):
            return SimpleCapability(
                self.lookup_factory(self.__get_value__, self.Keys.bright, default=_NO_JSON),
                bool,
            )

        @property
        def contrast(self):
            return SimpleCapability(
                self.lookup_factory(self.__get_value__, self.Keys.contrast, default=_NO_JSON),
                bool,
            )

        @property
        def day_night(self):
            return EnumCapability(
                self.lookup_factory(self.__get_value__, self.Keys.day_night, default=_NO_JSON),
                _DAYNIGHT,
            )

        @property
        def exposure_mode(self):
            return SimpleCapability(
                self.lookup_factory(self.__get_value__, self.Keys.exposure_mode, default=_NO_JSON),
                bool,
            )

        @property
        def flip(self):
            return SimpleCapability(
                self.lookup_factory(self.__get_value__, self.Keys.flip, default=_NO_JSON),
                bool,
            )

        @property
        def hue(self):
            return SimpleCapability(
                self.lookup_factory(self.__get_value__, self.Keys.hue, default=_NO_JSON),
                bool,
            )

        @property
        def mirror(self):
            return SimpleCapability(
                self.lookup_factory(self.__get_value__, self.Keys.mirror, default=_NO_JSON),
                bool,
            )

        @property
        def satruation(self):
            return SimpleCapability(
                self.lookup_factory(self.__get_value__, self.Keys.satruation, default=_NO_JSON),
                bool,
            )

        @property
        def sharpen(self):
            return SimpleCapability(
                self.lookup_factory(self.__get_value__, self.Keys.sharpen, default=_NO_JSON),
                bool,
            )

        @property
        def white_balance(self):
            return SimpleCapability(
                self.lookup_factory(self.__get_value__, self.Keys.white_balance, default=_NO_JSON),
                bool,
            )

    class MD(providers.Value[_JSONDict], capabilities.ChannelCapabilities.MD):
        """MotionDetection"""

        class Trigger(
            providers.Value[_JSONDict],
            capabilities.ChannelCapabilities.MD.Trigger,
        ):
            """Trigger"""

            class JSON(TypedDict):
                """JSON"""

                mdTriggerAudio: Capability.JSON
                mdTriggerRecord: Capability.JSON

            class Keys(Protocol):
                """Keys"""

                audo: Final = "mdTriggerAudio"
                record: Final = "mdTriggerRecord"

            __slots__ = ()

            @property
            def audio(self):
                return SimpleCapability(
                    self.lookup_factory(self.__get_value__, self.Keys.audo, default=_NO_JSON),
                    bool,
                )

            @property
            def record(self):
                return SimpleCapability(
                    self.lookup_factory(self.__get_value__, self.Keys.record, default=_NO_JSON),
                    bool,
                )

        class JSON(Trigger.JSON, TypedDict):
            """JSON"""

            mdWithPir: Capability.JSON

        class Keys(Protocol):
            """Keys"""

            with_pir: Final = "mdWithPir"
            trigger: "ChannelCapabilities.MD.Trigger.Keys"

        __slots__ = ()

        @property
        def trigger(self):
            return self.Trigger(self.__get_value__)

        @property
        def with_pir(self):
            return SimpleCapability(
                self.lookup_factory(self.__get_value__, self.Keys.with_pir, default=_NO_JSON),
                bool,
            )

    class PTZ(providers.Value[_JSONDict], capabilities.ChannelCapabilities.PTZ):
        """PTZ"""

        class JSON(TypedDict):
            """JSON"""

            ptzCtrl: Capability.JSON
            ptzDirection: Capability.JSON
            ptzPatrol: Capability.JSON
            ptzPreset: Capability.JSON
            ptzTattern: Capability.JSON
            ptzType: Capability.JSON

        class Keys(Protocol):
            """Keys"""

            control: Final = "ptzCtrl"
            direction: Final = "ptzDirection"
            patrol: Final = "ptzPatrol"
            preset: Final = "ptzPreset"
            tattern: Final = "ptzTattern"
            type: Final = "ptzType"

        __slots__ = ()

        @property
        def control(self):
            return EnumCapability(
                self.lookup_factory(self.__get_value__, self.Keys.control, default=_NO_JSON),
                _PTZ_CONTROL,
            )

        @property
        def direction(self):
            return EnumCapability(
                self.lookup_factory(self.__get_value__, self.Keys.direction, default=_NO_JSON),
                _PTZ_DIRECTION,
            )

        @property
        def patrol(self):
            return SimpleCapability(
                self.lookup_factory(self.__get_value__, self.Keys.patrol, default=_NO_JSON),
                bool,
            )

        @property
        def preset(self):
            return SimpleCapability(
                self.lookup_factory(self.__get_value__, self.Keys.preset, default=_NO_JSON),
                bool,
            )

        @property
        def tattern(self):
            return SimpleCapability(
                self.lookup_factory(self.__get_value__, self.Keys.tattern, default=_NO_JSON),
                bool,
            )

        @property
        def type(self):
            return EnumCapability(
                self.lookup_factory(self.__get_value__, self.Keys.type, default=_NO_JSON),
                _PTZ_TYPE,
            )

    class Record(providers.Value[_JSONDict], capabilities.ChannelCapabilities.Record):
        """Record"""

        class JSON(TypedDict):
            """JSON"""

            recCfg: Capability.JSON
            recDownload: Capability.JSON
            recReplay: Capability.JSON
            recSchedule: Capability.JSON

        class Keys(Protocol):
            """Keys"""

            config: Final = "recCfg"
            download: Final = "recDownload"
            replay: Final = "recReplay"
            schedule: Final = "recSchedule"

        __slots__ = ()

        @property
        def config(self):
            return SimpleCapability(
                self.lookup_factory(self.__get_value__, self.Keys.config, default=_NO_JSON),
                bool,
            )

        @property
        def download(self):
            return SimpleCapability(
                self.lookup_factory(self.__get_value__, self.Keys.download, default=_NO_JSON),
                bool,
            )

        @property
        def replay(self):
            return SimpleCapability(
                self.lookup_factory(self.__get_value__, self.Keys.replay, default=_NO_JSON),
                bool,
            )

        @property
        def schedule(self):
            return EnumCapability(
                self.lookup_factory(self.__get_value__, self.Keys.schedule, default=_NO_JSON),
                _RECORD_SCHEDULE,
            )

    class Supports(providers.Value[_JSONDict], capabilities.ChannelCapabilities.Supports):
        """Supports"""

        class AI(
            SimpleCapability[bool],
            capabilities.ChannelCapabilities.Supports.AI,
        ):
            """AI"""

            class JSON(TypedDict):
                """JSON"""

                supportAi: Capability.JSON
                supportAiAnimal: Capability.JSON
                supportAiDetectConfig: Capability.JSON
                supportAiDogCat: Capability.JSON
                supportAiFace: Capability.JSON
                supportAiPeople: Capability.JSON
                supportAiSensitivity: Capability.JSON
                supportAiStayTime: Capability.JSON
                supportAiTargetSize: Capability.JSON
                supportAiTrackClassify: Capability.JSON
                supportAiVehicle: Capability.JSON
                supportAoAdjust: Capability.JSON

            class Keys(Protocol):
                """Keys"""

                value: Final = "supportAi"
                animal: Final = "supportAiAnimal"
                detect_config: Final = "supportAiDetectConfig"
                pet: Final = "supportAiDogCat"
                face: Final = "supportAiFace"
                people: Final = "supportAiPeople"
                sensitivity: Final = "supportAiSensitivity"
                stay_time: Final = "supportAiStayTime"
                target_size: Final = "supportAiTargetSize"
                track_classify: Final = "supportAiTrackClassify"
                vehicle: Final = "supportAiVehicle"
                adjust: Final = "supportAoAdjust"

            __slots__ = ()

            def _get_capability(self, create=False) -> Capability.JSON:
                return self.lookup_value(
                    self.__get_value__, self.Keys.value, create, default=_NO_JSON
                )

            def _get_permissions(self, create=False) -> int:
                return self.lookup_value(
                    self._get_capability, Capability.Keys.permission, create, default=None
                )

            def _get_value(self, create=False) -> int:
                return self.lookup_value(
                    self._get_capability, Capability.Keys.value, create, default=None
                )

            def __init__(self, value: providers.FactoryValue[_JSONDict] | _JSONDict | None):
                super().__init__(value, bool)

            @property
            def animal(self):
                return SimpleCapability(
                    self.lookup_factory(self.__get_value__, self.Keys.animal, default=_NO_JSON),
                    bool,
                )

            @property
            def detect_config(self):
                return SimpleCapability(
                    self.lookup_factory(
                        self.__get_value__, self.Keys.detect_config, default=_NO_JSON
                    ),
                    bool,
                )

            @property
            def pet(self):
                return SimpleCapability(
                    self.lookup_factory(self.__get_value__, self.Keys.pet, default=_NO_JSON),
                    bool,
                )

            @property
            def face(self):
                return SimpleCapability(
                    self.lookup_factory(self.__get_value__, self.Keys.face, default=_NO_JSON),
                    bool,
                )

            @property
            def people(self):
                return SimpleCapability(
                    self.lookup_factory(self.__get_value__, self.Keys.people, default=_NO_JSON),
                    bool,
                )

            @property
            def sensitivity(self):
                return SimpleCapability(
                    self.lookup_factory(
                        self.__get_value__, self.Keys.sensitivity, default=_NO_JSON
                    ),
                    bool,
                )

            @property
            def stay_time(self):
                return SimpleCapability(
                    self.lookup_factory(self.__get_value__, self.Keys.stay_time, default=_NO_JSON),
                    bool,
                )

            @property
            def target_size(self):
                return SimpleCapability(
                    self.lookup_factory(
                        self.__get_value__, self.Keys.target_size, default=_NO_JSON
                    ),
                    bool,
                )

            @property
            def track_classify(self):
                return SimpleCapability(
                    self.lookup_factory(
                        self.__get_value__, self.Keys.track_classify, default=_NO_JSON
                    ),
                    bool,
                )

            @property
            def vehicle(self):
                return SimpleCapability(
                    self.lookup_factory(self.__get_value__, self.Keys.vehicle, default=_NO_JSON),
                    bool,
                )

            @property
            def adjust(self):
                return SimpleCapability(
                    self.lookup_factory(self.__get_value__, self.Keys.adjust, default=_NO_JSON),
                    bool,
                )

        class FloodLight(
            providers.Value[_JSONDict],
            capabilities.ChannelCapabilities.Supports.FloodLight,
        ):
            """FloodLight"""

            class JSON(TypedDict):
                """JSON"""

                supportFLBrightness: Capability.JSON
                supportFLIntelligent: Capability.JSON
                supportFLKeepOn: Capability.JSON
                supportFLSchedule: Capability.JSON
                supportFLswitch: Capability.JSON

            class Keys(Protocol):
                """Keys"""

                brightness: Final = "supportFLBrightness"
                intelligent: Final = "supportFLIntelligent"
                keep_on: Final = "supportFLKeepOn"
                schedule: Final = "supportFLSchedule"
                switch: Final = "supportFLswitch"

            __slots__ = ()

            @property
            def brightness(self):
                return SimpleCapability(
                    self.lookup_factory(self.__get_value__, self.Keys.brightness, default=_NO_JSON),
                    bool,
                )

            @property
            def intelligent(self):
                return SimpleCapability(
                    self.lookup_factory(
                        self.__get_value__, self.Keys.intelligent, default=_NO_JSON
                    ),
                    bool,
                )

            @property
            def keep_on(self):
                return SimpleCapability(
                    self.lookup_factory(self.__get_value__, self.Keys.keep_on, default=_NO_JSON),
                    bool,
                )

            @property
            def schedule(self):
                return SimpleCapability(
                    self.lookup_factory(self.__get_value__, self.Keys.schedule, default=_NO_JSON),
                    bool,
                )

            @property
            def switch(self):
                return SimpleCapability(
                    self.lookup_factory(self.__get_value__, self.Keys.switch, default=_NO_JSON),
                    bool,
                )

        class JSON(AI.JSON, FloodLight.JSON, TypedDict):
            """JSON"""

            supportGop: Capability.JSON
            supportMd: Capability.JSON
            supportPtzCheck: Capability.JSON
            supportThresholdAdjust: Capability.JSON
            supportWhiteDark: Capability.JSON

        class Keys(Protocol):
            """Keys"""

            ai: "ChannelCapabilities.Supports.AI.Keys"
            gop: Final = "supportGop"
            flood_light: "ChannelCapabilities.Supports.FloodLight.Keys"
            motion_detection: Final = "supportMd"
            ptz_check: Final = "supportPtzCheck"
            threshold_adjust: Final = "supportThresholdAdjust"
            white_dark: Final = "supportWhiteDark"

        __slots__ = ()

        @property
        def ai(self):
            return self.AI(self.__get_value__)

        @property
        def flood_light(self):
            return self.FloodLight(self.__get_value__)

        @property
        def gop(self):
            return SimpleCapability(
                self.lookup_factory(self.__get_value__, self.Keys.gop, default=_NO_JSON),
                bool,
            )

        @property
        def motion_detection(self):
            return SimpleCapability(
                self.lookup_factory(
                    self.__get_value__, self.Keys.motion_detection, default=_NO_JSON
                ),
                bool,
            )

        @property
        def ptz_check(self):
            return SimpleCapability(
                self.lookup_factory(self.__get_value__, self.Keys.ptz_check, default=_NO_JSON),
                bool,
            )

        @property
        def threshold_adjust(self):
            return SimpleCapability(
                self.lookup_factory(
                    self.__get_value__, self.Keys.threshold_adjust, default=_NO_JSON
                ),
                bool,
            )

        @property
        def white_dark(self):
            return SimpleCapability(
                self.lookup_factory(self.__get_value__, self.Keys.white_dark, default=_NO_JSON),
                bool,
            )

    class JSON(AI.JSON, Alarm.JSON, ISP.JSON, MD.JSON, Record.JSON, Supports.JSON, TypedDict):
        """JSON"""

        battery: Capability.JSON
        batAnalysis: Capability.JSON
        cameraMode: Capability.JSON
        disableAutoFocus: Capability.JSON
        enc: Capability.JSON
        floodLight: Capability.JSON
        ftp: Capability.JSON
        image: Capability.JSON
        indicatorLight: Capability.JSON
        ledControl: Capability.JSON
        live: Capability.JSON
        mainEncType: Capability.JSON
        mask: Capability.JSON
        osd: Capability.JSON
        powerLed: Capability.JSON
        shelterCfg: Capability.JSON
        snap: Capability.JSON
        videoClip: Capability.JSON
        waterMark: Capability.JSON
        white_balance: Capability.JSON

    class Keys(Protocol):
        """Keys"""

        ai: "ChannelCapabilities.AI.Keys"
        alarm: "ChannelCapabilities.Alarm.Keys"
        battery: Final = "battery"
        battery_analysis: Final = "batAnalysis"
        camera_mode: Final = "cameraMode"
        disable_autofocus: Final = "disableAutoFocus"
        enc: Final = "enc"
        floodlight: Final = "floodLight"
        ftp: Final = "ftp"
        image: Final = "image"
        indicator_light: Final = "indicatorLight"
        isp: "ChannelCapabilities.ISP.Keys"
        led_control: Final = "ledControl"
        live: Final = "live"
        main_encoding: Final = "mainEncType"
        mask: Final = "mask"
        motion_detection: "ChannelCapabilities.MD.Keys"
        osd: Final = "osd"
        power_led: Final = "powerLed"
        ptz: "ChannelCapabilities.PTZ.Keys"
        record: "ChannelCapabilities.Record.Keys"
        shelter_config: Final = "shelterCfg"
        snap: Final = "snap"
        supports: "ChannelCapabilities.Supports.Keys"
        video_clip: Final = "videoClip"
        watermark: Final = "waterMark"
        white_balance: Final = "white_balance"

    __slots__ = ()

    @property
    def ai(self):
        return self.AI(self.__get_value__)

    @property
    def alarm(self):
        return self.Alarm(self.__get_value__)

    @property
    def battery(self):
        return SimpleCapability(
            self.lookup_factory(self.__get_value__, self.Keys.battery, default=_NO_JSON),
            bool,
        )

    @property
    def battery_analysis(self):
        return SimpleCapability(
            self.lookup_factory(self.__get_value__, self.Keys.battery_analysis, default=_NO_JSON),
            bool,
        )

    @property
    def camera_mode(self):
        return SimpleCapability(
            self.lookup_factory(self.__get_value__, self.Keys.camera_mode, default=_NO_JSON),
            bool,
        )

    @property
    def disable_autofocus(self):
        return SimpleCapability(
            self.lookup_factory(self.__get_value__, self.Keys.disable_autofocus, default=_NO_JSON),
            bool,
        )

    @property
    def enc(self):
        return SimpleCapability(
            self.lookup_factory(self.__get_value__, self.Keys.enc, default=_NO_JSON),
            bool,
        )

    @property
    def floodlight(self):
        return EnumCapability(
            self.lookup_factory(self.__get_value__, self.Keys.floodlight, default=_NO_JSON),
            _FLOODLIGHT,
        )

    @property
    def ftp(self):
        return EnumCapability(
            self.lookup_factory(self.__get_value__, self.Keys.ftp, default=_NO_JSON), _FTP
        )

    @property
    def image(self):
        return SimpleCapability(
            self.lookup_factory(self.__get_value__, self.Keys.image, default=_NO_JSON),
            bool,
        )

    @property
    def indicator_light(self):
        return SimpleCapability(
            self.lookup_factory(self.__get_value__, self.Keys.indicator_light, default=_NO_JSON),
            bool,
        )

    @property
    def isp(self):
        return self.ISP(self.__get_value__)

    @property
    def led_control(self):
        return SimpleCapability(
            self.lookup_factory(self.__get_value__, self.Keys.led_control, default=_NO_JSON),
            bool,
        )

    @property
    def live(self):
        return EnumCapability(
            self.lookup_factory(self.__get_value__, self.Keys.live, default=_NO_JSON), _LIVE
        )

    @property
    def main_encoding(self):
        return EnumCapability(
            self.lookup_factory(self.__get_value__, self.Keys.main_encoding, default=_NO_JSON),
            _ENCODING_TYPE,
        )

    @property
    def mask(self):
        return SimpleCapability(
            self.lookup_factory(self.__get_value__, self.Keys.mask, default=_NO_JSON),
            bool,
        )

    @property
    def motion_detection(self):
        return self.MD(self.__get_value__)

    @property
    def osd(self):
        return EnumCapability(
            self.lookup_factory(self.__get_value__, self.Keys.osd, default=_NO_JSON), _OSD
        )

    @property
    def power_led(self):
        return SimpleCapability(
            self.lookup_factory(self.__get_value__, self.Keys.power_led, default=_NO_JSON),
            bool,
        )

    @property
    def ptz(self):
        return self.PTZ(self.__get_value__)

    @property
    def record(self):
        return self.Record(self.__get_value__)

    @property
    def shelter_config(self):
        return SimpleCapability(
            self.lookup_factory(self.__get_value__, self.Keys.shelter_config, default=_NO_JSON),
            bool,
        )

    @property
    def snap(self):
        return SimpleCapability(
            self.lookup_factory(self.__get_value__, self.Keys.snap, default=_NO_JSON),
            bool,
        )

    @property
    def supports(self):
        return self.Supports(self.__get_value__)

    @property
    def video_clip(self):
        return EnumCapability(
            self.lookup_factory(self.__get_value__, self.Keys.video_clip, default=_NO_JSON),
            _VIDEO_CLIP,
        )

    @property
    def watermark(self):
        return SimpleCapability(
            self.lookup_factory(self.__get_value__, self.Keys.watermark, default=_NO_JSON),
            bool,
        )

    @property
    def white_balance(self):
        return SimpleCapability(
            self.lookup_factory(self.__get_value__, self.Keys.white_balance, default=_NO_JSON),
            bool,
        )


class _Channels(providers.Value[list[_JSONDict]], Mapping[int, ChannelCapabilities]):
    """Channels"""

    __slots__ = ()

    def __getitem__(self, __k: int):
        return ChannelCapabilities(self.lookup_factory(self.__get_value__, __k, default=_NO_JSON))

    def __iter__(self):
        if (_list := self.__get_value__()) is None:
            return
        for i in range(0, len(_list)):
            yield i

    def __len__(self):
        if (_list := self.__get_value__()) is None:
            return 0
        return len(_list)


class Capabilities(providers.Value[_JSONDict], capabilities.Capabilities):
    """Capabilities"""

    class Alarm(providers.Value[_JSONDict], capabilities.Capabilities.Alarm):
        """Alarm"""

        class HDD(providers.Value[_JSONDict], capabilities.Capabilities.Alarm.HDD):
            """HDD"""

            class JSON(TypedDict):
                """JSON"""

                alarmHddErr: Capability.JSON
                alarmHddFull: Capability.JSON

            class Keys(Protocol):
                """Keys"""

                error: Final = "alarmHddErr"
                full: Final = "alarmHddFull"

            __slots__ = ()

            @property
            def error(self):
                return SimpleCapability(
                    self.lookup_factory(self.__get_value__, self.Keys.error, default=_NO_JSON),
                    bool,
                )

            @property
            def full(self):
                return SimpleCapability(
                    self.lookup_factory(self.__get_value__, self.Keys.full, default=_NO_JSON),
                    bool,
                )

        class JSON(HDD.JSON):
            """JSON"""

            alarmAudio: Capability.JSON
            alarmDisconnet: Capability.JSON
            alarmIpConflict: Capability.JSON

        class Keys(Protocol):
            """Keys"""

            audio: Final = "alarmAudio"
            disconnect: Final = "alarmDisconnet"
            hdd: "Capabilities.Alarm.HDD.Keys"
            ip_conflict: Final = "alarmIpConflict"

        __slots__ = ()

        @property
        def audio(self):
            return SimpleCapability(
                self.lookup_factory(self.__get_value__, self.Keys.audio, default=_NO_JSON),
                bool,
            )

        @property
        def disconnect(self):
            return SimpleCapability(
                self.lookup_factory(self.__get_value__, self.Keys.disconnect, default=_NO_JSON),
                bool,
            )

        @property
        def hdd(self):
            return self.HDD(self.__get_value__)

        @property
        def ip_conflict(self):
            return SimpleCapability(
                self.lookup_factory(self.__get_value__, self.Keys.ip_conflict, default=_NO_JSON),
                bool,
            )

    class Device(providers.Value[_JSONDict], capabilities.Capabilities.Device):
        """Device"""

        class JSON(TypedDict):
            """JSON"""

            devInfo: Capability.JSON
            devName: Capability.JSON

        class Keys(Protocol):
            """Keys"""

            info: Final = "devInfo"
            name: Final = "devName"

        __slots__ = ()

        @property
        def info(self):
            return SimpleCapability(
                self.lookup_factory(self.__get_value__, self.Keys.info, default=_NO_JSON),
                bool,
            )

        @property
        def name(self):
            return SimpleCapability(
                self.lookup_factory(self.__get_value__, self.Keys.name, default=_NO_JSON),
                bool,
            )

    class Email(EnumCapability[capabilities.Email], capabilities.Capabilities.Email):
        """Email"""

        class JSON(TypedDict):
            """JSON"""

            email: Capability.JSON
            emailInterval: Capability.JSON
            emailSchedule: Capability.JSON

        class Keys(Protocol):
            """Keys"""

            value: Final = "email"
            interval: Final = "emailInterval"
            schedule: Final = "emailSchedule"

        __slots__ = ()

        def _get_capability(self, create=False) -> Capability.JSON:
            return self.lookup_value(self.__get_value__, self.Keys.value, create, default=_NO_JSON)

        def _get_permissions(self, create=False) -> int:
            return self.lookup_value(
                self._get_capability, Capability.Keys.permission, create, default=None
            )

        def _get_value(self, create=False) -> int:
            return self.lookup_value(
                self._get_capability, Capability.Keys.value, create, default=None
            )

        def __init__(self, value: providers.FactoryValue[_JSONDict] | _JSONDict | None):
            super().__init__(value, _EMAIL)

        @property
        def interval(self):
            return SimpleCapability(
                self.lookup_factory(self.__get_value__, self.Keys.interval, default=_NO_JSON),
                bool,
            )

        @property
        def schedule(self):
            return SimpleCapability(
                self.lookup_factory(self.__get_value__, self.Keys.schedule, default=_NO_JSON),
                bool,
            )

    class FTP(providers.Value[_JSONDict], capabilities.Capabilities.FTP):
        """FTP"""

        class Stream(providers.Value[_JSONDict], capabilities.Capabilities.FTP.Stream):
            """Stream"""

            class JSON(TypedDict):
                """JSON"""

                ftpExtStream: Capability.JSON
                ftpSubStream: Capability.JSON

            class Keys(Protocol):
                """Keys"""

                ext: Final = "ftpExtStream"
                sub: Final = "ftpSubStream"

            __slots__ = ()

            @property
            def ext(self):
                return SimpleCapability(
                    self.lookup_factory(self.__get_value__, self.Keys.ext, default=_NO_JSON),
                    bool,
                )

            @property
            def sub(self):
                return SimpleCapability(
                    self.lookup_factory(self.__get_value__, self.Keys.sub, default=_NO_JSON),
                    bool,
                )

        class JSON(Stream.JSON):
            """JSON"""

            ftpAutoDir: Capability.JSON
            ftpPic: Capability.JSON
            ftpTest: Capability.JSON

        class Keys(Protocol):
            """Keys"""

            stream: "Capabilities.FTP.Stream.Keys"
            auto_dir: Final = "ftpAutoDir"
            picture: Final = "ftpPic"
            test: Final = "ftpTest"

        __slots__ = ()

        @property
        def auto_dir(self):
            return SimpleCapability(
                self.lookup_factory(self.__get_value__, self.Keys.auto_dir, default=_NO_JSON),
                bool,
            )

        @property
        def stream(self):
            return self.Stream(self.__get_value__)

        @property
        def picture(self):
            return SimpleCapability(
                self.lookup_factory(self.__get_value__, self.Keys.picture, default=_NO_JSON),
                bool,
            )

        @property
        def test(self):
            return SimpleCapability(
                self.lookup_factory(self.__get_value__, self.Keys.test, default=_NO_JSON),
                bool,
            )

    class Record(providers.Value[_JSONDict], capabilities.Capabilities.Record):
        """Record"""

        class JSON(TypedDict):
            """JSON"""

            recExtensionTimeList: Capability.JSON
            recOverWrite: Capability.JSON
            recPackDuration: Capability.JSON
            recPreRecord: Capability.JSON

        class Keys(Protocol):
            """Keys"""

            extension_time_list: Final = "recExtensionTimeList"
            overwrite: Final = "recOverWrite"
            pack_duration: Final = "recPackDuration"
            pre_record: Final = "recPreRecord"

        __slots__ = ()

        @property
        def extension_time_list(self):
            return SimpleCapability(
                self.lookup_factory(
                    self.__get_value__, self.Keys.extension_time_list, default=_NO_JSON
                ),
                bool,
            )

        @property
        def overwrite(self):
            return SimpleCapability(
                self.lookup_factory(self.__get_value__, self.Keys.overwrite, default=_NO_JSON),
                bool,
            )

        @property
        def pack_duration(self):
            return SimpleCapability(
                self.lookup_factory(self.__get_value__, self.Keys.pack_duration, default=_NO_JSON),
                bool,
            )

        @property
        def pre_record(self):
            return SimpleCapability(
                self.lookup_factory(self.__get_value__, self.Keys.pre_record, default=_NO_JSON),
                bool,
            )

    class Supports(providers.Value[_JSONDict], capabilities.Capabilities.Supports):
        """Supports"""

        class Audio(providers.Value[_JSONDict], capabilities.Capabilities.Supports.Audio):
            """Audio"""

            class Alarm(
                SimpleCapability[bool],
                capabilities.Capabilities.Supports.Audio.Alarm,
            ):
                """Alarm"""

                class JSON(TypedDict):
                    """JSON"""

                    supportAudioAlarm: Capability.JSON
                    supportAudioAlarmEnable: Capability.JSON
                    supportAudioAlarmSchedule: Capability.JSON
                    supportAudioAlarmTaskEnable: Capability.JSON

                class Keys(Protocol):
                    """Keys"""

                    value: Final = "supportAudioAlarm"
                    enable: Final = "supportAudioAlarmEnable"
                    schedule: Final = "supportAudioAlarmSchedule"
                    task_enable: Final = "supportAudioAlarmTaskEnable"

                __slots__ = ()

                def _get_capability(self, create=False) -> Capability.JSON:
                    return self.lookup_value(
                        self.__get_value__, self.Keys.value, create, default=_NO_JSON
                    )

                def _get_permissions(self, create=False) -> int:
                    return self.lookup_value(
                        self._get_capability, Capability.Keys.permission, create, default=None
                    )

                def _get_value(self, create=False) -> int:
                    return self.lookup_value(
                        self._get_capability, Capability.Keys.value, create, default=None
                    )

                def __init__(self, value: providers.FactoryValue[_JSONDict] | _JSONDict | None):
                    super().__init__(value, bool)

                @property
                def enable(self):
                    return SimpleCapability(
                        self.lookup_factory(self.__get_value__, self.Keys.enable, default=_NO_JSON),
                        bool,
                    )

                @property
                def schedule(self):
                    return SimpleCapability(
                        self.lookup_factory(
                            self.__get_value__, self.Keys.schedule, default=_NO_JSON
                        ),
                        bool,
                    )

                @property
                def task_enable(self):
                    return SimpleCapability(
                        self.lookup_factory(
                            self.__get_value__, self.Keys.task_enable, default=_NO_JSON
                        ),
                        bool,
                    )

            class JSON(Alarm.JSON):
                """JSON"""

            class Keys(Protocol):
                """Keys"""

                alarm: "Capabilities.Supports.Audio.Alarm.Keys"

            __slots__ = ()

            _provided_value: JSON

            @property
            def alarm(self):
                return self.Alarm(self.__get_value__)

        class Buzzer(SimpleCapability[bool], capabilities.Capabilities.Supports.Buzzer):
            """Buzzer"""

            __slots__ = ()

            class Task(
                SimpleCapability[bool],
                capabilities.Capabilities.Supports.Buzzer.Task,
            ):
                """Task"""

                class JSON(TypedDict):
                    """JSON"""

                    supportBuzzerTask: Capability.JSON
                    supportBuzzerEnable: Capability.JSON

                class Keys(Protocol):
                    """Keys"""

                    value: Final = "supportBuzzerTask"
                    enable: Final = "supportBuzzerEnable"

                __slots__ = ()

                def _get_capability(self, create=False) -> Capability.JSON:
                    return self.lookup_value(
                        self.__get_value__, self.Keys.value, create, default=_NO_JSON
                    )

                def _get_permissions(self, create=False) -> int:
                    return self.lookup_value(
                        self._get_capability, Capability.Keys.permission, create, default=None
                    )

                def _get_value(self, create=False) -> int:
                    return self.lookup_value(
                        self._get_capability, Capability.Keys.value, create, default=None
                    )

                def __init__(self, value: providers.FactoryValue[_JSONDict] | _JSONDict | None):
                    super().__init__(value, bool)

                @property
                def enable(self):
                    return SimpleCapability(
                        self.lookup_factory(self.__get_value__, self.Keys.enable, default=_NO_JSON),
                        bool,
                    )

            class JSON(Task.JSON):
                """JSON"""

                supportBuzzer: Capability.JSON

            class Keys(Protocol):
                """Keys"""

                task: "Capabilities.Supports.Buzzer.Task.Keys"
                value: Final = "supportBuzzer"

            __slots__ = ()

            def _get_capability(self, create=False) -> Capability.JSON:
                return self.lookup_value(
                    self.__get_value__, self.Keys.value, create, default=_NO_JSON
                )

            def _get_permissions(self, create=False) -> int:
                return self.lookup_value(
                    self._get_capability, Capability.Keys.permission, create, default=None
                )

            def _get_value(self, create=False) -> int:
                return self.lookup_value(
                    self._get_capability, Capability.Keys.value, create, default=None
                )

            def __init__(self, value: providers.FactoryValue[_JSONDict] | _JSONDict | None):
                super().__init__(value, bool)

            @property
            def task(self):
                return self.Task(self.__get_value__)

        class Email(providers.Value[_JSONDict], capabilities.Capabilities.Supports.Email):
            """Email"""

            class JSON(TypedDict):
                """JSON"""

                supportEmailEnable: Capability.JSON
                supportEmailTaskEnable: Capability.JSON

            class Keys(Protocol):
                """Keys"""

                enable: Final = "supportEmailEnable"
                task_enable: Final = "supportEmailTaskEnable"

            __slots__ = ()

            @property
            def enable(self):
                return SimpleCapability(
                    self.lookup_factory(self.__get_value__, self.Keys.enable, default=_NO_JSON),
                    bool,
                )

            @property
            def task_enable(self):
                return SimpleCapability(
                    self.lookup_factory(
                        self.__get_value__, self.Keys.task_enable, default=_NO_JSON
                    ),
                    bool,
                )

        class FTP(providers.Value[_JSONDict], capabilities.Capabilities.Supports.FTP):
            """FTP"""

            class Cover(
                providers.Value[_JSONDict],
                capabilities.Capabilities.Supports.FTP.Cover,
            ):
                """Cover"""

                class JSON(TypedDict):
                    """JSON"""

                    supportFtpCoverPicture: Capability.JSON
                    supportFtpCoverVideo: Capability.JSON

                class Keys(Protocol):
                    """Keys"""

                    picture: Final = "supportFtpCoverPicture"
                    video: Final = "supportFtpCoverVideo"

                __slots__ = ()

                @property
                def picture(self):
                    return SimpleCapability(
                        self.lookup_factory(
                            self.__get_value__, self.Keys.picture, default=_NO_JSON
                        ),
                        bool,
                    )

                @property
                def video(self):
                    return SimpleCapability(
                        self.lookup_factory(self.__get_value__, self.Keys.video, default=_NO_JSON),
                        bool,
                    )

            class Picture(
                providers.Value[_JSONDict],
                capabilities.Capabilities.Supports.FTP.Picture,
            ):
                """Picture"""

                class JSON(TypedDict):
                    """JSON"""

                    supportFtpPicCaptureMode: Capability.JSON
                    supportFtpPicResoCustom: Capability.JSON
                    supportFtpPictureSwap: Capability.JSON

                class Keys(Protocol):
                    """Keys"""

                    capture_mode: Final = "supportFtpPicCaptureMode"
                    custom_resolution: Final = "supportFtpPicResoCustom"
                    swap: Final = "supportFtpPictureSwap"

                __slots__ = ()

                @property
                def capture_mode(self):
                    return SimpleCapability(
                        self.lookup_factory(
                            self.__get_value__, self.Keys.capture_mode, default=_NO_JSON
                        ),
                        bool,
                    )

                @property
                def custom_resolution(self):
                    return SimpleCapability(
                        self.lookup_factory(
                            self.__get_value__, self.Keys.custom_resolution, default=_NO_JSON
                        ),
                        bool,
                    )

                @property
                def swap(self):
                    return SimpleCapability(
                        self.lookup_factory(self.__get_value__, self.Keys.swap, default=_NO_JSON),
                        bool,
                    )

            class Task(
                SimpleCapability[bool],
                capabilities.Capabilities.Supports.FTP.Task,
            ):
                """Task"""

                class JSON(TypedDict):
                    """JSON"""

                    supportFtpTask: Capability.JSON
                    supportFtpTaskEnable: Capability.JSON

                class Keys(Protocol):
                    """Keys"""

                    value: Final = "supportFtpTask"
                    enable: Final = "supportFtpTaskEnable"

                __slots__ = ()

                def _get_capability(self, create=False) -> Capability.JSON:
                    return self.lookup_value(
                        self.__get_value__, self.Keys.value, create, default=_NO_JSON
                    )

                def _get_permissions(self, create=False) -> int:
                    return self.lookup_value(
                        self._get_capability, Capability.Keys.permission, create, default=None
                    )

                def _get_value(self, create=False) -> int:
                    return self.lookup_value(
                        self._get_capability, Capability.Keys.value, create, default=None
                    )

                def __init__(self, value: providers.FactoryValue[_JSONDict] | _JSONDict | None):
                    super().__init__(value, bool)

                @property
                def enable(self):
                    return SimpleCapability(
                        self.lookup_factory(self.__get_value__, self.Keys.enable, default=_NO_JSON),
                        bool,
                    )

            class JSON(Cover.JSON, Picture.JSON, Task.JSON):
                """JSON"""

                supportFtpDirYM: Capability.JSON
                supportFtpEnable: Capability.JSON
                supportFtpVideoSwap: Capability.JSON
                supportFtpsEncrypt: Capability.JSON

            class Keys(Protocol):
                """Keys"""

                cover: "Capabilities.Supports.FTP.Cover.Keys"
                dir_YM: Final = "supportFtpDirYM"
                enable: Final = "supportFtpEnable"
                picture: "Capabilities.Supports.FTP.Picture.Keys"
                task: "Capabilities.Supports.FTP.Task.Keys"
                video_swap: Final = "supportFtpVideoSwap"
                ftps_encrypt: Final = "supportFtpsEncrypt"

            __slots__ = ()

            @property
            def cover(self):
                return self.Cover(self._factory)

            @property
            def dir_YM(self):
                return SimpleCapability(
                    self.lookup_factory(self.__get_value__, self.Keys.dir_YM, default=_NO_JSON),
                    bool,
                )

            @property
            def enable(self):
                return SimpleCapability(
                    self.lookup_factory(self.__get_value__, self.Keys.enable, default=_NO_JSON),
                    bool,
                )

            @property
            def picture(self):
                return self.Picture(self.__get_value__)

            @property
            def task(self):
                return self.Task(self.__get_value__)

            @property
            def video_swap(self):
                return SimpleCapability(
                    self.lookup_factory(self.__get_value__, self.Keys.video_swap, default=_NO_JSON),
                    bool,
                )

            @property
            def ftps_encrypt(self):
                return SimpleCapability(
                    self.lookup_factory(
                        self.__get_value__, self.Keys.ftps_encrypt, default=_NO_JSON
                    ),
                    bool,
                )

        class Record(providers.Value[_JSONDict], capabilities.Capabilities.Supports.Record):
            """Record"""

            class JSON(TypedDict):
                """JSON"""

                supportRecScheduleEnable: Capability.JSON
                supportRecordEnable: Capability.JSON

            class Keys(Protocol):
                """Keys"""

                schedule_enable: Final = "supportRecScheduleEnable"
                enable: Final = "supportRecordEnable"

            __slots__ = ()

            @property
            def schedule_enable(self):
                return SimpleCapability(
                    self.lookup_factory(
                        self.__get_value__, self.Keys.schedule_enable, default=_NO_JSON
                    ),
                    bool,
                )

            @property
            def enable(self):
                return SimpleCapability(
                    self.lookup_factory(self.__get_value__, self.Keys.enable, default=_NO_JSON),
                    bool,
                )

        class JSON(Audio.JSON, Buzzer.JSON, Email.JSON, FTP.JSON, Record.JSON):
            """JSON"""

            supportHttpEnable: Capability.JSON
            supportHttpsEnable: Capability.JSON
            supportOnvifEnable: Capability.JSON
            supportPushInterval: Capability.JSON
            supportRtmpEnable: Capability.JSON
            supportRtspEnable: Capability.JSON

        class Keys(Protocol):
            """Keys"""

            audio: "Capabilities.Supports.Audio.Keys"
            buzzer: "Capabilities.Supports.Buzzer.Keys"
            email: "Capabilities.Supports.Email.Keys"
            ftp: "Capabilities.Supports.FTP.Keys"
            record: "Capabilities.Supports.Record.Keys"

            http_enable: Final = "supportHttpEnable"
            https_enable: Final = "supportHttpsEnable"
            onvif_enable: Final = "supportOnvifEnable"
            push_interval: Final = "supportPushInterval"
            rtmp_enable: Final = "supportRtmpEnable"
            rtsp_enable: Final = "supportRtspEnable"

        __slots__ = ()

        @property
        def audio(self):
            return self.Audio(self.__get_value__)

        @property
        def buzzer(self):
            return self.Buzzer(self.__get_value__)

        @property
        def email(self):
            return self.Email(self.__get_value__)

        @property
        def ftp(self):
            return self.FTP(self.__get_value__)

        @property
        def http_enable(self):
            return SimpleCapability(
                self.lookup_factory(self.__get_value__, self.Keys.http_enable, default=_NO_JSON),
                bool,
            )

        @property
        def https_enable(self):
            return SimpleCapability(
                self.lookup_factory(self.__get_value__, self.Keys.https_enable, default=_NO_JSON),
                bool,
            )

        @property
        def onvif_enable(self):
            return SimpleCapability(
                self.lookup_factory(self.__get_value__, self.Keys.onvif_enable, default=_NO_JSON),
                bool,
            )

        @property
        def push_interval(self):
            return SimpleCapability(
                self.lookup_factory(self.__get_value__, self.Keys.push_interval, default=_NO_JSON),
                bool,
            )

        @property
        def record(self):
            return self.Record(self.__get_value__)

        @property
        def rtmp_enable(self):
            return SimpleCapability(
                self.lookup_factory(self.__get_value__, self.Keys.rtmp_enable, default=_NO_JSON),
                bool,
            )

        @property
        def rtsp_enable(self):
            return SimpleCapability(
                self.lookup_factory(self.__get_value__, self.Keys.rtsp_enable, default=_NO_JSON),
                bool,
            )

    class Wifi(SimpleCapability[bool], capabilities.Capabilities.Wifi):
        """WIFI"""

        class JSON(TypedDict):
            """JSON"""

            wifi: Capability.JSON
            wifiTest: Capability.JSON

        class Keys(Protocol):
            """Keys"""

            value: Final = "wifi"
            testable: Final = "wifiTest"

        __slots__ = ()

        def _get_capability(self, create=False) -> Capability.JSON:
            return self.lookup_value(self.__get_value__, self.Keys.value, create, default=_NO_JSON)

        def _get_permissions(self, create=False) -> int:
            return self.lookup_value(
                self._get_capability, Capability.Keys.permission, create, default=None
            )

        def _get_value(self, create=False) -> int:
            return self.lookup_value(
                self._get_capability, Capability.Keys.value, create, default=None
            )

        def __init__(self, value: providers.FactoryValue[_JSONDict] | _JSONDict | None):
            super().__init__(value, bool)

        @property
        def testable(self):
            return SimpleCapability(
                self.lookup_factory(self.__get_value__, self.Keys.testable, default=_NO_JSON),
                bool,
            )

    _BaseJSON = TypedDict("_BaseJSON", {"3g": Capability.JSON})

    class JSON(_BaseJSON, Alarm.JSON, Device.JSON, Email.JSON, FTP.JSON, Wifi.JSON):
        """JSON"""

        abilityChn: list[ChannelCapabilities.JSON]
        auth: Capability.JSON
        autoMaint: Capability.JSON
        cloudStorage: Capability.JSON
        customAudio: Capability.JSON
        dateFormat: Capability.JSON
        ddns: Capability.JSON
        disableAutoFocus: Capability.JSON
        disk: Capability.JSON
        display: Capability.JSON
        importCfg: Capability.JSON
        exportCfg: Capability.JSON
        hourFmt: Capability.JSON
        http: Capability.JSON
        httpFlv: Capability.JSON
        https: Capability.JSON
        ipcManager: Capability.JSON
        ledControl: Capability.JSON
        localLink: Capability.JSON
        log: Capability.JSON
        mediaPort: Capability.JSON
        ntp: Capability.JSON
        online: Capability.JSON
        onvif: Capability.JSON
        p2p: Capability.JSON
        performance: Capability.JSON
        pppoe: Capability.JSON
        push: Capability.JSON
        pushSchedule: Capability.JSON
        reboot: Capability.JSON
        restore: Capability.JSON
        rtmp: Capability.JSON
        rtsp: Capability.JSON
        scheduleVersion: Capability.JSON
        sdCard: Capability.JSON
        showQrCode: Capability.JSON
        simModule: Capability.JSON
        talk: Capability.JSON
        time: Capability.JSON
        tvSystem: Capability.JSON
        upgrade: Capability.JSON
        upnp: Capability.JSON
        user: Capability.JSON
        videoClip: Capability.JSON

    class Keys(Protocol):
        """Keys"""

        alarm: "Capabilities.Alarm.Keys"
        device: "Capabilities.Device.Keys"
        email: "Capabilities.Email.Keys"
        ftp: "Capabilities.FTP.Keys"
        wifi: "Capabilities.Wifi.Keys"

        three_g: Final = "3g"
        channels: Final = "abilityChn"
        auth: Final = "auth"
        auto_maintenance: Final = "autoMaint"
        cloud_storage: Final = "cloudStorage"
        custom_audio: Final = "customAudio"
        date_format: Final = "dateFormat"
        ddns: Final = "ddns"
        disable_autofocus: Final = "disableAutoFocus"
        disk: Final = "disk"
        display: Final = "display"
        config_import: Final = "importCfg"
        config_export: Final = "exportCfg"
        hour_format: Final = "hourFmt"
        http: Final = "http"
        http_flv: Final = "httpFlv"
        https: Final = "https"
        ipc_manager: Final = "ipcManager"
        led_control: Final = "ledControl"
        local_link: Final = "localLink"
        log: Final = "log"
        media_port: Final = "mediaPort"
        ntp: Final = "ntp"
        online: Final = "online"
        onvif: Final = "onvif"
        p2p: Final = "p2p"
        performance: Final = "performance"
        pppoe: Final = "pppoe"
        push: Final = "push"
        push_schedule: Final = "pushSchedule"
        reboot: Final = "reboot"
        restore: Final = "restore"
        rtmp: Final = "rtmp"
        rtsp: Final = "rtsp"
        schedule_version: Final = "scheduleVersion"
        sd_card: Final = "sdCard"
        show_qr_code: Final = "showQrCode"
        sim_module: Final = "simModule"
        talk: Final = "talk"
        time: Final = "time"
        tv_system: Final = "tvSystem"
        upgrade: Final = "upgrade"
        upnp: Final = "upnp"
        user: Final = "user"
        video_clip: Final = "videoClip"

    __slots__ = ()

    @property
    def three_g(self):
        return SimpleCapability(
            self.lookup_factory(self.__get_value__, self.Keys.three_g, default=_NO_JSON),
            bool,
        )

    @property
    def channels(self):
        """channels"""
        return _Channels(
            self.lookup_factory(self.__get_value__, self.Keys.channels, default=_NO_JSON)
        )

    @property
    def alarm(self):
        return self.Alarm(self.__get_value__)

    @property
    def auth(self):
        return SimpleCapability(
            self.lookup_factory(self.__get_value__, self.Keys.auth, default=_NO_JSON),
            bool,
        )

    @property
    def auto_maintenance(self):
        return SimpleCapability(
            self.lookup_factory(self.__get_value__, self.Keys.auto_maintenance, default=_NO_JSON),
            bool,
        )

    @property
    def cloud_storage(self):
        return FlagCapability(
            self.lookup_factory(self.__get_value__, self.Keys.cloud_storage, default=_NO_JSON),
            _CLOUDSTORAGE,
        )

    @property
    def custom_audio(self):
        return SimpleCapability(
            self.lookup_factory(self.__get_value__, self.Keys.custom_audio, default=_NO_JSON),
            bool,
        )

    @property
    def date_format(self):
        return SimpleCapability(
            self.lookup_factory(self.__get_value__, self.Keys.date_format, default=_NO_JSON),
            bool,
        )

    @property
    def ddns(self):
        return EnumCapability(
            self.lookup_factory(self.__get_value__, self.Keys.ddns, default=_NO_JSON), _DDNS
        )

    @property
    def device(self):
        return self.Device(self.__get_value__)

    @property
    def disable_autofocus(self):
        return SimpleCapability(
            self.lookup_factory(self.__get_value__, self.Keys.disable_autofocus, default=_NO_JSON),
            bool,
        )

    @property
    def disk(self):
        return SimpleCapability(
            self.lookup_factory(self.__get_value__, self.Keys.disk, default=_NO_JSON),
            bool,
        )

    @property
    def display(self):
        return SimpleCapability(
            self.lookup_factory(self.__get_value__, self.Keys.display, default=_NO_JSON),
            bool,
        )

    @property
    def email(self):
        return self.Email(self.__get_value__)

    @property
    def config_import(self):
        return SimpleCapability(
            self.lookup_factory(self.__get_value__, self.Keys.config_import, default=_NO_JSON),
            bool,
        )

    @property
    def config_export(self):
        return SimpleCapability(
            self.lookup_factory(self.__get_value__, self.Keys.config_export, default=_NO_JSON),
            bool,
        )

    @property
    def ftp(self):
        return self.FTP(self.__get_value__)

    @property
    def hour_format(self):
        """change hour format supported"""

        return SimpleCapability(
            self.lookup_factory(self.__get_value__, self.Keys.hour_format, default=_NO_JSON),
            bool,
        )

    @property
    def http(self):
        return SimpleCapability(
            self.lookup_factory(self.__get_value__, self.Keys.http, default=_NO_JSON),
            bool,
        )

    @property
    def http_flv(self):
        return SimpleCapability(
            self.lookup_factory(self.__get_value__, self.Keys.http_flv, default=_NO_JSON),
            bool,
        )

    @property
    def https(self):
        return SimpleCapability(
            self.lookup_factory(self.__get_value__, self.Keys.https, default=_NO_JSON),
            bool,
        )

    @property
    def ipc_manager(self):
        return SimpleCapability(
            self.lookup_factory(self.__get_value__, self.Keys.ipc_manager, default=_NO_JSON),
            bool,
        )

    @property
    def led_control(self):
        ledControl: Capability.JSON
        led_control: Final = "ledControl"
        return SimpleCapability(
            self.lookup_factory(self.__get_value__, led_control, default=_NO_JSON),
            bool,
        )

    @property
    def local_link(self):
        return SimpleCapability(
            self.lookup_factory(self.__get_value__, self.Keys.local_link, default=_NO_JSON),
            bool,
        )

    @property
    def log(self):
        return SimpleCapability(
            self.lookup_factory(self.__get_value__, self.Keys.log, default=_NO_JSON),
            bool,
        )

    @property
    def media_port(self):
        return SimpleCapability(
            self.lookup_factory(self.__get_value__, self.Keys.media_port, default=_NO_JSON),
            bool,
        )

    @property
    def ntp(self):
        return SimpleCapability(
            self.lookup_factory(self.__get_value__, self.Keys.ntp, default=_NO_JSON),
            bool,
        )

    @property
    def online(self):
        return SimpleCapability(
            self.lookup_factory(self.__get_value__, self.Keys.online, default=_NO_JSON),
            bool,
        )

    @property
    def onvif(self):
        return SimpleCapability(
            self.lookup_factory(self.__get_value__, self.Keys.onvif, default=_NO_JSON),
            bool,
        )

    @property
    def p2p(self):
        return SimpleCapability(
            self.lookup_factory(self.__get_value__, self.Keys.p2p, default=_NO_JSON),
            bool,
        )

    @property
    def performance(self):
        return SimpleCapability(
            self.lookup_factory(self.__get_value__, self.Keys.performance, default=_NO_JSON),
            bool,
        )

    @property
    def pppoe(self):
        return SimpleCapability(
            self.lookup_factory(self.__get_value__, self.Keys.pppoe, default=_NO_JSON),
            bool,
        )

    @property
    def push(self):
        return SimpleCapability(
            self.lookup_factory(self.__get_value__, self.Keys.push, default=_NO_JSON),
            bool,
        )

    @property
    def push_schedule(self):
        return SimpleCapability(
            self.lookup_factory(self.__get_value__, self.Keys.push_schedule, default=_NO_JSON),
            bool,
        )

    @property
    def reboot(self):
        return SimpleCapability(
            self.lookup_factory(self.__get_value__, self.Keys.reboot, default=_NO_JSON),
            bool,
        )

    @property
    def record(self):
        return self.Record(self.__get_value__)

    @property
    def restore(self):
        return SimpleCapability(
            self.lookup_factory(self.__get_value__, self.Keys.restore, default=_NO_JSON),
            bool,
        )

    @property
    def rtmp(self):
        return SimpleCapability(
            self.lookup_factory(self.__get_value__, self.Keys.rtmp, default=_NO_JSON),
            bool,
        )

    @property
    def rtsp(self):
        return SimpleCapability(
            self.lookup_factory(self.__get_value__, self.Keys.rtsp, default=_NO_JSON),
            bool,
        )

    @property
    def schedule_version(self):
        return EnumCapability(
            self.lookup_factory(self.__get_value__, self.Keys.schedule_version, default=_NO_JSON),
            _SCHEDULE_VERSION,
        )

    @property
    def sd_card(self):
        return SimpleCapability(
            self.lookup_factory(self.__get_value__, self.Keys.sd_card, default=_NO_JSON),
            bool,
        )

    @property
    def show_qr_code(self):
        return SimpleCapability(
            self.lookup_factory(self.__get_value__, self.Keys.show_qr_code, default=_NO_JSON),
            bool,
        )

    @property
    def sim_module(self):
        return SimpleCapability(
            self.lookup_factory(self.__get_value__, self.Keys.sim_module, default=_NO_JSON),
            bool,
        )

    @property
    def supports(self):
        return self.Supports(self.__get_value__)

    @property
    def talk(self):
        return SimpleCapability(
            self.lookup_factory(self.__get_value__, self.Keys.talk, default=_NO_JSON),
            bool,
        )

    @property
    def time(self):
        return EnumCapability(
            self.lookup_factory(self.__get_value__, self.Keys.time, default=_NO_JSON), _TIME
        )

    @property
    def tv_system(self):
        return SimpleCapability(
            self.lookup_factory(self.__get_value__, self.Keys.tv_system, default=_NO_JSON),
            bool,
        )

    @property
    def upgrade(self):
        return EnumCapability(
            self.lookup_factory(self.__get_value__, self.Keys.upgrade, default=_NO_JSON),
            _UPGRADE,
        )

    @property
    def upnp(self):
        return SimpleCapability(
            self.lookup_factory(self.__get_value__, self.Keys.upnp, default=_NO_JSON),
            bool,
        )

    @property
    def user(self):
        return SimpleCapability(
            self.lookup_factory(self.__get_value__, self.Keys.user, default=_NO_JSON),
            bool,
        )

    @property
    def video_clip(self):
        return EnumCapability(
            self.lookup_factory(self.__get_value__, self.Keys.video_clip, default=_NO_JSON),
            _VIDEO_CLIP,
        )

    @property
    def wifi(self):
        return self.Wifi(self.__get_value__)


class UpdatableCapabilities(Capabilities):
    """Updatatable Capabilities"""

    def update(self, value: Capabilities):
        """Update underlying values"""
        if not isinstance(value, Capabilities):
            raise ValueError("Must provide a Capabilities object")
        self.__set_value__(value.__get_value__())
