"""System REST Commands"""

from typing import Final, Protocol, TypedDict
from async_reolink.api.system import command as system

from .._utilities.providers import value as providers
from .._utilities.dictlist import DictList

from .model import UserInfo, DaylightSavingsTimeInfo, DeviceInfo, TimeInfo, StorageInfo

from ..connection.model import (
    Request,
    ResponseTypes,
    Response as RestResponse,
)

from .capabilities import UpdatableCapabilities

# pylint:disable=missing-function-docstring
# pylint: disable=too-few-public-methods


class GetAbilitiesRequest(Request, system.GetAbilitiesRequest):
    """REST Get Capabilities Request"""

    class Parameter(Protocol):
        """Parameter"""

        class User(Protocol):
            class JSON(UserInfo.JSON):
                """JSON"""

            class Keys(UserInfo.Keys, Protocol):
                """Keys"""

        class JSON(TypedDict):
            """JSON"""

            User: "GetAbilitiesRequest.Parameter.User.JSON"

        class Keys(Protocol):
            """Keys"""

            user: Final = "User"

    __slots__ = ()

    COMMAND: Final = "GetAbility"
    _COMMAND_ID: Final = hash(COMMAND)

    _NO_USER: Final = "NULL"
    _NO_USER_ID: Final = hash(_NO_USER)

    def __init__(self, /, user_name: str = ...) -> None:
        super().__init__(command=type(self).COMMAND, response_type=ResponseTypes.VALUE_ONLY)
        if user_name is not ...:
            self.user_name = user_name
        else:
            self._id = self._COMMAND_ID ^ self._NO_USER_ID

    def _get_user(self, create=False) -> Parameter.User.JSON:
        return self.lookup_value(
            self._get_parameter,
            self.Parameter.Keys.user,
            create=create,
            default_factory=lambda: dict() if create else None,
        )

    @property
    def _user(self):
        return self._get_user()

    @property
    def id(self):
        return self._id

    @property
    def user_name(self):
        if value := self._user:
            return value.get(self.Parameter.User.Keys.user_name, "")
        return ""

    @user_name.setter
    def user_name(self, value):
        self._get_user(True)[self.Parameter.User.Keys.user_name] = (
            str(value) if value else self._NO_USER
        )
        self._id = self._COMMAND_ID ^ (self._NO_USER_ID if not value else hash(value))


class GetAbilitiesResponse(RestResponse, system.GetAbilitiesResponse):
    """REST Get Capability Response"""

    @classmethod
    def from_response(cls, response: any, /, request: Request | None = None, **kwargs: any):
        if super().is_response(response, GetAbilitiesRequest.COMMAND):
            return GetAbilitiesResponse(
                response, request_id=request.id if request else None, **kwargs
            )
        return None

    class Value(Protocol):
        """Value"""

        class JSON(TypedDict):
            """JSON"""

            Ability: dict

        class Keys(Protocol):
            """Keys"""

            capabilities: Final = "Ability"

    __slots__ = ()

    _get_value: providers.FactoryValue[Value.JSON]
    _value: Value.JSON

    @property
    def capabilities(self):
        return UpdatableCapabilities(
            self.lookup_factory(self._get_value, self.Value.Keys.capabilities, default=None)
        )


class GetDeviceInfoRequest(Request, system.GetDeviceInfoRequest):
    """REST Get Device Info Request"""

    COMMAND: Final = "GetDevInfo"
    _COMMAND_ID: Final = hash(COMMAND)

    @property
    def id(self):
        return self._COMMAND_ID

    def __init__(self, response_type: ResponseTypes = ResponseTypes.VALUE_ONLY) -> None:
        super().__init__(command=type(self).COMMAND, response_type=response_type)


