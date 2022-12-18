"""REST Network Commands"""

from typing import Callable, Final, Mapping, Protocol, TypedDict
from async_reolink.api.network import command as network

from async_reolink.api.typing import StreamTypes
from ...rest.typing import stream_type_str
from ..model import MinMaxRange

from .._utilities import providers

from . import model

from ..connection.model import (
    Request,
    ResponseTypes,
    Response as RestCommandResponse,
    ResponseWithChannel,
)


# pylint:disable=missing-function-docstring
# pylint: disable=too-few-public-methods


class GetLocalLinkRequest(Request, network.GetLocalLinkRequest):
    """REST Get Local Link Request"""

    __slots__ = ()

    COMMAND: Final = "GetLocalLink"
    _COMMAND_ID: Final = hash(COMMAND)

    @property
    def id(self):
        return self._COMMAND_ID

    def __init__(self, response_type: ResponseTypes = ResponseTypes.VALUE_ONLY) -> None:
        super().__init__()
        self.command = type(self).COMMAND
        self.response_type = response_type


class GetLocalLinkResponse(RestCommandResponse, network.GetLocalLinkResponse):
    """REST Get Local Link Response"""

    @classmethod
    def from_response(cls, response: any, /, request: Request | None = None, **kwargs):
        if super().is_response(response, GetLocalLinkRequest.COMMAND):
            return cls(response, request_id=request.id if request else None, **kwargs)
        return None

    class Value(Protocol):
        """Value"""

        class JSON(TypedDict):
            """JSON"""

            LocalLink: model.LinkInfo.JSON

        class Keys(Protocol):
            """Keys"""

            local_link: Final = "LocalLink"

    __slots__ = ()

    _value: Value.JSON

    @property
    def local_link(self):
        return model.LinkInfo(self._value.get(self.Value.Keys.local_link))


class GetChannelStatusRequest(Request, network.GetChannelStatusRequest):
    """REST Get Channel Status Request"""

    __slots__ = ()

    COMMAND: Final = "GetChannelstatus"
    _COMMAND_ID: Final = hash(COMMAND)

    @property
    def id(self):
        return self._COMMAND_ID

    def __init__(self, response_type: ResponseTypes = ResponseTypes.VALUE_ONLY) -> None:
        super().__init__()
        self.command = type(self).COMMAND
        self.response_type = response_type


class GetChannelStatusResponse(RestCommandResponse, network.GetChannelStatusResponse):
    """REST Get Channel Status Response"""

    @classmethod
    def from_response(cls, response: any, /, request: Request | None = None, **kwargs):
        if super().is_response(response, GetChannelStatusRequest.COMMAND):
            return cls(response, request_id=request.id if request else None, **kwargs)
        return None

    class Value(Protocol):
        """Value"""

        JSON = model.ChannelStatuses.JSON
        Keys = model.ChannelStatuses.Keys

    __slots__ = ()

    _value: Value.JSON

    @property
    def channels(self):
        return model.UpdatableChannelStatuses(self._value)


class GetNetworkPortsRequest(Request, network.GetNetworkPortsRequest):
    """REST Get Network Ports"""

    __slots__ = ()

    COMMAND: Final = "GetNetPort"
    _COMMAND_ID: Final = hash(COMMAND)

    @property
    def id(self):
        return self._COMMAND_ID

    def __init__(self, response_type: ResponseTypes = ResponseTypes.VALUE_ONLY) -> None:
        super().__init__()
        self.command = type(self).COMMAND
        self.response_type = response_type


class GetNetworkPortsResponse(RestCommandResponse, network.GetNetworkPortsResponse):
    """REST Get Local Link Response"""

    @classmethod
    def from_response(cls, response: any, /, request: Request | None = None, **kwargs):
        if super().is_response(response, GetNetworkPortsRequest.COMMAND):
            return cls(response, request_id=request.id if request else None, **kwargs)
        return None

    __slots__ = ()

    class Value(Protocol):
        """Value"""

        class JSON(TypedDict):
            """JSON"""

            NetPort: dict

        class Keys(Protocol):
            """Keys"""

            ports: Final = "NetPort"

    _value: Value.JSON

    @property
    def ports(self):
        return model.NetworkPorts(self._value.get(self.Value.Keys.ports))


class GetRTSPUrlsRequest(Request, network.GetRTSPUrlsRequest):
    """REST Get RTSP Urls Request"""

    __slots__ = ()

    COMMAND: Final = "GetRtspUrl"
    _COMMAND_ID: Final = hash(COMMAND)

    def __init__(
        self,
        channel_id: int = 0,
        response_type: ResponseTypes = ResponseTypes.VALUE_ONLY,
    ) -> None:
        super().__init__()
        self.command = type(self).COMMAND
        self.response_type = response_type
        self.channel_id = channel_id

    @property
    def id(self):
        return self._COMMAND_ID ^ self.channel_id


class _RTSPUrls(providers.DictProvider[str, any], Mapping[StreamTypes, str]):

    _SUFFIX: Final = "Stream"

    __slots__ = ()

    def __getitem__(self, __k: StreamTypes) -> str:
        if (value := self._provided_value) is None:
            return None
        return value.get(stream_type_str(__k) + self._SUFFIX, None)

    def __contains__(self, __o: StreamTypes) -> bool:
        if (value := self._provided_value) is None:
            return False
        return stream_type_str(__o) + self._SUFFIX in value

    def __iter__(self):
        if (value := self._provided_value) is None:
            return
        for _k in StreamTypes:
            if stream_type_str(_k) + self._SUFFIX in value:
                yield _k

    def __len__(self) -> int:
        if (value := self._provided_value) is None:
            return 0
        return len((True for _v in stream_type_str() if _v + self._SUFFIX in value))


