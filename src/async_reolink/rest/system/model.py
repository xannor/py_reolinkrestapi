"""System models"""

from typing import Callable, Final, Protocol, TypeAlias, TypedDict
from async_reolink.api.system import command as system
from async_reolink.api.system import typing as sys_typing
from async_reolink.api.typing import WeekDays
from async_reolink.api import model as api_model

from ..system.typing import (
    int_hour_format,
    int_storage_type,
    int_weekday,
    storage_type_int,
    weekday_int,
    hour_format_int,
)

from .. import model

from .._utilities.providers import value as providers

_JSONDict: TypeAlias = dict[str, any]

# pylint: disable=missing-function-docstring
# pylint: disable=too-few-public-methods


class UserInfo(providers.Value[_JSONDict]):
    class JSON(TypedDict):
        """JSON"""

        userName: str

    class Keys(Protocol):
        """Keys"""

        user_name: Final = "userName"

    __slots__ = ()

    __get_value__: providers.FactoryValue[JSON]

    @property
    def user_name(self):
        if value := self.__get_value__():
            return value.get(self.Keys.user_name, "")
        return ""


class MutableUserInfo(UserInfo):
    __slots__ = ()

    def __default_factory__(self, create=False):
        if not create:
            return None
        value = {}
        if self is not None and not isinstance(self, type):
            self.__set_value__(value)
        return value

    @UserInfo.user_name.setter
    def user_name(self, value):
        self.__get_value__(True)[self.Keys.user_name] = str(value)


class DeviceInfo(providers.Value[_JSONDict], sys_typing.DeviceInfo):
    """Device Info"""

    class IO(providers.Value[_JSONDict], sys_typing.DeviceInfo.IO):
        """IO"""

        class JSON(TypedDict):
            """JSON"""

            IOInputNum: int
            IOOutputNum: int

        class Keys(Protocol):
            """Keys"""

            inputs: Final = "IOInputNum"
            outputs: Final = "IOOutputNum"

        __slots__ = ()

        __get_value__: providers.FactoryValue[JSON]

        @property
        def inputs(self):
            if value := self.__get_value__():
                return value.get(self.Keys.inputs, 0)
            return 0

        @property
        def outputs(self):
            if value := self.__get_value__():
                return value.get(self.Keys.outputs, 0)
            return 0

    class Version(providers.Value[_JSONDict], sys_typing.DeviceInfo.Version):
        """Versions"""

        class JSON(TypedDict):
            """JSON"""

            firmVer: str
            frameworkVer: str
            hardVer: str
            cfgVer: str

        class Keys(Protocol):
            """Keys"""

            firmware: Final = "firmVer"
            framework: Final = "frameworkVer"
            hardware: Final = "hardVer"
            config: Final = "cfgVer"

        __slots__ = ()

        __get_value__: providers.FactoryValue[JSON]

        @property
        def firmware(self):
            if value := self.__get_value__():
                return value.get(self.Keys.firmware, "")
            return ""

        @property
        def framework(self):
            if value := self.__get_value__():
                return value.get(self.Keys.framework, "")
            return ""

        @property
        def hardware(self):
            if value := self.__get_value__():
                return value.get(self.Keys.hardware, "")
            return ""

        @property
        def config(self):
            if value := self.__get_value__():
                return value.get(self.Keys.config, "")
            return ""

    class JSON(IO.JSON, Version.JSON):
        """JSON"""

        audioNum: int
        buildDay: str
        channelNum: int
        detail: str
        diskNum: int
        model: str
        name: str
        type: str
        wifi: int
        B845: any
        exactType: str
        serial: str
        paxSuffix: str

    class Keys(Protocol):
        """Keys"""

        audio_sources: Final = "audioNum"
        build_day: Final = "buildDay"
        channels: Final = "channelNum"
        detail: Final = "detail"
        disks: Final = "diskNum"
        model: Final = "model"
        name: Final = "name"
        type: Final = "type"
        wifi: Final = "wifi"
        B845: Final = "B845"
        exact_type: Final = "exactType"
        serial: Final = "serial"
        pak_suffix: Final = "paxSuffix"

    __slots__ = ()

    __get_value__: providers.FactoryValue[JSON]

    @property
    def io(self):
        return DeviceInfo.IO(self.__get_value__)

    @property
    def version(self):
        return DeviceInfo.Version(self.__get_value__)

    @property
    def audio_sources(self):
        if value := self.__get_value__():
            return value.get(self.Keys.audio_sources, 0)
        return 0

    @property
    def build_day(self):
        if value := self.__get_value__():
            return value.get(self.Keys.build_day, "")
        return ""

    @property
    def channels(self):
        if value := self.__get_value__():
            return value.get(self.Keys.channels, 0)
        return 0

    @property
    def detail(self):
        if value := self.__get_value__():
            return value.get(self.Keys.detail, "")
        return ""

    @property
    def disks(self):
        if value := self.__get_value__():
            return value.get(self.Keys.disks, 0)
        return 0

    @property
    def model(self):
        if value := self.__get_value__():
            return value.get(self.Keys.model, "")
        return ""

    @property
    def name(self):
        if value := self.__get_value__():
            return value.get(self.Keys.name, "")
        return ""

    @property
    def type(self):
        if value := self.__get_value__():
            return value.get(self.Keys.type, "")
        return ""

    @property
    def wifi(self):
        return True if (value := self.__get_value__()) and value.get(self.Keys.wifi, 0) else False

    @property
    def exact_type(self):
        if value := self.__get_value__():
            return value.get(self.Keys.exact_type, "")
        return ""

    @property
    def serial(self):
        if value := self.__get_value__():
            return value.get(self.Keys.serial, "")
        return ""

    @property
    def pak_suffix(self):
        if value := self.__get_value__():
            return value.get(self.Keys.pak_suffix, "")
        return ""

    def update(self, value: "DeviceInfo"):
        if not isinstance(value, type(self)):
            raise TypeError("Can only update from another DeviceInfo")
        # pylint: disable=protected-access
        self.__set_value__(value.__get_value__())
        return self


