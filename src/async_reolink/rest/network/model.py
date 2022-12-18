"""REST Network Models"""

from typing import TYPE_CHECKING, Callable, Final, Mapping, Protocol, Sequence, TypedDict, cast
from async_reolink.api.network import typing as network_typing

from .._utilities import providers

from ..connection.model import RequestWithChannel

from .. import model

from ..network.typing import link_types_str

# pylint: disable=missing-function-docstring


class IPInfo(providers.DictProvider[str, any], network_typing.IPInfo):
    """REST IP Info"""

    class JSON(TypedDict):
        """JSON"""

        gateway: str
        ip: str
        mask: str

    class Keys(Protocol):
        """Keys"""

        gateway: Final = "gateway"
        address: Final = "ip"
        address_mask: Final = "mask"

    __slots__ = ()

    _provided_value: JSON

    @property
    def gateway(self):
        if value := self._provided_value:
            return value.get(self.Keys.gateway, "")
        return ""

    @property
    def address(self):
        if value := self._provided_value:
            return value.get(self.Keys.address, "")
        return ""

    @property
    def address_mask(self):
        if value := self._provided_value:
            return value.get(self.Keys.address_mask, "")
        return ""


class _DNSList(providers.DictProvider[str, any], Sequence[str]):

    __slots__ = ("__prefix",)

    def __init__(self, prefix: str, value: providers.ProvidedDict[str, any] | None = None) -> None:
        super().__init__(value)
        self.__prefix = prefix


class DNSInfo(providers.DictProvider[str, any], network_typing.DNSInfo):
    """REST DNS Info"""

    class JSON(TypedDict):
        """JSON"""

        auto: int
        dns1: str
        dns2: str

    class Keys(Protocol):
        """Keys"""

        auto: Final = "auto"
        dns: Final = "dns"

    __slots__ = ()

    _provided_value: JSON

    @property
    def auto(self):
        return True if (value := self._provided_value) and value.get(self.Keys.auto, 0) else False

    @property
    def dns(self):
        return _DNSList(self.Keys.dns, lambda _: self._provided_value)


_DefaultLinkType: Final = network_typing.LinkTypes.DHCP
_DefaultLinkTypeStr: Final = link_types_str(_DefaultLinkType)


class LinkInfo(providers.DictProvider[str, any], network_typing.LinkInfo):
    """REST Link Info"""

    class JSON(TypedDict):
        """JSON"""

        activeLink: str
        mac: str
        type: str
        static: IPInfo.JSON
        dns: DNSInfo.JSON

    class Keys(Protocol):
        """Keys"""

        active_link: Final = "activeLink"
        mac: Final = "mac"
        type: Final = "type"
        ip: Final = "static"
        dns: Final = "dns"

    __slots__ = ()

    _provided_value: JSON

    @property
    def active_link(self):
        if value := self._provided_value:
            return value.get(self.Keys.active_link, "")
        return ""

    @property
    def mac(self):
        if value := self._provided_value:
            return value.get(self.Keys.mac, "")
        return ""

    @property
    def type(self):
        if value := self._provided_value:
            return network_typing.LinkTypes(value.get(self.Keys.type, _DefaultLinkTypeStr))
        return _DefaultLinkType

    @property
    def _static(self):
        if value := self._provided_value:
            return value.get(self.Keys.ip)
        return None

    @property
    def ip(self):
        return IPInfo(lambda _: self._static)

    @property
    def _dns(self):
        if value := self._provided_value:
            return value.get(self.Keys.dns)
        return None

    def dns(self):
        return DNSInfo(lambda _: self._dns)


class ChannelStatus(providers.DictProvider[str, any], network_typing.ChannelStatus):
    """REST Channel Status"""

    class JSON(RequestWithChannel.Parameter.JSON):
        """JSON"""

        name: str
        online: int
        typeInfo: str

    class Keys(RequestWithChannel.Parameter.Keys, Protocol):
        """Keys"""

        name: Final = "name"
        online: Final = "online"
        type: Final = "typeInfo"

    __slots__ = ()

    _provided_value: JSON

    @property
    def channel_id(self):
        if value := self._provided_value:
            return value.get(self.Keys.channel_id, 0)
        return 0

    @property
    def name(self):
        if value := self._provided_value:
            return value.get(self.Keys.name, "")
        return ""

    @property
    def online(self):
        return True if (value := self._provided_value) and value.get(self.Keys.online, 0) else False

    @property
    def type(self):
        if value := self._provided_value:
            return value.get(self.Keys.type, "")
        return ""