class GetRTSPUrlsResponse(RestCommandResponse, network.GetRTSPUrlsResponse):
    """REST Get RTSP Urls Response"""

    @classmethod
    def from_response(cls, response: any, /, request: Request | None = None, **kwargs):
        if super().is_response(response, GetRTSPUrlsRequest.COMMAND):
            return cls(response, request_id=request.id if request else None, **kwargs)
        return None

    class Value(Protocol):
        """Value"""

        class JSON(TypedDict):
            """JSON"""

            rtspUrl: dict

        class Keys(Protocol):
            """Keys"""

            urls: Final = "rtspUrl"

    __slots__ = ()

    _value: Value.JSON

    def _get_urls(self, create=False) -> dict:
        if value := self._get_provided_value(create):
            return value.get(self.Value.Keys.urls)
        return None

    _urls: dict = property(_get_urls)

    @property
    def channel_id(self):
        value: ResponseWithChannel.Value.JSON
        if value := self._urls:
            return value.get(ResponseWithChannel.Value.Keys.channel_id, 0)
        return 0

    @property
    def urls(self):
        # we are not passing the factory here since this object is meant to be detachable
        return _RTSPUrls(self._urls)


class GetP2PRequest(Request, network.GetP2PRequest):
    """REST Get Local Link Request"""

    __slots__ = ()

    COMMAND: Final = "GetP2p"
    _COMMAND_ID: Final = hash(COMMAND)

    @property
    def id(self):
        return self._COMMAND_ID

    def __init__(self, response_type: ResponseTypes = ResponseTypes.VALUE_ONLY) -> None:
        super().__init__()
        self.command = type(self).COMMAND
        self.response_type = response_type


class GetP2PResponse(RestCommandResponse, network.GetP2PResponse):
    """REST Get P2P Response"""

    @classmethod
    def from_response(cls, response: any, /, request: Request | None = None, **kwargs):
        if super().is_response(response, GetP2PRequest.COMMAND):
            return cls(response, request_id=request.id if request else None, **kwargs)
        return None

    class Value(Protocol):
        """Value"""

        class JSON(TypedDict):
            """JSON"""

            P2p: model.P2PInfo.JSON

        class Keys(Protocol):
            """Keys"""

            info: Final = "P2p"

    __slots__ = ()

    _value: Value.JSON

    @property
    def info(self):
        # we are not passing the factory here since this object is meant to be detachable
        return model.P2PInfo(self._value.get(self.Value.Keys.info))


class GetWifiInfoRequest(Request, network.GetWifiInfoRequest):
    """REST Get Wifi Info Request"""

    __slots__ = ()

    COMMAND: Final = "GetWifi"
    _COMMAND_ID: Final = hash(COMMAND)

    @property
    def id(self):
        return self._COMMAND_ID

    def __init__(self, response_type: ResponseTypes = ResponseTypes.VALUE_ONLY) -> None:
        super().__init__()
        self.command = type(self).COMMAND
        self.response_type = response_type


class GetWifiInfoResponse(RestCommandResponse, network.GetWifiInfoResponse):
    """REST Get Wifi Info Response"""

    @classmethod
    def from_response(cls, response: any, /, request: Request | None = None, **kwargs):
        if super().is_response(response, GetWifiInfoRequest.COMMAND):
            return cls(response, request_id=request.id if request else None, **kwargs)
        return None

    class Value(Protocol):
        """Value"""

        class JSON(TypedDict):
            """JSON"""

            Wifi: model.WifiInfo.JSON

        class Keys(Protocol):
            """Keys"""

            info: Final = "Wifi"

    __slots__ = ()

    _value: Value.JSON

    def info(self):
        # we are not passing the factory here since this object is meant to be detachable
        return model.WifiInfo(self._value.get(self.Value.Keys.info))


class GetWifiSignalRequest(Request, network.GetWifiSignalRequest):
    """REST Get Signal Strength Request"""

    __slots__ = ()

    COMMAND: Final = "GetWifiSignal"
    _COMMAND_ID: Final = hash(COMMAND)

    @property
    def id(self):
        return self._COMMAND_ID

    def __init__(self, response_type: ResponseTypes = ResponseTypes.VALUE_ONLY) -> None:
        super().__init__()
        self.command = type(self).COMMAND
        self.response_type = response_type


class GetWifiSignalResponse(RestCommandResponse, network.GetWifiSignalResponse):
    """REST Get Wifi Signal Strength Response"""

    @classmethod
    def from_response(cls, response: any, /, request: Request | None = None, **kwargs):
        if super().is_response(response, GetWifiSignalRequest.COMMAND):
            return cls(response, request_id=request.id if request else None, **kwargs)
        return None

    class Value(Protocol):
        """Value"""

        class JSON(TypedDict):
            """JSON"""

            wifiSignal: int

        class Keys(Protocol):
            """Keys"""

            signal: Final = "wifiSignal"

    class Range(Protocol):
        """Range"""

        class JSON(TypedDict):
            """JSON"""

            wifiSignal: model.model.MinMaxRange.JSON

    __slots__ = ()

    _value: Value.JSON
    _initial: Value.JSON
    _range: Range.JSON

    @property
    def signal(self):
        if value := self._value:
            return value.get(self.Value.Keys.signal, 0)
        return 0

    @property
    def initial_signal(self):
        if value := self._initial:
            return value.get(self.Value.Keys.signal, 0)
        return 0

    @property
    def signal_range(self):
        return MinMaxRange(
            "", lambda _: value.get(self.Value.Keys.signal) if (value := self._range) else None
        )
