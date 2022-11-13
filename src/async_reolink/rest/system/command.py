"""System REST Commands"""

from typing import Final
from async_reolink.api.system import command as system

from .._utilities.dictlist import DictList

from .model import DaylightSavingsTimeInfo, DeviceInfo, TimeInfo, StorageInfo

from ..connection.model import (
    Request,
    ResponseTypes,
    Response as RestResponse,
)

from .capabilities import Capabilities

# pylint:disable=missing-function-docstring
# pylint: disable=too-few-public-methods


class GetAbilitiesRequest(Request, system.GetAbilitiesRequest):
    """REST Get Capabilities Request"""

    __slots__ = ()

    COMMAND: Final = "GetAbility"

    def __init__(
        self,
        username: str | None,
        response_type: ResponseTypes = ResponseTypes.VALUE_ONLY,
    ) -> None:
        super().__init__()
        self.command = type(self).COMMAND
        self.response_type = response_type
        self.user_name = username or "NULL"

    def _get_user(self, create=False) -> dict:
        _key: Final = "User"
        if (parameter := self._get_parameter(create)) is None:
            return None
        if _key in parameter or not create:
            return parameter.get(_key, None)
        return parameter.setdefault(_key, {})

    @property
    def _user(self) -> dict:
        return self._get_user(True)

    @property
    def user_name(self) -> str:
        return value.get("userName", "") if (value := self._get_user()) is not None else ""

    @user_name.setter
    def user_name(self, value):
        self._user["userName"] = value


class GetAbilitiesResponse(RestResponse, system.GetAbilitiesResponse):
    """REST Get Capability Response"""

    @classmethod
    def from_response(cls, response: any, request: Request | None = None):
        if super().is_response(response, GetAbilitiesRequest.COMMAND):
            return cls(response, request_id=request.id if request else None)
        return None

    __slots__ = ()

    def _get_ability(self) -> dict:
        return value.get("Ability", None) if (value := self._get_value()) is not None else None

    @property
    def capabilities(self):
        # we are not passing the factory here since this object is meant to be updatable
        return Capabilities(self._get_ability())


class GetDeviceInfoRequest(Request, system.GetDeviceInfoRequest):
    """REST Get Device Info Request"""

    COMMAND: Final = "GetDevInfo"

    def __init__(self, response_type: ResponseTypes = ResponseTypes.VALUE_ONLY) -> None:
        super().__init__()
        self.command = type(self).COMMAND
        self.response_type = response_type


class GetDeviceInfoResponse(RestResponse, system.GetDeviceInfoResponse):
    """REST Get Device Info Response"""

    @classmethod
    def from_response(cls, response: any, request: Request | None = None):
        if super().is_response(response, GetDeviceInfoRequest.COMMAND):
            return cls(response, request_id=request.id if request else None)
        return None

    __slots__ = ()

    def _get_info(self) -> dict:
        return value.get("DevInfo", None) if (value := self._get_value()) is not None else None

    @property
    def info(self):
        """device info"""
        # we are not passing the factory here since this object is meant to be updatable
        return DeviceInfo(self._get_info())


class GetTimeRequest(Request, system.GetTimeRequest):
    """REST Get Time Request"""

    COMMAND: Final = "GetTime"

    def __init__(self, response_type: ResponseTypes = ResponseTypes.VALUE_ONLY) -> None:
        super().__init__()
        self.command = type(self).COMMAND
        self.response_type = response_type


class GetTimeResponse(RestResponse, system.GetTimeResponse):
    """REST Get Time Response"""

    @classmethod
    def from_response(cls, response: any, request: Request | None = None):
        if super().is_response(response, GetTimeRequest.COMMAND):
            return cls(response, request_id=request.id if request else None)
        return None

    __slots__ = ()

    def _get_dst(self) -> dict:
        return value.get("Dst", None) if (value := self._get_value()) is not None else None

    @property
    def dst(self):
        return DaylightSavingsTimeInfo(self._get_dst)

    def _get_time(self) -> dict:
        return value.get("Time", None) if (value := self._get_value()) is not None else None

    @property
    def time(self):
        return TimeInfo(self._get_time)


class RebootRequest(Request, system.RebootRequest):
    """REST Reboot Request"""

    __slots__ = ()

    COMMAND: Final = "Reboot"

    def __init__(self, response_type: ResponseTypes = ResponseTypes.VALUE_ONLY) -> None:
        super().__init__()
        self.command = type(self).COMMAND
        self.response_type = response_type


class GetHddInfoRequest(Request, system.GetHddInfoRequest):
    """REST Get HDD Info Request"""

    __slots__ = ()

    COMMAND: Final = "GetHddInfo"

    def __init__(self, response_type: ResponseTypes = ResponseTypes.VALUE_ONLY) -> None:
        super().__init__()
        self.command = type(self).COMMAND
        self.response_type = response_type


class GetHddInfoResponse(RestResponse, system.GetHddInfoResponse):
    """REST Get HDD Info Response"""

    @classmethod
    def from_response(cls, response: any, request: Request | None = None):
        if super().is_response(response, GetHddInfoRequest.COMMAND):
            return cls(response, request_id=request.id if request else None)
        return None

    __slots__ = ()

    def _get_info(self) -> list:
        return value.get("HddInfo", None) if (value := self._get_value()) is not None else None

    @property
    def info(self):
        return DictList("number", self._get_info(), StorageInfo)
