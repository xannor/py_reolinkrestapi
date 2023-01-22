"""System capabilities"""

from enum import Flag
from typing import (
    ClassVar,
    Final,
    Mapping,
    Protocol,
    TypeAlias,
    TypedDict,
    get_args,
    overload,
)
from typing_extensions import TypeVar

from async_reolink.api.system import capabilities

from .._utilities.providers import value as providers
from .._utilities.descriptors import instance_or_classproperty
from .._utilities.enum import FlagMap, EnumMap

_JSONDict: TypeAlias = dict[str, any]

# pylint: disable=too-few-public-methods
# pylint: disable=missing-function-docstring

_defaults: dict[type, any] = {None: 0, int: 0, bool: False, str: ""}

_T = TypeVar("_T", infer_variance=True)

_F = TypeVar("_F", bound=Flag)

_Permissions = FlagMap(
    {
        capabilities.Permissions.OPTION: 1,
        capabilities.Permissions.WRITE: 2,
        capabilities.Permissions.READ: 4,
    }
)

_MISSING_VALUE: Final = ...


class _NoKey:
    ...


_MISSING_KEY: Final = _NoKey()

_CT = TypeVar("_CT", infer_variance=True, default=int)


class Capability(providers.Value[_JSONDict], capabilities.Capability[_CT]):
    """Capability"""

    class JSON(TypedDict):
        """JSON"""

        ver: int
        permit: int

    class Keys(Protocol):
        """Keys"""

        value: Final = "ver"
        permission: Final = "permit"

    @instance_or_classproperty
    def Type(self):
        return self.__type

    @Type.class_getter
    def Type(cls):
        args = get_args(cls)
        if len(args) > 0:
            return args[0]
        return int

    Permissions: ClassVar[type[capabilities.Permissions]] = capabilities.Permissions

    __slots__ = ("__type", "__map")

    def __init__(
        self,
        value: providers.FactoryValue[_JSONDict] | _JSONDict | None,
        __type: type[_CT] | EnumMap[_CT, int] | FlagMap[_CT, int] = _MISSING_VALUE,
        /,
        **kwargs: any,
    ) -> None:
        super().__init__(value, **kwargs)
        # self._get_value: providers.FactoryValue[int] = self.lookup_factory(
        #     self.__get_value__, self.Keys.value, default=_MISSING_KEY
        # )
        # self._get_permissions: providers.FactoryValue[int] = self.lookup_factory(
        #     self.__get_value__, self.Keys.permission, default=_MISSING_KEY
        # )
        if __type in {_MISSING_VALUE, None}:
            __type = type(self).Type
        if isinstance(__type, EnumMap):
            self.__map = __type
            __type = self.__map.Enum
        elif isinstance(__type, FlagMap):
            self.__map = __type
            __type = self.__map.Flag
        else:
            self.__map = None

        self.__type: type[_T] = __type

    __get_value__: providers.FactoryValue[JSON]

    def _get_value(self, create=False) -> int:
        return self.lookup_value(
            self.__get_value__, self.Keys.value, create=create, default=_MISSING_KEY
        )

    @property
    def _raw_value(self):
        if (value := self._get_value()) is None or value is _MISSING_KEY or value is _MISSING_VALUE:
            return None
        return value

    @property
    def value(self) -> _T:
        __type = self.Type
        if (value := self._get_value()) is _MISSING_KEY:
            if (value := _defaults.get(self.Type, _MISSING_VALUE)) is _MISSING_VALUE:
                if isinstance(self.__map, EnumMap):
                    value = self.__map.DEFAULT
                elif isinstance(self.__map, FlagMap):
                    value = self.__map.NONE
                else:
                    value = __type(0)
                _defaults[__type] = value
        return self.__type(value)

    def _get_permissions(self, create=False) -> int:
        return self.lookup_value(
            self.__get_value__, self.Keys.permission, create=create, default=_MISSING_KEY
        )

    @property
    def permissions(self):
        if (value := self._get_permissions()) is _MISSING_KEY:
            return _Permissions.NONE
        return _Permissions(value)

    def __bool__(self):
        if (perms := self.permissions) is None or capabilities.Permissions.READ not in perms:
            return False
        return bool(self._raw_value)

    def __index__(self):
        if (perms := self.permissions) is None or capabilities.Permissions.READ not in perms:
            return 0
        return self._raw_value or 0

    def __int__(self):
        if (perms := self.permissions) is None or capabilities.Permissions.READ not in perms:
            return 0
        return self._raw_value or 0

    def __str__(self):
        if (perms := self.permissions) is None or capabilities.Permissions.READ not in perms:
            return ""
        return str(self.value)

    def __eq__(self, __o: object) -> bool:
        if hasattr(__o, "__index__"):
            return self._raw_value == __o.__index__()
        return self.value == __o


