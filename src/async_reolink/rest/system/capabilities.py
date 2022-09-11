"""System capabilities"""

from typing import Callable, Mapping, TypeVar
from async_reolink.api.system import capabilities

_T = TypeVar("_T")

# pylint: disable=too-few-public-methods
# pylint: disable=missing-function-docstring


class Capability(capabilities.Capability[_T]):
    """Capability"""

    __slots__ = ("_factory",)

    def __init__(self, factory: Callable[[], dict]) -> None:
        super().__init__()
        self._factory = factory

    @property
    def value(self) -> _T:
        if (value := self._factory()) is None:
            return 0
        return value.get("ver", 0)

    @property
    def permissions(self):
        if (value := self._factory()) is None:
            return 0
        return value.get("perm", 0)

    def __bool__(self):
        return bool(self.value)


class ChannelCapabilities(capabilities.ChannelCapabilities):
    """Channel Capabilities"""

    __slots__ = ("_factory",)

    def __init__(self, factory: Callable[[], dict]) -> None:
        super().__init__()
        self._factory = factory

    class AI(capabilities.ChannelCapabilities.AI):
        """AI"""

        __slots__ = ("_factory",)

        def __init__(self, factory: Callable[[], dict]) -> None:
            super().__init__()
            self._factory = factory

        class Track(capabilities.ChannelCapabilities.AI.Track):
            """Track"""

            __slots__ = ("_factory",)

            def __init__(self, factory: Callable[[], dict]) -> None:
                super().__init__()
                self._factory = factory

            @property
            def _value(self):
                def _get():
                    if (value := self._factory()) is None:
                        return None
                    return value.get("aiTrack", None)

                return Capability(_get)

            @property
            def value(self):
                return self._value.value

            @property
            def permissions(self):
                return self._value.permissions

            def __bool__(self):
                return bool(self.value)

            @property
            def pet(self):
                def _get():
                    if (value := self._factory()) is None:
                        return None
                    return value.get("aiTrackDogCat", None)

                return Capability(_get)

        @property
        def track(self):
            return type(self).Track(self._factory)

    @property
    def ai(self):
        return type(self).AI(self._factory)

    class Alarm(capabilities.ChannelCapabilities.Alarm):
        """Alarm"""

        __slots__ = ("_factory",)

        def __init__(self, factory: Callable[[], dict]) -> None:
            super().__init__()
            self._factory = factory

        @property
        def audio(self):
            def _get():
                if (value := self._factory()) is None:
                    return None
                return value.get("alarmAudio", None)

            return Capability(_get)

        @property
        def io_in(self):
            def _get():
                if (value := self._factory()) is None:
                    return None
                return value.get("alarmIoIn", None)

            return Capability(_get)

        @property
        def io_out(self):
            def _get():
                if (value := self._factory()) is None:
                    return None
                return value.get("alarmIoOut", None)

            return Capability(_get)

        @property
        def motion(self):
            def _get():
                if (value := self._factory()) is None:
                    return None
                return value.get("alarmMd", None)

            return Capability(_get)

        @property
        def rf(self):
            def _get():
                if (value := self._factory()) is None:
                    return None
                return value.get("alarmRf", None)

            return Capability(_get)

    @property
    def alarm(self):
        return type(self).Alarm(self._factory)

    @property
    def battery(self):
        def _get():
            if (value := self._factory()) is None:
                return None
            return value.get("battery", None)

        return Capability(_get)

    @property
    def battery_analysis(self):
        def _get():
            if (value := self._factory()) is None:
                return None
            return value.get("batAnalysis", None)

        return Capability(_get)

    @property
    def camera_mode(self):
        def _get():
            if (value := self._factory()) is None:
                return None
            return value.get("cameraMode", None)

        return Capability(_get)

    @property
    def disable_autofocus(self):
        def _get():
            if (value := self._factory()) is None:
                return None
            return value.get("disableAutoFocus", None)

        return Capability(_get)

    @property
    def enc(self):
        def _get():
            if (value := self._factory()) is None:
                return None
            return value.get("enc", None)

        return Capability(_get)

    @property
    def floodlight(self):
        def _get():
            if (value := self._factory()) is None:
                return None
            return value.get("floodLight", None)

        return Capability(_get)

    @property
    def ftp(self):
        def _get():
            if (value := self._factory()) is None:
                return None
            return value.get("ftp", None)

        return Capability(_get)

    @property
    def image(self):
        def _get():
            if (value := self._factory()) is None:
                return None
            return value.get("image", None)

        return Capability(_get)

    @property
    def indicator_light(self):
        def _get():
            if (value := self._factory()) is None:
                return None
            return value.get("indicatorLight", None)

        return Capability(_get)

    class ISP(capabilities.ChannelCapabilities.ISP):
        """ISP"""

        __slots__ = ("_factory",)

        def __init__(self, factory: Callable[[], dict]) -> None:
            super().__init__()
            self._factory = factory

        @property
        def _value(self):
            def _get():
                if (value := self._factory()) is None:
                    return None
                return value.get("isp", None)

            return Capability(_get)

        @property
        def value(self):
            return self._value.value

        @property
        def permissions(self):
            return self._value.permissions

        def __bool__(self):
            return bool(self.value)

        @property
        def threeDnr(self):
            def _get():
                if (value := self._factory()) is None:
                    return None
                return value.get("isp3Dnr", None)

            return Capability(_get)

        @property
        def antiflicker(self):
            def _get():
                if (value := self._factory()) is None:
                    return None
                return value.get("ispAntiFlick", None)

            return Capability(_get)

        @property
        def backlight(self):
            def _get():
                if (value := self._factory()) is None:
                    return None
                return value.get("ispBackLight", None)

            return Capability(_get)

        @property
        def bright(self):
            def _get():
                if (value := self._factory()) is None:
                    return None
                return value.get("ispBright", None)

            return Capability(_get)

        @property
        def contrast(self):
            def _get():
                if (value := self._factory()) is None:
                    return None
                return value.get("ispContrast", None)

            return Capability(_get)

        @property
        def day_night(self):
            def _get():
                if (value := self._factory()) is None:
                    return None
                return value.get("ispDayNight", None)

            return Capability(_get)

        @property
        def exposure_mode(self):
            def _get():
                if (value := self._factory()) is None:
                    return None
                return value.get("ispExposureMode", None)

            return Capability(_get)

        @property
        def flip(self):
            def _get():
                if (value := self._factory()) is None:
                    return None
                return value.get("ispFlip", None)

            return Capability(_get)

        @property
        def hue(self):
            def _get():
                if (value := self._factory()) is None:
                    return None
                return value.get("ispHue", None)

            return Capability(_get)

        @property
        def mirror(self):
            def _get():
                if (value := self._factory()) is None:
                    return None
                return value.get("ispMirror", None)

            return Capability(_get)

        @property
        def satruation(self):
            def _get():
                if (value := self._factory()) is None:
                    return None
                return value.get("ispSatruation", None)

            return Capability(_get)

        @property
        def sharpen(self):
            def _get():
                if (value := self._factory()) is None:
                    return None
                return value.get("ispSharpen", None)

            return Capability(_get)

        @property
        def white_balance(self):
            def _get():
                if (value := self._factory()) is None:
                    return None
                return value.get("ispWhiteBalance", None)

            return Capability(_get)

    @property
    def isp(self):
        return type(self).ISP(self._factory)

    @property
    def led_control(self):
        def _get():
            if (value := self._factory()) is None:
                return None
            return value.get("ledControl", None)

        return Capability(_get)

    @property
    def live(self):
        def _get():
            if (value := self._factory()) is None:
                return None
            return value.get("live", None)

        return Capability(_get)

    @property
    def main_encoding(self):
        def _get():
            if (value := self._factory()) is None:
                return None
            return value.get("mainEncType", None)

        return Capability(_get)

    @property
    def mask(self):
        def _get():
            if (value := self._factory()) is None:
                return None
            return value.get("mask", None)

        return Capability(_get)

    class MD(capabilities.ChannelCapabilities.MD):
        """MotionDetection"""

        __slots__ = ("_factory",)

        def __init__(self, factory: Callable[[], dict]) -> None:
            super().__init__()
            self._factory = factory

        class Trigger(capabilities.ChannelCapabilities.MD.Trigger):
            """Trigger"""

            __slots__ = ("_factory",)

            def __init__(self, factory: Callable[[], dict]) -> None:
                super().__init__()
                self._factory = factory

            @property
            def audio(self):
                def _get():
                    if (value := self._factory()) is None:
                        return None
                    return value.get("mdTriggerAudio", None)

                return Capability(_get)

            @property
            def record(self):
                def _get():
                    if (value := self._factory()) is None:
                        return None
                    return value.get("mdTriggerRecord", None)

                return Capability(_get)

        trigger: Trigger

        @property
        def with_pir(self):
            def _get():
                if (value := self._factory()) is None:
                    return None
                return value.get("mdWithPir", None)

            return Capability(_get)

    @property
    def motion_detection(self):
        return type(self).MD(self._factory)

    @property
    def osd(self):
        def _get():
            if (value := self._factory()) is None:
                return None
            return value.get("osd", None)

        return Capability(_get)

    @property
    def power_led(self):
        def _get():
            if (value := self._factory()) is None:
                return None
            return value.get("powerLed", None)

        return Capability(_get)

    class PTZ(capabilities.ChannelCapabilities.PTZ):
        """PTZ"""

        __slots__ = ("_factory",)

        def __init__(self, factory: Callable[[], dict]) -> None:
            super().__init__()
            self._factory = factory

        @property
        def control(self):
            def _get():
                if (value := self._factory()) is None:
                    return None
                return value.get("ptzCtrl", None)

            return Capability(_get)

        @property
        def direction(self):
            def _get():
                if (value := self._factory()) is None:
                    return None
                return value.get("ptzDirection", None)

            return Capability(_get)

        @property
        def patrol(self):
            def _get():
                if (value := self._factory()) is None:
                    return None
                return value.get("ptzPatrol", None)

            return Capability(_get)

        @property
        def preset(self):
            def _get():
                if (value := self._factory()) is None:
                    return None
                return value.get("ptzPreset", None)

            return Capability(_get)

        @property
        def tattern(self):
            def _get():
                if (value := self._factory()) is None:
                    return None
                return value.get("ptzTattern", None)

            return Capability(_get)

        @property
        def type(self):
            def _get():
                if (value := self._factory()) is None:
                    return None
                return value.get("ptzType", None)

            return Capability(_get)

    @property
    def ptz(self):
        return type(self).PTZ(self._factory)

    class Record(capabilities.ChannelCapabilities.Record):
        """Record"""

        __slots__ = ("_factory",)

        def __init__(self, factory: Callable[[], dict]) -> None:
            super().__init__()
            self._factory = factory

        @property
        def config(self):
            def _get():
                if (value := self._factory()) is None:
                    return None
                return value.get("recCfg", None)

            return Capability(_get)

        @property
        def download(self):
            def _get():
                if (value := self._factory()) is None:
                    return None
                return value.get("recDownload", None)

            return Capability(_get)

        @property
        def replay(self):
            def _get():
                if (value := self._factory()) is None:
                    return None
                return value.get("recReplay", None)

            return Capability(_get)

        @property
        def schedule(self):
            def _get():
                if (value := self._factory()) is None:
                    return None
                return value.get("recSchedule", None)

            return Capability(_get)

    @property
    def record(self):
        return type(self).Record(self._factory)

    @property
    def shelter_config(self):
        def _get():
            if (value := self._factory()) is None:
                return None
            return value.get("shelterCfg", None)

        return Capability(_get)

    @property
    def snap(self):
        def _get():
            if (value := self._factory()) is None:
                return None
            return value.get("snap", None)

        return Capability(_get)

    class Supports(capabilities.ChannelCapabilities.Supports):
        """Supports"""

        __slots__ = ("_factory",)

        def __init__(self, factory: Callable[[], dict]) -> None:
            super().__init__()
            self._factory = factory

        class AI(capabilities.ChannelCapabilities.Supports.AI):
            """AI"""

            __slots__ = ("_factory",)

            def __init__(self, factory: Callable[[], dict]) -> None:
                super().__init__()
                self._factory = factory

            @property
            def _value(self):
                def _get():
                    if (value := self._factory()) is None:
                        return None
                    return value.get("supportAi", None)

                return Capability(_get)

            @property
            def value(self):
                return self._value.value

            @property
            def permissions(self):
                return self._value.permissions

            def __bool__(self):
                return bool(self.value)

            @property
            def animal(self):
                def _get():
                    if (value := self._factory()) is None:
                        return None
                    return value.get("supportAiAnimal", None)

                return Capability(_get)

            @property
            def detect_config(self):
                def _get():
                    if (value := self._factory()) is None:
                        return None
                    return value.get("supportAiDetectConfig", None)

                return Capability(_get)

            @property
            def pet(self):
                def _get():
                    if (value := self._factory()) is None:
                        return None
                    return value.get("supportAiDogCat", None)

                return Capability(_get)

            @property
            def face(self):
                def _get():
                    if (value := self._factory()) is None:
                        return None
                    return value.get("supportAiFace", None)

                return Capability(_get)

            @property
            def people(self):
                def _get():
                    if (value := self._factory()) is None:
                        return None
                    return value.get("supportAiPeople", None)

                return Capability(_get)

            @property
            def sensitivity(self):
                def _get():
                    if (value := self._factory()) is None:
                        return None
                    return value.get("supportAiSensitivity", None)

                return Capability(_get)

            @property
            def stay_time(self):
                def _get():
                    if (value := self._factory()) is None:
                        return None
                    return value.get("supportAiStayTime", None)

                return Capability(_get)

            @property
            def target_size(self):
                def _get():
                    if (value := self._factory()) is None:
                        return None
                    return value.get("supportAiTargetSize", None)

                return Capability(_get)

            @property
            def track_classify(self):
                def _get():
                    if (value := self._factory()) is None:
                        return None
                    return value.get("supportAiTrackClassify", None)

                return Capability(_get)

            @property
            def vehicle(self):
                def _get():
                    if (value := self._factory()) is None:
                        return None
                    return value.get("supportAiVehicle", None)

                return Capability(_get)

            @property
            def adjust(self):
                def _get():
                    if (value := self._factory()) is None:
                        return None
                    return value.get("supportAoAdjust", None)

                return Capability(_get)

        @property
        def ai(self):
            return type(self).AI(self._factory)

        class FloodLight(capabilities.ChannelCapabilities.Supports.FloodLight):
            """FloodLight"""

            __slots__ = ("_factory",)

            def __init__(self, factory: Callable[[], dict]) -> None:
                super().__init__()
                self._factory = factory

            @property
            def brightness(self):
                def _get():
                    if (value := self._factory()) is None:
                        return None
                    return value.get("supportFLBrightness", None)

                return Capability(_get)

            @property
            def intelligent(self):
                def _get():
                    if (value := self._factory()) is None:
                        return None
                    return value.get("supportFLIntelligent", None)

                return Capability(_get)

            @property
            def keep_on(self):
                def _get():
                    if (value := self._factory()) is None:
                        return None
                    return value.get("supportFLKeepOn", None)

                return Capability(_get)

            @property
            def schedule(self):
                def _get():
                    if (value := self._factory()) is None:
                        return None
                    return value.get("supportFLSchedule", None)

                return Capability(_get)

            @property
            def switch(self):
                def _get():
                    if (value := self._factory()) is None:
                        return None
                    return value.get("supportFLswitch", None)

                return Capability(_get)

        @property
        def flood_light(self):
            return type(self).FloodLight(self._factory)

        @property
        def gop(self):
            def _get():
                if (value := self._factory()) is None:
                    return None
                return value.get("supportGop", None)

            return Capability(_get)

        @property
        def motion_detection(self):
            def _get():
                if (value := self._factory()) is None:
                    return None
                return value.get("supportMd", None)

            return Capability(_get)

        @property
        def ptz_check(self):
            def _get():
                if (value := self._factory()) is None:
                    return None
                return value.get("supportPtzCheck", None)

            return Capability(_get)

        @property
        def threshold_adjust(self):
            def _get():
                if (value := self._factory()) is None:
                    return None
                return value.get("supportThresholdAdjust", None)

            return Capability(_get)

        @property
        def white_dark(self):
            def _get():
                if (value := self._factory()) is None:
                    return None
                return value.get("supportWhiteDark", None)

            return Capability(_get)

    @property
    def supports(self):
        return type(self).Supports(self._factory)

    @property
    def video_clip(self):
        def _get():
            if (value := self._factory()) is None:
                return None
            return value.get("videoClip", None)

        return Capability(_get)

    @property
    def watermark(self):
        def _get():
            if (value := self._factory()) is None:
                return None
            return value.get("waterMark", None)

        return Capability(_get)

    @property
    def white_balance(self):
        def _get():
            if (value := self._factory()) is None:
                return None
            return value.get("white_balance", None)

        return Capability(_get)