_DefaultWeekday: Final = WeekDays.SUNDAY
_DefaultWeekdayInt: Final = weekday_int(_DefaultWeekday)


class DaylightSavingsTimeInfo(providers.Value[_JSONDict], system.DaylightSavingsTimeInfo):
    """Dalight Savings Time Info"""

    class TimeInfo(model.SimpleTime, system.DaylightSavingsTimeInfo.TimeInfo):
        """Time Info"""

        class JSON(model.SimpleTime.JSON):
            """JSON"""

            mon: int
            week: int
            weekday: int

        class Keys(model.SimpleTime.Keys, Protocol):
            """Keys"""

            month: Final = "mon"
            week: Final = "week"
            weekday: Final = "weekday"

            __all__ = model.SimpleTime.Keys.__all__ + (month, week, weekday)

        __get_value__: providers.FactoryValue[JSON]

        @property
        def month(self):
            if value := self.__get_value__():
                return value.get(self._mangle_key(self.Keys.month), 0)
            return 0

        @property
        def week(self):
            if value := self.__get_value__():
                return value.get(self._mangle_key(self.Keys.week), 0)
            return 0

        @property
        def weekday(self):
            if value := self.__get_value__():
                return int_weekday(value.get(self._mangle_key(self.Keys.week), _DefaultWeekdayInt))
            return _DefaultWeekday

    class JSON(TypedDict):
        """JSON"""

        enable: int
        offset: int

    class Keys(Protocol):
        """Keys"""

        enabled: Final = "enable"
        hour_offset: Final = "offset"

    __slots__ = ()

    __get_value__: providers.FactoryValue[JSON]

    @property
    def enabled(self):
        return (
            True if (value := self.__get_value__()) and value.get(self.Keys.enabled, 0) else False
        )

    @property
    def hour_offset(self):
        if value := self.__get_value__():
            return value.get(self.Keys.hour_offset, 0)
        return 0

    @property
    def start(self):
        return DaylightSavingsTimeInfo.TimeInfo(self.__get_value__, prefix="start", titleCase=True)

    @property
    def end(self):
        return DaylightSavingsTimeInfo.TimeInfo(self.__get_value__, prefix="end", titleCase=True)


_DefaultHourFormat: Final = sys_typing.HourFormat.HR_24
_DefaultHourFormatInt: Final = hour_format_int(_DefaultHourFormat)


class TimeInfo(model.DateTime, system.TimeInfo):
    """Device Time"""

    class JSON(model.DateTime.JSON):
        """JSON"""

        hourFmt: int
        timeFmt: str
        timeZome: int

    class Keys(model.DateTime.Keys, Protocol):
        """Keys"""

        hour_format: Final = "hourFmt"
        date_format: Final = "timeFmt"
        timezone_offset: Final = "timeZone"

        __all__ = model.DateTime.Keys.__all__ + (hour_format, date_format, timezone_offset)

    __slots__ = ()

    __get_value__: providers.FactoryValue[JSON]

    @property
    def hour_format(self):
        if value := self.__get_value__():
            return int_hour_format(value.get(self.Keys.hour_format, _DefaultHourFormat))
        return _DefaultHourFormat

    @property
    def date_format(self):
        _default = "DD/MM/YYYY"
        if value := self.__get_value__():
            return value.get(self.Keys.date_format, _default)
        return _default

    @property
    def timezone_offset(self):
        if value := self.__get_value__():
            return value.get(self.Keys.timezone_offset, 0)
        return 0


_DefaultStorageType: Final = sys_typing.StorageTypes.SDC
_DefaultStorageTypeInt: Final = storage_type_int(_DefaultStorageType)


class StorageInfo(providers.Value[_JSONDict], sys_typing.StorageInfo):
    """REST Storage Info"""

    class JSON(TypedDict):
        """JSON"""

        number: int
        capacity: int
        format: int
        mount: int
        size: int
        storageType: int

    class Keys(Protocol):
        """Keys"""

        id: Final = "number"
        capacity: Final = "capacity"
        formatted: Final = "format"
        mounted: Final = "mount"
        free_space: Final = "size"
        type: Final = "storageType"

    __slots__ = ()

    __get_value__: providers.FactoryValue[JSON]

    @property
    def id(self):
        if value := self.__get_value__():
            return value.get(self.Keys.id, 0)
        return 0

    @property
    def capacity(self):
        if value := self.__get_value__():
            return value.get(self.Keys.capacity, 0)
        return 0

    @property
    def formatted(self) -> bool:
        return (
            True if (value := self.__get_value__()) and value.get(self.Keys.formatted, 0) else False
        )

    @property
    def mounted(self) -> bool:
        return (
            True if (value := self.__get_value__()) and value.get(self.Keys.mounted, 0) else False
        )

    @property
    def free_space(self):
        if value := self.__get_value__():
            return value.get(self.Keys.free_space, 0)
        return 0

    @property
    def type(self):
        if value := self.__get_value__():
            return int_storage_type(value.get(self.Keys.type, _DefaultStorageTypeInt))
        return _DefaultStorageType