_CloudStorage: Final = FlagMap(
    {
        capabilities.CloudStorage.UPLOAD: 1 << 0,
        capabilities.CloudStorage.CONFIG: 1 << 1,
        capabilities.CloudStorage.DEPLOY: 1 << 3,
    }
)

_DayNight: Final = EnumMap(
    {
        capabilities.DayNight.DAY_NIGHT: 1,
        capabilities.DayNight.THRESHOLD: 2,
    }
)

_DDns: Final = EnumMap(
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

_Email: Final = EnumMap(
    {
        capabilities.Email.JPEG: 1,
        capabilities.Email.VIDEO_JPEG: 2,
        capabilities.Email.VIDEO_JPEG_NICK: 3,
    }
)

_EncodingType: Final = EnumMap(
    {
        capabilities.EncodingType.H264: 0,
        capabilities.EncodingType.H265: 1,
    }
)

_Floodlight: Final = EnumMap(
    {
        capabilities.FloodLight.WHITE: 1,
        capabilities.FloodLight.AUTO: 2,
    }
)

_FTP: Final = EnumMap(
    {
        capabilities.Ftp.STREAM: 1,
        capabilities.Ftp.JPEG_STREAM: 2,
        capabilities.Ftp.MODE: 3,
        capabilities.Ftp.JPEG_STREAM_MODE: 4,
        capabilities.Ftp.STREAM_MODE_TYPE: 5,
        capabilities.Ftp.JPEG_STREAM_MODE_TYPE: 6,
    }
)

_Live: Final = EnumMap(
    {
        capabilities.Live.MAIN_EXTERN_SUB: 1,
        capabilities.Live.MAIN_SUB: 2,
    }
)

_OSD: Final = EnumMap(
    {
        capabilities.Osd.SUPPORTED: 1,
        capabilities.Osd.DISTINCT: 2,
    }
)

_PtzControl: Final = EnumMap(
    {
        capabilities.PTZControl.ZOOM: 1,
        capabilities.PTZControl.ZOOM_FOCUS: 2,
    }
)

_PtzDirection: Final = EnumMap(
    {
        capabilities.PTZDirection.EIGHT_AUTO: 0,
        capabilities.PTZDirection.FOUR_NO_AUTO: 1,
    }
)

_PtzType: Final = EnumMap(
    {
        capabilities.PTZType.AF: 1,
        capabilities.PTZType.PTZ: 2,
        capabilities.PTZType.PT: 3,
        capabilities.PTZType.BALL: 4,
        capabilities.PTZType.PTZ_NO_SPEED: 5,
    }
)

_RecordSchedule: Final = EnumMap(
    {
        capabilities.RecordSchedule.MOTION: 1,
        capabilities.RecordSchedule.MOTION_LIVE: 2,
    }
)

_ScheduleVersion: Final = EnumMap(
    {
        capabilities.ScheduleVersion.BASIC: 0,
        capabilities.ScheduleVersion.V20: 1,
    }
)


_Time: Final = EnumMap(
    {
        capabilities.Time.SUNDAY: 1,
        capabilities.Time.ANYDAY: 2,
    }
)


_Upgrade: Final = EnumMap(
    {
        capabilities.Upgrade.MANUAL: 1,
        capabilities.Upgrade.ONLINE: 2,
    }
)


_VideoClip: Final = EnumMap(
    {
        capabilities.VideoClip.FIXED: 1,
        capabilities.VideoClip.MOD: 2,
    }
)


class ChannelCapabilities(providers.Value[_JSONDict], capabilities.ChannelCapabilities):
    """Channel Capabilities"""

    class AI(providers.Value[_JSONDict], capabilities.ChannelCapabilities.AI):
        """AI"""

        class Track(providers.Value[_JSONDict], capabilities.ChannelCapabilities.AI.Track):
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

            @property
            def _value(self):
                return Capability(
                    self.lookup_factory(self.__get_value__, self.Keys.value, default=None), bool
                )

            def __bool__(self):
                return self._value.__bool__()

            def __index__(self):
                return self._value.__index__()

            def __int__(self):
                return self._value.__int__()

            def __str__(self):
                return self._value.__str__()

            def __eq__(self, __o: object):
                return self._value.__eq__(__o)

            @property
            def value(self):
                return self._value.value

            @property
            def permissions(self):
                return self._value.permissions

            @property
            def pet(self):
                return Capability(
                    self.lookup_factory(self.__get_value__, self.Keys.pet, default=None),
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
            return Capability(
                self.lookup_factory(self.__get_value__, self.Keys.audio, default=None), bool
            )

        @property
        def io_in(self):
            return Capability(
                self.lookup_factory(self.__get_value__, self.Keys.io_in, default=None), bool
            )

        @property
        def io_out(self):
            return Capability(
                self.lookup_factory(self.__get_value__, self.Keys.io_out, default=None),
                bool,
            )

        @property
        def motion(self):
            return Capability(
                self.lookup_factory(self.__get_value__, self.Keys.motion, default=None),
                bool,
            )

        @property
        def rf(self):
            return Capability(
                self.lookup_factory(self.__get_value__, self.Keys.rf, default=None), bool
            )

    class ISP(providers.Value[_JSONDict], capabilities.ChannelCapabilities.ISP):
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

        @property
        def _value(self):
            return Capability(
                self.lookup_factory(self.__get_value__, self.Keys.value, default=None), bool
            )

        def __bool__(self):
            return self._value.__bool__()

        def __index__(self):
            return self._value.__index__()

        def __int__(self):
            return self._value.__int__()

        def __str__(self):
            return self._value.__str__()

        def __eq__(self, __o: object):
            return self._value.__eq__(__o)

        @property
        def value(self):
            return self._value.value

        @property
        def permissions(self):
            return self._value.permissions

        @property
        def threeDnr(self):
            return Capability(
                self.lookup_factory(self.__get_value__, self.Keys.threeDnr, default=None),
                bool,
            )

        @property
        def antiflicker(self):
            return Capability(
                self.lookup_factory(self.__get_value__, self.Keys.antiflicker, default=None),
                bool,
            )

        @property
        def backlight(self):
            return Capability(
                self.lookup_factory(self.__get_value__, self.Keys.backlight, default=None),
                bool,
            )

        @property
        def bright(self):
            return Capability(
                self.lookup_factory(self.__get_value__, self.Keys.bright, default=None),
                bool,
            )

        @property
        def contrast(self):
            return Capability(
                self.lookup_factory(self.__get_value__, self.Keys.contrast, default=None),
                bool,
            )

        @property
        def day_night(self):
            return Capability(
                self.lookup_factory(self.__get_value__, self.Keys.day_night, default=None),
                _DayNight,
            )

        @property
        def exposure_mode(self):
            return Capability(
                self.lookup_factory(self.__get_value__, self.Keys.exposure_mode, default=None),
                bool,
            )

        @property
        def flip(self):
            return Capability(
                self.lookup_factory(self.__get_value__, self.Keys.flip, default=None), bool
            )

        @property
        def hue(self):
            return Capability(
                self.lookup_factory(self.__get_value__, self.Keys.hue, default=None), bool
            )

        @property
        def mirror(self):
            return Capability(
                self.lookup_factory(self.__get_value__, self.Keys.mirror, default=None),
                bool,
            )

        @property
        def satruation(self):
            return Capability(
                self.lookup_factory(self.__get_value__, self.Keys.satruation, default=None),
                bool,
            )

        @property
        def sharpen(self):
            return Capability(
                self.lookup_factory(self.__get_value__, self.Keys.sharpen, default=None),
                bool,
            )

        @property
        def white_balance(self):
            return Capability(
                self.lookup_factory(self.__get_value__, self.Keys.white_balance, default=None),
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
                return Capability(
                    self.lookup_factory(self.__get_value__, self.Keys.audo, default=None),
                    bool,
                )

            @property
            def record(self):
                return Capability(
                    self.lookup_factory(self.__get_value__, self.Keys.record, default=None),
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
            return Capability(
                self.lookup_factory(self.__get_value__, self.Keys.with_pir, default=None),
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
            return Capability(
                self.lookup_factory(self.__get_value__, self.Keys.control, default=None),
                _PtzControl,
            )

        @property
        def direction(self):
            return Capability(
                self.lookup_factory(self.__get_value__, self.Keys.direction, default=None),
                _PtzDirection,
            )

        @property
        def patrol(self):
            return Capability(
                self.lookup_factory(self.__get_value__, self.Keys.patrol, default=None),
                bool,
            )

        @property
        def preset(self):
            return Capability(
                self.lookup_factory(self.__get_value__, self.Keys.preset, default=None),
                bool,
            )

        @property
        def tattern(self):
            return Capability(
                self.lookup_factory(self.__get_value__, self.Keys.tattern, default=None),
                bool,
            )

        @property
        def type(self):
            return Capability(
                self.lookup_factory(self.__get_value__, self.Keys.type, default=None),
                _PtzType,
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
            return Capability(
                self.lookup_factory(self.__get_value__, self.Keys.config, default=None),
                bool,
            )

        @property
        def download(self):
            return Capability(
                self.lookup_factory(self.__get_value__, self.Keys.download, default=None),
                bool,
            )

        @property
        def replay(self):
            return Capability(
                self.lookup_factory(self.__get_value__, self.Keys.replay, default=None),
                bool,
            )

        @property
        def schedule(self):
            return Capability(
                self.lookup_factory(self.__get_value__, self.Keys.schedule, default=None),
                _RecordSchedule,
            )

    class Supports(providers.Value[_JSONDict], capabilities.ChannelCapabilities.Supports):
        """Supports"""

        class AI(
            providers.Value[_JSONDict],
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

            @property
            def _value(self):
                return Capability(
                    self.lookup_factory(self.__get_value__, self.Keys.value, default=None),
                    bool,
                )

            def __bool__(self):
                return self._value.__bool__()

            def __index__(self):
                return self._value.__index__()

            def __int__(self):
                return self._value.__int__()

            def __str__(self):
                return self._value.__str__()

            def __eq__(self, __o: object):
                return self._value.__eq__(__o)

            @property
            def value(self):
                return self._value.value

            @property
            def permissions(self):
                return self._value.permissions

            @property
            def animal(self):
                return Capability(
                    self.lookup_factory(self.__get_value__, self.Keys.animal, default=None),
                    bool,
                )

            @property
            def detect_config(self):
                return Capability(
                    self.lookup_factory(self.__get_value__, self.Keys.detect_config, default=None),
                    bool,
                )

            @property
            def pet(self):
                return Capability(
                    self.lookup_factory(self.__get_value__, self.Keys.pet, default=None),
                    bool,
                )

            @property
            def face(self):
                return Capability(
                    self.lookup_factory(self.__get_value__, self.Keys.face, default=None),
                    bool,
                )

            @property
            def people(self):
                return Capability(
                    self.lookup_factory(self.__get_value__, self.Keys.people, default=None),
                    bool,
                )

            @property
            def sensitivity(self):
                return Capability(
                    self.lookup_factory(self.__get_value__, self.Keys.sensitivity, default=None),
                    bool,
                )

            @property
            def stay_time(self):
                return Capability(
                    self.lookup_factory(self.__get_value__, self.Keys.stay_time, default=None),
                    bool,
                )

            @property
            def target_size(self):
                return Capability(
                    self.lookup_factory(self.__get_value__, self.Keys.target_size, default=None),
                    bool,
                )

            @property
            def track_classify(self):
                return Capability(
                    self.lookup_factory(self.__get_value__, self.Keys.track_classify, default=None),
                    bool,
                )

            @property
            def vehicle(self):
                return Capability(
                    self.lookup_factory(self.__get_value__, self.Keys.vehicle, default=None),
                    bool,
                )

            @property
            def adjust(self):
                return Capability(
                    self.lookup_factory(self.__get_value__, self.Keys.adjust, default=None),
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
                return Capability(
                    self.lookup_factory(self.__get_value__, self.Keys.brightness, default=None),
                    bool,
                )

            @property
            def intelligent(self):
                return Capability(
                    self.lookup_factory(self.__get_value__, self.Keys.intelligent, default=None),
                    bool,
                )

            @property
            def keep_on(self):
                return Capability(
                    self.lookup_factory(self.__get_value__, self.Keys.keep_on, default=None),
                    bool,
                )

            @property
            def schedule(self):
                return Capability(
                    self.lookup_factory(self.__get_value__, self.Keys.schedule, default=None),
                    bool,
                )

            @property
            def switch(self):
                return Capability(
                    self.lookup_factory(self.__get_value__, self.Keys.switch, default=None),
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
            return Capability(
                self.lookup_factory(self.__get_value__, self.Keys.gop, default=None), bool
            )

        @property
        def motion_detection(self):
            return Capability(
                self.lookup_factory(self.__get_value__, self.Keys.motion_detection, default=None),
                bool,
            )

        @property
        def ptz_check(self):
            return Capability(
                self.lookup_factory(self.__get_value__, self.Keys.ptz_check, default=None),
                bool,
            )

        @property
        def threshold_adjust(self):
            return Capability(
                self.lookup_factory(self.__get_value__, self.Keys.threshold_adjust, default=None),
                bool,
            )

        @property
        def white_dark(self):
            return Capability(
                self.lookup_factory(self.__get_value__, self.Keys.white_dark, default=None),
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
        return Capability(
            self.lookup_factory(self.__get_value__, self.Keys.battery, default=None), bool
        )

    @property
    def battery_analysis(self):
        return Capability(
            self.lookup_factory(self.__get_value__, self.Keys.battery_analysis, default=None),
            bool,
        )

    @property
    def camera_mode(self):
        return Capability(
            self.lookup_factory(self.__get_value__, self.Keys.camera_mode, default=None),
            bool,
        )

    @property
    def disable_autofocus(self):
        return Capability(
            self.lookup_factory(self.__get_value__, self.Keys.disable_autofocus, default=None),
            bool,
        )

    @property
    def enc(self):
        return Capability(
            self.lookup_factory(self.__get_value__, self.Keys.enc, default=None), bool
        )

    @property
    def floodlight(self):
        return Capability(
            self.lookup_factory(self.__get_value__, self.Keys.floodlight, default=None),
            _Floodlight,
        )

    @property
    def ftp(self):
        return Capability(
            self.lookup_factory(self.__get_value__, self.Keys.ftp, default=None), _FTP
        )

    @property
    def image(self):
        return Capability(
            self.lookup_factory(self.__get_value__, self.Keys.image, default=None), bool
        )

    @property
    def indicator_light(self):
        return Capability(
            self.lookup_factory(self.__get_value__, self.Keys.indicator_light, default=None),
            bool,
        )

    @property
    def isp(self):
        return self.ISP(self.__get_value__)

    @property
    def led_control(self):
        return Capability(
            self.lookup_factory(self.__get_value__, self.Keys.led_control, default=None),
            bool,
        )

    @property
    def live(self):
        return Capability(self.lookup_factory(self.__get_value__, self.Keys.live), _Live)

    @property
    def main_encoding(self):
        return Capability(
            self.lookup_factory(self.__get_value__, self.Keys.main_encoding, default=None),
            _EncodingType,
        )

    @property
    def mask(self):
        return Capability(
            self.lookup_factory(self.__get_value__, self.Keys.mask, default=None), bool
        )

    @property
    def motion_detection(self):
        return self.MD(self.__get_value__)

    @property
    def osd(self):
        return Capability(
            self.lookup_factory(self.__get_value__, self.Keys.osd, default=None), _OSD
        )

    @property
    def power_led(self):
        return Capability(
            self.lookup_factory(self.__get_value__, self.Keys.power_led, default=None), bool
        )

    @property
    def ptz(self):
        return self.PTZ(self.__get_value__)

    @property
    def record(self):
        return self.Record(self.__get_value__)

    @property
    def shelter_config(self):
        return Capability(
            self.lookup_factory(self.__get_value__, self.Keys.shelter_config, default=None),
            bool,
        )

    @property
    def snap(self):
        return Capability(
            self.lookup_factory(self.__get_value__, self.Keys.snap, default=None), bool
        )

    @property
    def supports(self):
        return self.Supports(self.__get_value__)

    @property
    def video_clip(self):
        return Capability(
            self.lookup_factory(self.__get_value__, self.Keys.video_clip, default=None),
            _VideoClip,
        )

    @property
    def watermark(self):
        return Capability(
            self.lookup_factory(self.__get_value__, self.Keys.watermark, default=None), bool
        )

    @property
    def white_balance(self):
        return Capability(
            self.lookup_factory(self.__get_value__, self.Keys.white_balance, default=None),
            bool,
        )


class _Channels(providers.Value[list[_JSONDict]], Mapping[int, ChannelCapabilities]):
    """Channels"""

    __slots__ = ()

    def __getitem__(self, __k: int):
        return ChannelCapabilities(self.lookup_factory(self.__get_value__, __k, default=None))

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
                return Capability(
                    self.lookup_factory(self.__get_value__, self.Keys.error, default=None),
                    bool,
                )

            @property
            def full(self):
                return Capability(
                    self.lookup_factory(self.__get_value__, self.Keys.full, default=None),
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
            return Capability(
                self.lookup_factory(self.__get_value__, self.Keys.audio, default=None), bool
            )

        @property
        def disconnect(self):
            return Capability(
                self.lookup_factory(self.__get_value__, self.Keys.disconnect, default=None),
                bool,
            )

        @property
        def hdd(self):
            return self.HDD(self.__get_value__)

        @property
        def ip_conflict(self):
            return Capability(
                self.lookup_factory(self.__get_value__, self.Keys.ip_conflict, default=None),
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
            return Capability(
                self.lookup_factory(self.__get_value__, self.Keys.info, default=None), bool
            )

        @property
        def name(self):
            return Capability(
                self.lookup_factory(self.__get_value__, self.Keys.name, default=None), bool
            )

    class Email(providers.Value[_JSONDict], capabilities.Capabilities.Email):
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

        @property
        def _value(self):
            return Capability(
                self.lookup_factory(self.__get_value__, self.Keys.value, default=None),
                _Email,
            )

        @property
        def value(self):
            return self._value.value

        @property
        def permissions(self):
            return self._value.permissions

        def __bool__(self):
            return bool(self.value)

        @property
        def interval(self):
            return Capability(
                self.lookup_factory(self.__get_value__, self.Keys.interval, default=None),
                bool,
            )

        @property
        def schedule(self):
            return Capability(
                self.lookup_factory(self.__get_value__, self.Keys.schedule, default=None),
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
                return Capability(
                    self.lookup_factory(self.__get_value__, self.Keys.ext, default=None),
                    bool,
                )

            @property
            def sub(self):
                return Capability(
                    self.lookup_factory(self.__get_value__, self.Keys.sub, default=None),
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
            return Capability(
                self.lookup_factory(self.__get_value__, self.Keys.auto_dir, default=None),
                bool,
            )

        @property
        def stream(self):
            return self.Stream(self.__get_value__)

        @property
        def picture(self):
            return Capability(
                self.lookup_factory(self.__get_value__, self.Keys.picture, default=None),
                bool,
            )

        @property
        def test(self):
            return Capability(
                self.lookup_factory(self.__get_value__, self.Keys.test, default=None), bool
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
            return Capability(
                self.lookup_factory(
                    self.__get_value__, self.Keys.extension_time_list, default=None
                ),
                bool,
            )

        @property
        def overwrite(self):
            return Capability(
                self.lookup_factory(self.__get_value__, self.Keys.overwrite, default=None),
                bool,
            )

        @property
        def pack_duration(self):
            return Capability(
                self.lookup_factory(self.__get_value__, self.Keys.pack_duration, default=None),
                bool,
            )

        @property
        def pre_record(self):
            return Capability(
                self.lookup_factory(self.__get_value__, self.Keys.pre_record, default=None),
                bool,
            )

    class Supports(providers.Value[_JSONDict], capabilities.Capabilities.Supports):
        """Supports"""

        class Audio(providers.Value[_JSONDict], capabilities.Capabilities.Supports.Audio):
            """Audio"""

            class Alarm(
                providers.Value[_JSONDict],
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

                _provided_value: JSON

                @property
                def _value(self):
                    return Capability(
                        self.lookup_factory(self.__get_value__, self.Keys.value, default=None),
                        bool,
                    )

                @property
                def value(self):
                    return self._value.value

                @property
                def permissions(self):
                    return self._value.permissions

                def __bool__(self):
                    return self.value

                @property
                def enable(self):
                    return Capability(
                        self.lookup_factory(self.__get_value__, self.Keys.enable, default=None),
                        bool,
                    )

                @property
                def schedule(self):
                    return Capability(
                        self.lookup_factory(self.__get_value__, self.Keys.schedule, default=None),
                        bool,
                    )

                @property
                def task_enable(self):
                    return Capability(
                        self.lookup_factory(
                            self.__get_value__, self.Keys.task_enable, default=None
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

        class Buzzer(providers.Value[_JSONDict], capabilities.Capabilities.Supports.Buzzer):
            """Buzzer"""

            __slots__ = ()

            class Task(
                providers.Value[_JSONDict],
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

                _provided_value: JSON

                @property
                def _value(self):
                    return Capability(
                        self.lookup_factory(self.__get_value__, self.Keys.value, default=None),
                        bool,
                    )

                @property
                def value(self):
                    return self._value.value

                @property
                def permissions(self):
                    return self._value.permissions

                def __bool__(self):
                    return self.value

                @property
                def enable(self):
                    return Capability(
                        self.lookup_factory(self.__get_value__, self.Keys.enable, default=None),
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

            @property
            def _value(self):
                return Capability(
                    self.lookup_factory(self.__get_value__, self.Keys.value, default=None), bool
                )

            @property
            def task(self):
                return self.Task(self.__get_value__)

            @property
            def value(self):
                """value"""
                return self._value.value

            @property
            def permissions(self):
                """permissions"""
                return self._value.permissions

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
                return Capability(
                    self.lookup_factory(self.__get_value__, self.Keys.enable, default=None),
                    bool,
                )

            @property
            def task_enable(self):
                return Capability(
                    self.lookup_factory(self.__get_value__, self.Keys.task_enable),
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
                    return Capability(
                        self.lookup_factory(self.__get_value__, self.Keys.picture),
                        bool,
                    )

                @property
                def video(self):
                    return Capability(
                        self.lookup_factory(self.__get_value__, self.Keys.video),
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
                    return Capability(
                        self.lookup_factory(self.__get_value__, self.Keys.capture_mode),
                        bool,
                    )

                @property
                def custom_resolution(self):
                    return Capability(
                        self.lookup_factory(self.__get_value__, self.Keys.custom_resolution),
                        bool,
                    )

                @property
                def swap(self):
                    return Capability(
                        self.lookup_factory(self.__get_value__, self.Keys.swap),
                        bool,
                    )

            class Task(
                providers.Value[_JSONDict],
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

                @property
                def _value(self):
                    return Capability(
                        self.lookup_factory(self.__get_value__, self.Keys.value),
                        bool,
                    )

                @property
                def value(self):
                    return self._value.value

                @property
                def permissions(self):
                    return self._value.permissions

                def __bool__(self):
                    return bool(self.value)

                @property
                def enable(self):
                    return Capability(
                        self.lookup_factory(self.__get_value__, self.Keys.enable),
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
                return Capability(
                    self.lookup_factory(self.__get_value__, self.Keys.dir_YM),
                    bool,
                )

            @property
            def enable(self):
                return Capability(
                    self.lookup_factory(self.__get_value__, self.Keys.enable),
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
                return Capability(
                    self.lookup_factory(self.__get_value__, self.Keys.video_swap),
                    bool,
                )

            @property
            def ftps_encrypt(self):
                return Capability(
                    self.lookup_factory(self.__get_value__, self.Keys.ftps_encrypt),
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
                return Capability(
                    self.lookup_factory(self.__get_value__, self.Keys.schedule_enable),
                    bool,
                )

            @property
            def enable(self):
                return Capability(
                    self.lookup_factory(self.__get_value__, self.Keys.enable),
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
            return Capability(
                self.lookup_factory(self.__get_value__, self.Keys.http_enable),
                bool,
            )

        @property
        def https_enable(self):
            return Capability(
                self.lookup_factory(self.__get_value__, self.Keys.https_enable),
                bool,
            )

        @property
        def onvif_enable(self):
            return Capability(
                self.lookup_factory(self.__get_value__, self.Keys.onvif_enable),
                bool,
            )

        @property
        def push_interval(self):
            return Capability(
                self.lookup_factory(self.__get_value__, self.Keys.push_interval),
                bool,
            )

        @property
        def record(self):
            return self.Record(self.__get_value__)

        @property
        def rtmp_enable(self):
            return Capability(
                self.lookup_factory(self.__get_value__, self.Keys.rtmp_enable),
                bool,
            )

        @property
        def rtsp_enable(self):
            return Capability(
                self.lookup_factory(self.__get_value__, self.Keys.rtsp_enable),
                bool,
            )

    class Wifi(providers.Value[_JSONDict], capabilities.Capabilities.Wifi):
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

        @property
        def _value(self):
            return Capability(
                self.lookup_factory(self.__get_value__, self.Keys.value, default=None), bool
            )

        @property
        def value(self):
            return self._value.value

        @property
        def permissions(self):
            return self._value.permissions

        def __bool__(self):
            return bool(self.value)

        @property
        def testable(self):
            return Capability(
                self.lookup_factory(self.__get_value__, self.Keys.testable),
                bool,
            )

    _BaseJSON = TypedDict("_BaseJSON", {"3g": Capability.JSON})

    class JSON(_BaseJSON, Alarm.JSON, Device.JSON, Email.JSON, FTP.JSON, Wifi.JSON):
        """JSON"""

        abilityChn: list[ChannelCapabilities.JSON]
        auth: Capability.JSON
        autoMaint: Capability.JSON
        cloudStorage: Capability.JSON
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
        return Capability(
            self.lookup_factory(self.__get_value__, self.Keys.three_g, default=None), bool
        )

    @property
    def channels(self):
        """channels"""
        return _Channels(self.lookup_factory(self.__get_value__, self.Keys.channels))

    @property
    def alarm(self):
        return self.Alarm(self.__get_value__)

    @property
    def auth(self):
        return Capability(
            self.lookup_factory(self.__get_value__, self.Keys.auth, default=None), bool
        )

    @property
    def auto_maintenance(self):
        return Capability(
            self.lookup_factory(self.__get_value__, self.Keys.auto_maintenance),
            bool,
        )

    @property
    def cloud_storage(self):
        return Capability(
            self.lookup_factory(self.__get_value__, self.Keys.cloud_storage),
            _CloudStorage,
        )

    @property
    def custom_audio(self):
        return Capability(
            self.lookup_factory(self.__get_value__, self.Keys.custom_audio),
            bool,
        )

    @property
    def date_format(self):
        return Capability(
            self.lookup_factory(self.__get_value__, self.Keys.date_format),
            bool,
        )

    @property
    def ddns(self):
        return Capability(self.lookup_factory(self.__get_value__, self.Keys.ddns), _DDns)

    @property
    def device(self):
        return self.Device(self.__get_value__)

    @property
    def disable_autofocus(self):
        return Capability(
            self.lookup_factory(self.__get_value__, self.Keys.disable_autofocus),
            bool,
        )

    @property
    def disk(self):
        return Capability(
            self.lookup_factory(self.__get_value__, self.Keys.disk, default=None), bool
        )

    @property
    def display(self):
        return Capability(
            self.lookup_factory(self.__get_value__, self.Keys.display, default=None), bool
        )

    @property
    def email(self):
        return self.Email(self.__get_value__)

    @property
    def config_import(self):
        return Capability(
            self.lookup_factory(self.__get_value__, self.Keys.config_import),
            bool,
        )

    @property
    def config_export(self):
        return Capability(
            self.lookup_factory(self.__get_value__, self.Keys.config_export),
            bool,
        )

    @property
    def ftp(self):
        return self.FTP(self.__get_value__)

    @property
    def hour_format(self):
        """change hour format supported"""

        return Capability(
            self.lookup_factory(self.__get_value__, self.Keys.hour_format),
            bool,
        )

    @property
    def http(self):
        return Capability(
            self.lookup_factory(self.__get_value__, self.Keys.http, default=None), bool
        )

    @property
    def http_flv(self):
        return Capability(
            self.lookup_factory(self.__get_value__, self.Keys.http_flv, default=None), bool
        )

    @property
    def https(self):
        return Capability(
            self.lookup_factory(self.__get_value__, self.Keys.https, default=None), bool
        )

    @property
    def ipc_manager(self):
        return Capability(
            self.lookup_factory(self.__get_value__, self.Keys.ipc_manager),
            bool,
        )

    @property
    def led_control(self):
        ledControl: Capability.JSON
        led_control: Final = "ledControl"
        return Capability(self.lookup_factory(self.__get_value__, led_control, default=None), bool)

    @property
    def local_link(self):
        return Capability(
            self.lookup_factory(self.__get_value__, self.Keys.local_link),
            bool,
        )

    @property
    def log(self):
        return Capability(
            self.lookup_factory(self.__get_value__, self.Keys.log, default=None), bool
        )

    @property
    def media_port(self):
        return Capability(
            self.lookup_factory(self.__get_value__, self.Keys.media_port),
            bool,
        )

    @property
    def ntp(self):
        return Capability(
            self.lookup_factory(self.__get_value__, self.Keys.ntp, default=None), bool
        )

    @property
    def online(self):
        return Capability(
            self.lookup_factory(self.__get_value__, self.Keys.online, default=None), bool
        )

    @property
    def onvif(self):
        return Capability(
            self.lookup_factory(self.__get_value__, self.Keys.onvif, default=None), bool
        )

    @property
    def p2p(self):
        return Capability(
            self.lookup_factory(self.__get_value__, self.Keys.p2p, default=None), bool
        )

    @property
    def performance(self):
        return Capability(
            self.lookup_factory(self.__get_value__, self.Keys.performance),
            bool,
        )

    @property
    def pppoe(self):
        return Capability(
            self.lookup_factory(self.__get_value__, self.Keys.pppoe, default=None), bool
        )

    @property
    def push(self):
        return Capability(
            self.lookup_factory(self.__get_value__, self.Keys.push, default=None), bool
        )

    @property
    def push_schedule(self):
        return Capability(
            self.lookup_factory(self.__get_value__, self.Keys.push_schedule),
            bool,
        )

    @property
    def reboot(self):
        return Capability(
            self.lookup_factory(self.__get_value__, self.Keys.reboot, default=None), bool
        )

    @property
    def record(self):
        return self.Record(self.__get_value__)

    @property
    def restore(self):
        return Capability(
            self.lookup_factory(self.__get_value__, self.Keys.restore, default=None), bool
        )

    @property
    def rtmp(self):
        return Capability(
            self.lookup_factory(self.__get_value__, self.Keys.rtmp, default=None), bool
        )

    @property
    def rtsp(self):
        return Capability(
            self.lookup_factory(self.__get_value__, self.Keys.rtsp, default=None), bool
        )

    @property
    def schedule_version(self):
        return Capability(
            self.lookup_factory(self.__get_value__, self.Keys.schedule_version),
            _ScheduleVersion,
        )

    @property
    def sd_card(self):
        return Capability(
            self.lookup_factory(self.__get_value__, self.Keys.sd_card, default=None), bool
        )

    @property
    def show_qr_code(self):
        return Capability(
            self.lookup_factory(self.__get_value__, self.Keys.show_qr_code),
            bool,
        )

    @property
    def sim_module(self):
        return Capability(
            self.lookup_factory(self.__get_value__, self.Keys.sim_module),
            bool,
        )

    @property
    def supports(self):
        return self.Supports(self.__get_value__)

    @property
    def talk(self):
        return Capability(
            self.lookup_factory(self.__get_value__, self.Keys.talk, default=None), bool
        )

    @property
    def time(self):
        return Capability(
            self.lookup_factory(self.__get_value__, self.Keys.time, default=None), _Time
        )

    @property
    def tv_system(self):
        return Capability(
            self.lookup_factory(self.__get_value__, self.Keys.tv_system, default=None), bool
        )

    @property
    def upgrade(self):
        return Capability(
            self.lookup_factory(self.__get_value__, self.Keys.upgrade, default=None),
            _Upgrade,
        )

    @property
    def upnp(self):
        return Capability(
            self.lookup_factory(self.__get_value__, self.Keys.upnp, default=None), bool
        )

    @property
    def user(self):
        return Capability(
            self.lookup_factory(self.__get_value__, self.Keys.user, default=None), bool
        )

    @property
    def video_clip(self):
        return Capability(
            self.lookup_factory(self.__get_value__, self.Keys.video_clip),
            _VideoClip,
        )

    @property
    def wifi(self):
        return self.Wifi(self._get_key_value)


class UpdatableCapabilities(Capabilities):
    """Updatatable Capabilities"""

    def update(self, value: Capabilities):
        """Update underlying values"""
        if not isinstance(value, Capabilities):
            raise ValueError("Must provide a Capabilities object")
        self.__get_value__ = self.create_factory(value.__get_value__())
