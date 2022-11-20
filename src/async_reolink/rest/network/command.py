"""REST Network Commands"""

from typing import Callable, Final, Mapping
from async_reolink.api.network import command as network

from async_reolink.api.typing import StreamTypes
from ..typing import STREAMTYPES_STR_MAP
from ..model import MinMaxRange

from . import model

from ..connection.model import (
    _CHANNEL_KEY,
    Request,
    ResponseTypes,
    Response as RestCommandResponse,
)


# pylint:disable=missing-function-docstring
# pylint: disable=too-few-public-methods


class GetLocalLinkRequest(Request, network.GetLocalLinkRequest):
    """REST Get Local Link Request"""

    __slots__ = ()

    COMMAND: Final = "GetLocalLink"

    def __init__(self, response_type: ResponseTypes = ResponseTypes.VALUE_ONLY) -> None:
        super().__init__()
        self.command = type(self).COMMAND
        self.response_type = response_type


class GetLocalLinkResponse(RestCommandResponse, network.GetLocalLinkResponse):
    """REST Get Local Link Response"""

    @classmethod
    def from_response(cls, response: any, request: Request | None = None):
        if super().is_response(response, GetLocalLinkRequest.COMMAND):
            return cls(response, request_id=request.id if request else None)
        return None

    __slots__ = ()

    def _local_link(self) -> dict:
        return value.get("LocalLink", None) if (value := self._get_value()) is not None else None

    @property
    def local_link(self):
        # we are not passing the factory here since this object is meant to be detachable
        return model.LinkInfo(self._local_link())


class GetChannelStatusRequest(Request, network.GetChannelStatusRequest):
    """REST Get Channel Status Request"""

    __slots__ = ()

    COMMAND: Final = "GetChannelstatus"

    def __init__(self, response_type: ResponseTypes = ResponseTypes.VALUE_ONLY) -> None:
        super().__init__()
        self.command = type(self).COMMAND
        self.response_type = response_type


class GetChannelStatusResponse(RestCommandResponse, network.GetChannelStatusResponse):
    """REST Get Channel Status Response"""

    @classmethod
    def from_response(cls, response: any, request: Request | None = None):
        if super().is_response(response, GetChannelStatusRequest.COMMAND):
            return cls(response, request_id=request.id if request else None)
        return None

    __slots__ = ()

    @property
    def channels(self):
        # we are not passing the factory here since this object is meant to be detachable
        return model.ChannelStatuses(self._get_value())


class GetNetworkPortsRequest(Request, network.GetNetworkPortsRequest):
    """REST Get Network Ports"""

    __slots__ = ()

    COMMAND: Final = "GetNetPort"

    def __init__(self, response_type: ResponseTypes = ResponseTypes.VALUE_ONLY) -> None:
        super().__init__()
        self.command = type(self).COMMAND
        self.response_type = response_type


class GetNetworkPortsResponse(RestCommandResponse, network.GetNetworkPortsResponse):
    """REST Get Local Link Response"""

    @classmethod
    def from_response(cls, response: any, request: Request | None = None):
        if super().is_response(response, GetNetworkPortsRequest.COMMAND):
            return cls(response, request_id=request.id if request else None)
        return None

    __slots__ = ()

    def _get_ports(self) -> dict:
        return value.get("NetPort", None) if (value := self._get_value()) is not None else None

    @property
    def ports(self):
        # we are not passing the factory here since this object is meant to be detachable
        return model.NetworkPorts(self._get_ports())


class GetRTSPUrlsRequest(Request, network.GetRTSPUrlsRequest):
    """REST Get RTSP Urls Request"""

    __slots__ = ()

    COMMAND: Final = "GetRtspUrl"

    def __init__(
        self,
        channel_id: int = 0,
        response_type: ResponseTypes = ResponseTypes.VALUE_ONLY,
    ) -> None:
        super().__init__()
        self.command = type(self).COMMAND
        self.response_type = response_type
        self.channel_id = channel_id


class _RTSPUrls(Mapping[StreamTypes, str]):
    __slots__ = ("_value",)

    def __init__(self, value: dict) -> None:
        self._value = value

    def _factory(self):
        return self._value

    def __getitem__(self, __k: StreamTypes) -> str:
        if (value := self._factory()) is None:
            return None
        return value.get(STREAMTYPES_STR_MAP[__k] + "Stream", None)

    def __contains__(self, __o: StreamTypes) -> bool:
        if (value := self._factory()) is None:
            return False
        return STREAMTYPES_STR_MAP[__o] + "Stream" in value

    def __iter__(self):
        if (value := self._factory()) is None:
            return
        for _k, _v in STREAMTYPES_STR_MAP.items():
            if _v + "Stream" in value:
                yield _k

    def __len__(self) -> int:
        if (value := self._factory()) is None:
            return 0
        return len((True for _v in STREAMTYPES_STR_MAP.values() if _v + "Stream" in value))