class GetDeviceInfoResponse(RestResponse, system.GetDeviceInfoResponse):
    """REST Get Device Info Response"""

    @classmethod
    def from_response(cls, response: any, /, request: Request | None = None, **kwargs):
        if super().is_response(response, GetDeviceInfoRequest.COMMAND):
            return cls(response, request_id=request.id if request else None, **kwargs)
        return None

    class Value(Protocol):
        """Value"""

        class JSON(TypedDict):
            """JSON"""

            DevInfo: DeviceInfo.JSON

        class Keys(Protocol):
            """Keys"""

            info: Final = "DevInfo"

    __slots__ = ()

    _get_value: providers.FactoryValue[Value.JSON]
    _value: Value.JSON

    @property
    def info(self):
        return DeviceInfo(self.lookup_factory(self._get_value, self.Value.Keys.info, default=None))


class GetTimeRequest(Request, system.GetTimeRequest):
    """REST Get Time Request"""

    COMMAND: Final = "GetTime"
    _COMMAND_ID: Final = hash(COMMAND)

    @property
    def id(self):
        return self._COMMAND_ID

    def __init__(self, response_type: ResponseTypes = ResponseTypes.VALUE_ONLY) -> None:
        super().__init__(command=type(self).COMMAND, response_type=response_type)


class GetTimeResponse(RestResponse, system.GetTimeResponse):
    """REST Get Time Response"""

    @classmethod
    def from_response(cls, response: any, /, request: Request | None = None, **kwargs):
        if super().is_response(response, GetTimeRequest.COMMAND):
            t = GetTimeResponse(response, request_id=request.id if request else None, **kwargs)
            return cls(response, request_id=request.id if request else None, **kwargs)
        return None

    class Value(Protocol):
        """Value"""

        class JSON(TypedDict):
            """JSON"""

            Dst: DaylightSavingsTimeInfo.JSON
            Time: TimeInfo.JSON

        class Keys(Protocol):
            """Keys"""

            dst: Final = "Dst"
            time: Final = "Time"

    __slots__ = ()

    _get_value: providers.FactoryValue[Value.JSON]
    _value: Value.JSON

    @property
    def dst(self):
        return DaylightSavingsTimeInfo(
            self.lookup_factory(self._get_value, self.Value.Keys.dst, default=None)
        )

    @property
    def time(self):
        return TimeInfo(self.lookup_factory(self._get_value, self.Value.Keys.time, default=None))


class RebootRequest(Request, system.RebootRequest):
    """REST Reboot Request"""

    __slots__ = ()

    COMMAND: Final = "Reboot"
    _COMMAND_ID: Final = hash(COMMAND)

    @property
    def id(self):
        return self._COMMAND_ID

    def __init__(self, response_type: ResponseTypes = ResponseTypes.VALUE_ONLY) -> None:
        super().__init__(command=type(self).COMMAND, response_type=response_type)


class GetHddInfoRequest(Request, system.GetHddInfoRequest):
    """REST Get HDD Info Request"""

    __slots__ = ()

    COMMAND: Final = "GetHddInfo"
    _COMMAND_ID: Final = hash(COMMAND)

    @property
    def id(self):
        return self._COMMAND_ID

    def __init__(self, response_type: ResponseTypes = ResponseTypes.VALUE_ONLY) -> None:
        super().__init__(command=type(self).COMMAND, response_type=response_type)


class GetHddInfoResponse(RestResponse, system.GetHddInfoResponse):
    """REST Get HDD Info Response"""

    @classmethod
    def from_response(cls, response: any, /, request: Request | None = None, **kwargs):
        if super().is_response(response, GetHddInfoRequest.COMMAND):
            return cls(response, request_id=request.id if request else None, **kwargs)
        return None

    class Value(Protocol):
        """Value"""

        class JSON(TypedDict):
            """JSON"""

            HddInfo: list[StorageInfo.JSON]

        class Keys(Protocol):
            """Keys"""

            info: Final = "HddInfo"

    __slots__ = ()

    _get_value: providers.FactoryValue[Value.JSON]
    _value: Value.JSON

    @property
    def info(self) -> DictList[int, StorageInfo]:
        return DictList(
            StorageInfo.Keys.id,
            self.lookup_factory(self._get_value, self.Value.Keys.info, default=None),
            StorageInfo,
        )