class _Channels(Mapping[int, ChannelCapabilities]):
    """Channels"""

    __slots__ = ("_factory",)

    def __init__(self, factory: Callable[[], list]) -> None:
        super().__init__()
        self._factory = factory

    def __getitem__(self, __k: int):
        def _get():
            if (_list := self._factory()) is None:
                return None
            return _list[__k]

        return ChannelCapabilities(_get)

    def __iter__(self):
        if (_list := self._factory()) is None:
            return
        for i in range(0, len(_list)):
            yield i

    def __len__(self):
        if (_list := self._factory()) is None:
            return 0
        return len(_list)


class Capabilities(capabilities.Capabilities):
    """Capabilities"""

    __slots__ = ("_factory",)

    def __init__(self, factory: Callable[[], dict]) -> None:
        super().__init__()
        self._factory = factory

    @property
    def three_g(self):
        def _get():
            if (value := self._factory()) is None:
                return None
            return value.get("3g", None)

        return Capability(_get)

    @property
    def channels(self):
        """channels"""

        def _get():
            if (value := self._factory()) is None:
                return None
            return value.get("abilityChn", None)

        return _Channels(_get)

    class Alarm(capabilities.Capabilities.Alarm):
        """Alarm"""

        __slots__ = ("_factory",)

        def __init__(self, factory: Callable[[], dict]) -> None:
            super().__init__()
            self._factory = factory

        @property
        def audio(self):
            def _get():
                if (value := self._factory()) is None:
                    return None
                return value.get("alarmAudio", None)

            return Capability(_get)

        @property
        def disconnect(self):
            def _get():
                if (value := self._factory()) is None:
                    return None
                return value.get("alarmDisconnet", None)

            return Capability(_get)

        class HDD(capabilities.Capabilities.Alarm.HDD):
            """HDDD"""

            __slots__ = ("_factory",)

            def __init__(self, factory: Callable[[], dict]) -> None:
                super().__init__()
                self._factory = factory

            @property
            def error(self):
                def _get():
                    if (value := self._factory()) is None:
                        return None
                    return value.get("alarmHddErr", None)

                return Capability(_get)

            @property
            def full(self):
                def _get():
                    if (value := self._factory()) is None:
                        return None
                    return value.get("alarmHddFull", None)

                return Capability(_get)

        @property
        def hdd(self):
            return type(self).HDD(self._factory)

        @property
        def ip_conflict(self):
            def _get():
                if (value := self._factory()) is None:
                    return None
                return value.get("alarmIpConflict", None)

            return Capability(_get)

    @property
    def alarm(self):
        return type(self).Alarm(self._factory)

    @property
    def auth(self):
        def _get():
            if (value := self._factory()) is None:
                return None
            return value.get("auth", None)

        return Capability(_get)

    @property
    def auto_maintenance(self):
        def _get():
            if (value := self._factory()) is None:
                return None
            return value.get("autoMaint", None)

        return Capability(_get)

    @property
    def cloud_storage(self):
        def _get():
            if (value := self._factory()) is None:
                return None
            return value.get("cloudStorage", None)

        return Capability(_get)

    @property
    def custom_audio(self):
        def _get():
            if (value := self._factory()) is None:
                return None
            return value.get("customAudio", None)

        return Capability(_get)

    @property
    def date_format(self):
        def _get():
            if (value := self._factory()) is None:
                return None
            return value.get("dateFormat", None)

        return Capability(_get)

    @property
    def ddns(self):
        def _get():
            if (value := self._factory()) is None:
                return None
            return value.get("ddns", None)

        return Capability(_get)

    class Device(capabilities.Capabilities.Device):
        """Device"""

        __slots__ = ("_factory",)

        def __init__(self, factory: Callable[[], dict]) -> None:
            super().__init__()
            self._factory = factory

        @property
        def info(self):
            def _get():
                if (value := self._factory()) is None:
                    return None
                return value.get("devInfo", None)

            return Capability(_get)

        @property
        def name(self):
            def _get():
                if (value := self._factory()) is None:
                    return None
                return value.get("devName", None)

            return Capability(_get)

    @property
    def device(self):
        return type(self).Device(self._factory)

    @property
    def disable_autofocus(self):
        def _get():
            if (value := self._factory()) is None:
                return None
            return value.get("disableAutoFocus", None)

        return Capability(_get)

    @property
    def disk(self):
        def _get():
            if (value := self._factory()) is None:
                return None
            return value.get("disk", None)

        return Capability(_get)

    @property
    def display(self):
        def _get():
            if (value := self._factory()) is None:
                return None
            return value.get("display", None)

        return Capability(_get)

    class Email(capabilities.Capabilities.Email):
        """Email"""

        __slots__ = ("_factory",)

        def __init__(self, factory: Callable[[], dict]) -> None:
            super().__init__()
            self._factory = factory

        @property
        def _value(self):
            def _get():
                if (value := self._factory()) is None:
                    return None
                return value.get("email", None)

            return Capability(_get)

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
            def _get():
                if (value := self._factory()) is None:
                    return None
                return value.get("emailInterval", None)

            return Capability(_get)

        @property
        def schedule(self):
            def _get():
                if (value := self._factory()) is None:
                    return None
                return value.get("emailSchedule", None)

            return Capability(_get)

    @property
    def email(self):
        return type(self).Email(self._factory)

    @property
    def config_import(self):
        def _get():
            if (value := self._factory()) is None:
                return None
            return value.get("importCfg", None)

        return Capability(_get)

    @property
    def config_export(self):
        def _get():
            if (value := self._factory()) is None:
                return None
            return value.get("exportCfg", None)

        return Capability(_get)

    class FTP(capabilities.Capabilities.FTP):
        """FTP"""

        __slots__ = ("_factory",)

        def __init__(self, factory: Callable[[], dict]) -> None:
            super().__init__()
            self._factory = factory

        @property
        def auto_dir(self):
            def _get():
                if (value := self._factory()) is None:
                    return None
                return value.get("ftpAutoDir", None)

            return Capability(_get)

        class Stream(capabilities.Capabilities.FTP.Stream):
            """Stream"""

            __slots__ = ("_factory",)

            def __init__(self, factory: Callable[[], dict]) -> None:
                super().__init__()
                self._factory = factory

            @property
            def ext(self):
                def _get():
                    if (value := self._factory()) is None:
                        return None
                    return value.get("ftpExtStream", None)

                return Capability(_get)

            @property
            def sub(self):
                def _get():
                    if (value := self._factory()) is None:
                        return None
                    return value.get("ftpSubStream", None)

                return Capability(_get)

        @property
        def stream(self):
            return type(self).Stream(self._factory)

        @property
        def picture(self):
            def _get():
                if (value := self._factory()) is None:
                    return None
                return value.get("ftpPic", None)

            return Capability(_get)

        @property
        def test(self):
            def _get():
                if (value := self._factory()) is None:
                    return None
                return value.get("ftpTest", None)

            return Capability(_get)

    @property
    def ftp(self):
        return type(self).FTP(self._factory)

    @property
    def hour_format(self):
        """change hour format supported"""

        def _get():
            if (value := self._factory()) is None:
                return None
            return value.get("hourFmt", None)

        return Capability(_get)

    @property
    def http(self):
        def _get():
            if (value := self._factory()) is None:
                return None
            return value.get("http", None)

        return Capability(_get)

    @property
    def http_flv(self):
        def _get():
            if (value := self._factory()) is None:
                return None
            return value.get("httpFlv", None)

        return Capability(_get)

    @property
    def https(self):
        def _get():
            if (value := self._factory()) is None:
                return None
            return value.get("https", None)

        return Capability(_get)

    @property
    def ipc_manager(self):
        def _get():
            if (value := self._factory()) is None:
                return None
            return value.get("ipcManager", None)

        return Capability(_get)

    @property
    def led_control(self):
        def _get():
            if (value := self._factory()) is None:
                return None
            return value.get("ledControl", None)

        return Capability(_get)

    @property
    def local_link(self):
        def _get():
            if (value := self._factory()) is None:
                return None
            return value.get("localLink", None)

        return Capability(_get)

    @property
    def log(self):
        def _get():
            if (value := self._factory()) is None:
                return None
            return value.get("log", None)

        return Capability(_get)

    @property
    def media_port(self):
        def _get():
            if (value := self._factory()) is None:
                return None
            return value.get("mediaPort", None)

        return Capability(_get)

    @property
    def ntp(self):
        def _get():
            if (value := self._factory()) is None:
                return None
            return value.get("ntp", None)

        return Capability(_get)

    @property
    def online(self):
        def _get():
            if (value := self._factory()) is None:
                return None
            return value.get("online", None)

        return Capability(_get)

    @property
    def onvif(self):
        def _get():
            if (value := self._factory()) is None:
                return None
            return value.get("onvif", None)

        return Capability(_get)

    @property
    def p2p(self):
        def _get():
            if (value := self._factory()) is None:
                return None
            return value.get("p2p", None)

        return Capability(_get)

    @property
    def performance(self):
        def _get():
            if (value := self._factory()) is None:
                return None
            return value.get("performance", None)

        return Capability(_get)

    @property
    def pppoe(self):
        def _get():
            if (value := self._factory()) is None:
                return None
            return value.get("pppoe", None)

        return Capability(_get)

    @property
    def push(self):
        def _get():
            if (value := self._factory()) is None:
                return None
            return value.get("push", None)

        return Capability(_get)

    @property
    def push_schedule(self):
        def _get():
            if (value := self._factory()) is None:
                return None
            return value.get("pushSchedule", None)

        return Capability(_get)

    @property
    def reboot(self):
        def _get():
            if (value := self._factory()) is None:
                return None
            return value.get("reboot", None)

        return Capability(_get)

    class Record(capabilities.Capabilities.Record):
        """Record"""

        __slots__ = ("_factory",)

        def __init__(self, factory: Callable[[], dict]) -> None:
            super().__init__()
            self._factory = factory

        @property
        def extension_time_list(self):
            def _get():
                if (value := self._factory()) is None:
                    return None
                return value.get("recExtensionTimeList", None)

            return Capability(_get)

        @property
        def overwrite(self):
            def _get():
                if (value := self._factory()) is None:
                    return None
                return value.get("recOverWrite", None)

            return Capability(_get)

        @property
        def pack_duration(self):
            def _get():
                if (value := self._factory()) is None:
                    return None
                return value.get("recPackDuration", None)

            return Capability(_get)

        @property
        def pre_record(self):
            def _get():
                if (value := self._factory()) is None:
                    return None
                return value.get("recPreRecord", None)

            return Capability(_get)

    @property
    def record(self):
        return type(self).Record(self._factory)

    @property
    def restore(self):
        def _get():
            if (value := self._factory()) is None:
                return None
            return value.get("restore", None)

        return Capability(_get)

    @property
    def rtmp(self):
        def _get():
            if (value := self._factory()) is None:
                return None
            return value.get("rtmp", None)

        return Capability(_get)

    @property
    def rtsp(self):
        def _get():
            if (value := self._factory()) is None:
                return None
            return value.get("rtsp", None)

        return Capability(_get)

    @property
    def schedule_version(self):
        def _get():
            if (value := self._factory()) is None:
                return None
            return value.get("scheduleVersion", None)

        return Capability(_get)

    @property
    def sd_card(self):
        def _get():
            if (value := self._factory()) is None:
                return None
            return value.get("sdCard", None)

        return Capability(_get)

    @property
    def show_qr_code(self):
        def _get():
            if (value := self._factory()) is None:
                return None
            return value.get("showQrCode", None)

        return Capability(_get)

    @property
    def sim_module(self):
        def _get():
            if (value := self._factory()) is None:
                return None
            return value.get("simModule", None)

        return Capability(_get)

    class Supports(capabilities.Capabilities.Supports):
        """Supports"""

        __slots__ = ("_factory",)

        def __init__(self, factory: Callable[[], dict]) -> None:
            super().__init__()
            self._factory = factory

        class Audio(capabilities.Capabilities.Supports.Audio):
            """Audio"""

            __slots__ = ("_factory",)

            def __init__(self, factory: Callable[[], dict]) -> None:
                super().__init__()
                self._factory = factory

            class Alarm(capabilities.Capabilities.Supports.Audio.Alarm):
                """Alarm"""

                __slots__ = ("_factory",)

                def __init__(self, factory: Callable[[], dict]) -> None:
                    super().__init__()
                    self._factory = factory

                @property
                def _value(self):
                    def _get():
                        if (value := self._factory()) is None:
                            return None
                        return value.get("supportAudioAlarm", None)

                    return Capability(_get)

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
                    def _get():
                        if (value := self._factory()) is None:
                            return None
                        return value.get("supportAudioAlarmEnable", None)

                    return Capability(_get)

                @property
                def schedule(self):
                    def _get():
                        if (value := self._factory()) is None:
                            return None
                        return value.get("supportAudioAlarmSchedule", None)

                    return Capability(_get)

                @property
                def task_enable(self):
                    def _get():
                        if (value := self._factory()) is None:
                            return None
                        return value.get("supportAudioAlarmTaskEnable", None)

                    return Capability(_get)

            @property
            def alarm(self):
                return type(self).Alarm(self._factory)

        @property
        def audio(self):
            return type(self).Audio(self._factory)

        class Buzzer(capabilities.Capabilities.Supports.Buzzer):
            """Buzzer"""

            __slots__ = ("_factory",)

            def __init__(self, factory: Callable[[], dict]) -> None:
                super().__init__()
                self._factory = factory

            class Task(capabilities.Capabilities.Supports.Buzzer.Task):
                """Task"""

                __slots__ = ("_factory",)

                def __init__(self, factory: Callable[[], dict]) -> None:
                    super().__init__()
                    self._factory = factory

                @property
                def _value(self):
                    def _get():
                        if (value := self._factory()) is None:
                            return None
                        return value.get("supportBuzzerTask", None)

                    return Capability(_get)

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
                    def _get():
                        if (value := self._factory()) is None:
                            return None
                        return value.get("supportBuzzerEnable", None)

                    return Capability(_get)

            @property
            def _value(self):
                def _get():
                    if (value := self._factory()) is None:
                        return None
                    return value.get("supportBuzzer", None)

                return Capability(_get)

            @property
            def task(self):
                return type(self).Task(self._factory)

            @property
            def value(self):
                """value"""
                return self._value.value

            @property
            def permissions(self):
                """permissions"""
                return self._value.permissions

        @property
        def buzzer(self):
            return type(self).Buzzer(self._factory)

        class Email(capabilities.Capabilities.Supports.Email):
            """Email"""

            __slots__ = ("_factory",)

            def __init__(self, factory: Callable[[], dict]) -> None:
                super().__init__()
                self._factory = factory

            @property
            def enable(self):
                def _get():
                    if (value := self._factory()) is None:
                        return None
                    return value.get("supportEmailEnable", None)

                return Capability(_get)

            @property
            def task_enable(self):
                def _get():
                    if (value := self._factory()) is None:
                        return None
                    return value.get("supportEmailTaskEnable", None)

                return Capability(_get)

        @property
        def email(self):
            return type(self).Email(self._factory)

        class FTP(capabilities.Capabilities.Supports.FTP):
            """FTP"""

            __slots__ = ("_factory",)

            def __init__(self, factory: Callable[[], dict]) -> None:
                super().__init__()
                self._factory = factory

            class Cover(capabilities.Capabilities.Supports.FTP.Cover):
                """Cover"""

                __slots__ = ("_factory",)

                def __init__(self, factory: Callable[[], dict]) -> None:
                    super().__init__()
                    self._factory = factory

                @property
                def picture(self):
                    def _get():
                        if (value := self._factory()) is None:
                            return None
                        return value.get("supportFtpCoverPicture", None)

                    return Capability(_get)

                @property
                def video(self):
                    def _get():
                        if (value := self._factory()) is None:
                            return None
                        return value.get("supportFtpCoverVideo", None)

                    return Capability(_get)

            @property
            def cover(self):
                return type(self).Cover(self._factory)

            @property
            def dir_YM(self):
                def _get():
                    if (value := self._factory()) is None:
                        return None
                    return value.get("supportFtpDirYM", None)

                return Capability(_get)

            @property
            def enable(self):
                def _get():
                    if (value := self._factory()) is None:
                        return None
                    return value.get("supportFtpEnable", None)

                return Capability(_get)

            class Picture(capabilities.Capabilities.Supports.FTP.Picture):
                """Picture"""

                __slots__ = ("_factory",)

                def __init__(self, factory: Callable[[], dict]) -> None:
                    super().__init__()
                    self._factory = factory

                @property
                def capture_mode(self):
                    def _get():
                        if (value := self._factory()) is None:
                            return None
                        return value.get("supportFtpPicCaptureMode", None)

                    return Capability(_get)

                @property
                def custom_resolution(self):
                    def _get():
                        if (value := self._factory()) is None:
                            return None
                        return value.get("supportFtpPicResoCustom", None)

                    return Capability(_get)

                @property
                def swap(self):
                    def _get():
                        if (value := self._factory()) is None:
                            return None
                        return value.get("supportFtpPictureSwap", None)

                    return Capability(_get)

            @property
            def picture(self):
                return type(self).Picture(self._factory)

            class Task(capabilities.Capabilities.Supports.FTP.Task):
                """Task"""

                __slots__ = ("_factory",)

                def __init__(self, factory: Callable[[], dict]) -> None:
                    super().__init__()
                    self._factory = factory

                @property
                def _value(self):
                    def _get():
                        if (value := self._factory()) is None:
                            return None
                        return value.get("supportFtpTask", None)

                    return Capability(_get)

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
                    def _get():
                        if (value := self._factory()) is None:
                            return None
                        return value.get("supportFtpTaskEnable", None)

                    return Capability(_get)

            @property
            def task(self):
                return type(self).Task(self._factory)

            @property
            def video_swap(self):
                def _get():
                    if (value := self._factory()) is None:
                        return None
                    return value.get("supportFtpVideoSwap", None)

                return Capability(_get)

            @property
            def ftps_encrypt(self):
                def _get():
                    if (value := self._factory()) is None:
                        return None
                    return value.get("supportFtpsEncrypt", None)

                return Capability(_get)

        @property
        def ftp(self):
            return type(self).FTP(self._factory)

        @property
        def http_enable(self):
            def _get():
                if (value := self._factory()) is None:
                    return None
                return value.get("supportHttpEnable", None)

            return Capability(_get)

        @property
        def https_enable(self):
            def _get():
                if (value := self._factory()) is None:
                    return None
                return value.get("supportHttpsEnable", None)

            return Capability(_get)

        @property
        def onvif_enable(self):
            def _get():
                if (value := self._factory()) is None:
                    return None
                return value.get("supportOnvifEnable", None)

            return Capability(_get)

        @property
        def push_interval(self):
            def _get():
                if (value := self._factory()) is None:
                    return None
                return value.get("supportPushInterval", None)

            return Capability(_get)

        class Record(capabilities.Capabilities.Supports.Record):
            """Record"""

            __slots__ = ("_factory",)

            def __init__(self, factory: Callable[[], dict]) -> None:
                super().__init__()
                self._factory = factory

            @property
            def schedule_enable(self):
                def _get():
                    if (value := self._factory()) is None:
                        return None
                    return value.get("supportRecScheduleEnable", None)

                return Capability(_get)

            @property
            def enable(self):
                def _get():
                    if (value := self._factory()) is None:
                        return None
                    return value.get("supportRecordEnable", None)

                return Capability(_get)

        @property
        def record(self):
            return type(self).Record(self._factory)

        @property
        def rtmp_enable(self):
            def _get():
                if (value := self._factory()) is None:
                    return None
                return value.get("supportRtmpEnable", None)

            return Capability(_get)

        @property
        def rtsp_enable(self):
            def _get():
                if (value := self._factory()) is None:
                    return None
                return value.get("supportRtspEnable", None)

            return Capability(_get)

    @property
    def supports(self):
        return type(self).Supports(self._factory)

    @property
    def talk(self):
        def _get():
            if (value := self._factory()) is None:
                return None
            return value.get("talk", None)

        return Capability(_get)

    @property
    def time(self):
        def _get():
            if (value := self._factory()) is None:
                return None
            return value.get("time", None)

        return Capability(_get)

    @property
    def tv_system(self):
        def _get():
            if (value := self._factory()) is None:
                return None
            return value.get("tvSystem", None)

        return Capability(_get)

    @property
    def upgrade(self):
        def _get():
            if (value := self._factory()) is None:
                return None
            return value.get("upgrade", None)

        return Capability(_get)

    @property
    def upnp(self):
        def _get():
            if (value := self._factory()) is None:
                return None
            return value.get("upnp", None)

        return Capability(_get)

    @property
    def user(self):
        def _get():
            if (value := self._factory()) is None:
                return None
            return value.get("user", None)

        return Capability(_get)

    @property
    def video_clip(self):
        def _get():
            if (value := self._factory()) is None:
                return None
            return value.get("videoClip", None)

        return Capability(_get)

    class Wifi(capabilities.Capabilities.Wifi):
        """WIFI"""

        __slots__ = ("_factory",)

        def __init__(self, factory: Callable[[], dict]) -> None:
            super().__init__()
            self._factory = factory

        @property
        def _value(self):
            def _get():
                if (value := self._factory()) is None:
                    return None
                return value.get("wifi", None)

            return Capability(_get)

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
            def _get():
                if (value := self._factory()) is None:
                    return None
                return value.get("wifiTest", None)

            return Capability(_get)

    @property
    def wifi(self):
        return type(self).Wifi(self._factory)