class ChannelStatuses(providers.DictProvider[str, any], Mapping[int, ChannelStatus]):
    """Channel Statuses"""

    class JSON(TypedDict):
        """JSON"""

        status: list[ChannelStatus.JSON]
        count: int

    class Keys(Protocol):
        """Keys"""

        status: Final = "status"
        count: Final = "count"

    __slots__ = ()

    _provided_value: JSON

    @property
    def _status(self):
        if value := self._provided_value:
            return value.get(self.Keys.status, [])
        return []

    def __getitem__(self, __k: int):
        return ChannelStatus(lambda _: self._status[__k])

    def __iter__(self):
        if not (channels := self._status):
            return
        for _c in channels:
            if (
                isinstance(_c, dict)
                and (channel := _c.get(ChannelStatus.Keys.channel_id, None)) is not None
            ):
                yield int(channel)

    def __contains__(self, __o: int):
        if not (channels := self._status):
            return False
        for _c in channels:
            if (
                isinstance(_c, dict)
                and (channel := _c.get(ChannelStatus.Keys.channel_id, None)) is not None
                and channel == __o
            ):
                return True
        return False

    def __len__(self):
        if not (value := self.__value):
            return 0
        return int(value.get(self.Keys.count, 0))


class UpdatableChannelStatuses(ChannelStatuses):
    """Updatable REST Channel Statuses"""

    def update(self, value: ChannelStatuses):
        if not isinstance(value, ChannelStatuses):
            raise TypeError("Can only update from another ChannelStatuses")
        # pylint: disable=protected-access
        self._set_value(value._provided_value)
        return self


class P2PInfo(providers.DictProvider[str, any], network_typing.P2PInfo):
    """REST P2P Info"""

    class JSON(TypedDict):
        """JSON"""

        enable: int
        uid: str

    class Keys(Protocol):
        """Keys"""

        enabled: Final = "enable"
        uid: Final = "uid"

    __slots__ = ()

    _provided_value: JSON

    @property
    def enabled(self):
        return (
            True if (value := self._provided_value) and value.get(self.Keys.enabled, 0) else False
        )

    @property
    def uid(self):
        if value := self._provided_value:
            return value.get(self.Keys.uid, "")
        return ""


class NetworkPort(providers.DictProvider[str, any], model._ManglesKeys, network_typing.NetworkPort):
    """REST Network Port"""

    class JSON(TypedDict):
        """JSON"""

        Enable: int
        Port: int

    class Keys(Protocol):
        """Keys"""

        enabled: Final = "Enable"
        value: Final = "Port"

    __slots__ = ()

    def __init__(self, prefix: str, value: providers.ProvidedDict[str, any] | None = None) -> None:
        super().__init__(value)
        model._ManglesKeys.__init__(self, prefix)

    _provided_value: JSON

    @property
    def value(self):
        if value := self._provided_value:
            return value.get(self._mangle_key(self.Keys.value), 0)
        return 0

    @property
    def enabled(self):
        if value := self._provided_value:
            if (enabled := value.get(self._mangle_key(self.Keys.enabled))) is not None:
                return True if enabled else False
            # older firmwares dont support Enable so the port cannot be disabled, so we default to true if Port exists
            return bool(self.value)
        return False

    def __bool__(self):
        return self.enabled

    def __int__(self):
        return self.value if self.enabled else 0

    def __str__(self):
        return str(self.value) if self.enabled else ""


class NetworkPorts(providers.DictProvider[str, any], network_typing.NetworkPorts):
    """REST Network Ports"""

    __slots__ = ()

    def _port(self, prefix: str):
        return NetworkPort(prefix, lambda _: self._provided_value)

    @property
    def media(self):
        return self._port("media")

    @property
    def http(self):
        return self._port("http")

    @property
    def https(self):
        return self._port("https")

    @property
    def onvif(self):
        return self._port("onvif")

    @property
    def rtsp(self):
        return self._port("rtsp")

    @property
    def rtmp(self):
        return self._port("rtmp")


class WifiInfo(providers.DictProvider[str, any], network_typing.WifiInfo):
    """REST Wifi Info"""

    class JSON(TypedDict):
        """JSON"""

        ssid: str
        password: str

    class Keys(Protocol):
        """Keys"""

        ssid: Final = "ssid"
        password: Final = "password"

    __slots__ = ()

    _provided_value: JSON

    @property
    def ssid(self):
        if value := self._provided_value:
            return value.get(self.Keys.ssid, "")
        return ""

    @property
    def password(self):
        if value := self._provided_value:
            return value.get(self.Keys.password, "")
        return ""