class GetRTSPUrlsResponse(RestCommandResponse, network.GetRTSPUrlsResponse):
    """REST Get RTSP Urls Response"""

    @classmethod
    def from_response(cls, response: any, request: Request | None = None):
        if super().is_response(response, GetRTSPUrlsRequest.COMMAND):
            return cls(response, request_id=request.id if request else None)
        return None

    __slots__ = ()

    def _get_urls(self) -> dict:
        return value.get("rtspUrl", None) if (value := self._get_value()) is not None else None

    @property
    def channel_id(self) -> int:
        return value.get(_CHANNEL_KEY, 0) if (value := self._get_urls()) is not None else 0

    @property
    def urls(self):
        # we are not passing the factory here since this object is meant to be detachable
        return _RTSPUrls(self._get_urls())


class GetP2PRequest(Request, network.GetP2PRequest):
    """REST Get Local Link Request"""

    __slots__ = ()

    COMMAND: Final = "GetP2p"

    def __init__(self, response_type: ResponseTypes = ResponseTypes.VALUE_ONLY) -> None:
        super().__init__()
        self.command = type(self).COMMAND
        self.response_type = response_type


class GetP2PResponse(RestCommandResponse, network.GetP2PResponse):
    """REST Get P2P Response"""

    @classmethod
    def from_response(cls, response: any, request: Request | None = None):
        if super().is_response(response, GetP2PRequest.COMMAND):
            return cls(response, request_id=request.id if request else None)
        return None

    __slots__ = ()

    def _get_info(self) -> dict:
        return value.get("P2p", None) if (value := self._get_value()) is not None else None

    @property
    def info(self):
        # we are not passing the factory here since this object is meant to be detachable
        return model.P2PInfo(self._get_info())


class GetWifiInfoRequest(Request, network.GetWifiInfoRequest):
    """REST Get Wifi Info Request"""

    __slots__ = ()

    COMMAND: Final = "GetWifi"

    def __init__(self, response_type: ResponseTypes = ResponseTypes.VALUE_ONLY) -> None:
        super().__init__()
        self.command = type(self).COMMAND
        self.response_type = response_type


class GetWifiInfoResponse(RestCommandResponse, network.GetWifiInfoResponse):
    """REST Get Wifi Info Response"""

    @classmethod
    def from_response(cls, response: any, request: Request | None = None):
        if super().is_response(response, GetWifiInfoRequest.COMMAND):
            return cls(response, request_id=request.id if request else None)
        return None

    __slots__ = ()

    def _get_info(self) -> dict:
        return value.get("Wifi", None) if (value := self._get_value()) is not None else None

    @property
    def info(self):
        # we are not passing the factory here since this object is meant to be detachable
        return model.WifiInfo(self._get_info())


class GetWifiSignalRequest(Request, network.GetWifiSignalRequest):
    """REST Get Signal Strength Request"""

    __slots__ = ()

    COMMAND: Final = "GetWifiSignal"

    def __init__(self, response_type: ResponseTypes = ResponseTypes.VALUE_ONLY) -> None:
        super().__init__()
        self.command = type(self).COMMAND
        self.response_type = response_type


_SIGNAL_KEY: Final = "wifiSignal"


class GetWifiSignalResponse(RestCommandResponse, network.GetWifiSignalResponse):
    """REST Get Wifi Signal Strength Response"""

    @classmethod
    def from_response(cls, response: any, request: Request | None = None):
        if super().is_response(response, GetWifiSignalRequest.COMMAND):
            return cls(response, request_id=request.id if request else None)
        return None

    __slots__ = ()

    def _get_info(self, factory: Callable[[], dict]):
        def _factory() -> dict:
            return value.get("WifiSignal", None) if (value := factory()) is not None else None

        return _factory

    @property
    def signal(self) -> int:
        if (value := self._get_value()) is None:
            return 0
        return value.get(_SIGNAL_KEY, 0)

    @property
    def initial_signal(self) -> int | None:
        if (value := self._get_initial()) is None:
            return None
        return value.get(_SIGNAL_KEY, 0)

    @property
    def signal_range(self):
        if (value := self._get_range()) is None:
            return None

        def _factory():
            return value

        return MinMaxRange("", _factory)
