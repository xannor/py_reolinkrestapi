"""REST Network Models"""

from typing import Final, Mapping, Protocol, Sequence, TypeAlias, TypedDict
from typing_extensions import Unpack
from async_reolink.api.network import typing as network_typing

from .._utilities.providers import value as providers, mangle

from ..connection.model import RequestWithChannel

from ..network.typing import link_types_str

# pylint: disable=missing-function-docstring

_JSONDict: TypeAlias = dict[str, any]


class IPInfo(providers.Value[_JSONDict], network_typing.IPInfo):
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

    __get_value__: providers.FactoryValue[JSON]

    @property
    def gateway(self):
        if value := self.__get_value__():
            return value.get(self.Keys.gateway, "")
        return ""

    @property
    def address(self):
        if value := self.__get_value__():
            return value.get(self.Keys.address, "")
        return ""

    @property
    def address_mask(self):
        if value := self.__get_value__():
            return value.get(self.Keys.address_mask, "")
        return ""


def _parseint(value: str, default=None):
    if not value:
        return default
    try:
        return int(value)
    except ValueError:
        return default


class _DNSList(providers.Value[_JSONDict], Sequence[str]):

    __slots__ = ("__prefix", "__length")

    def __init__(
        self,
        prefix: str,
        value: providers.FactoryValue[_JSONDict] | _JSONDict | None = ...,
        /,
        **kwargs: any,
    ) -> None:
        super().__init__(value, **kwargs)
        self.__prefix = prefix
        self.__length = -1

    def __getitem__(self, key: int):
        return self.__get_value__()[self.__prefix + key]

    def __len__(self):
        if self.__length > -1:
            return self.__length
        if not (value := self.__get_value__()):
            return 0
        _l = 0
        for _k in value:
            if (
                _k.startswith(self.__prefix)
                and (_i := _parseint(_k[len(self.__prefix) :])) is not None
            ):
                _l = max(_l, _i)
        return _l


class DNSInfo(providers.Value[_JSONDict], network_typing.DNSInfo):
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

    __get_value__: providers.FactoryValue[JSON]

    @property
    def auto(self):
        return True if (value := self.__get_value__()) and value.get(self.Keys.auto, 0) else False

    @property
    def dns(self):
        return _DNSList(self.Keys.dns, self.__get_value__)


_DefaultLinkType: Final = network_typing.LinkTypes.DHCP
_DefaultLinkTypeStr: Final = link_types_str(_DefaultLinkType)


class LinkInfo(providers.Value[_JSONDict], network_typing.LinkInfo):
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

    __get_value__: providers.FactoryValue[JSON]

    @property
    def active_link(self):
        if value := self.__get_value__():
            return value.get(self.Keys.active_link, "")
        return ""

    @property
    def mac(self):
        if value := self.__get_value__():
            return value.get(self.Keys.mac, "")
        return ""

    @property
    def type(self):
        if value := self.__get_value__():
            return network_typing.LinkTypes(value.get(self.Keys.type, _DefaultLinkTypeStr))
        return _DefaultLinkType

    def _get_ip(self, create=False) -> IPInfo.JSON:
        return self.lookup_value(self.__get_value__, self.Keys.ip, create=create, default=None)

    @property
    def _ip(self):
        return self._get_ip()

    @property
    def ip(self):
        return IPInfo(self._get_ip)

    def _get_dns(self, create=False) -> DNSInfo.JSON:
        return self.lookup_value(self.__get_value__, self.Keys.dns, create=create, default=None)

    @property
    def _dns(self):
        return self._get_dns()

    def dns(self):
        return DNSInfo(self._get_dns)


class ChannelStatus(providers.Value[_JSONDict], network_typing.ChannelStatus):
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

    __get_value__: providers.FactoryValue[JSON]

    @property
    def channel_id(self):
        if value := self.__get_value__():
            return value.get(self.Keys.channel_id, 0)
        return 0

    @property
    def name(self):
        if value := self.__get_value__():
            return value.get(self.Keys.name, "")
        return ""

    @property
    def online(self):
        return True if (value := self.__get_value__()) and value.get(self.Keys.online, 0) else False

    @property
    def type(self):
        if value := self.__get_value__():
            return value.get(self.Keys.type, "")
        return ""


class ChannelStatuses(providers.Value[_JSONDict], Mapping[int, ChannelStatus]):
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

    __get_value__: providers.FactoryValue[JSON]

    def _get_status(self, create=False) -> list[ChannelStatus.JSON]:
        return self.lookup_value(
            self.__get_value__, self.Keys.status, create=create, default_factory=list
        )

    def __getitem__(self, __k: int):
        return ChannelStatus(self.lookup_factory(self._get_status, __k, default=None))

    def __iter__(self):
        if not (channels := self._get_status()):
            return
        for _c in channels:
            if (
                isinstance(_c, dict)
                and (channel := _c.get(ChannelStatus.Keys.channel_id, None)) is not None
            ):
                yield int(channel)

    def __contains__(self, __o: int):
        if not (channels := self._get_status()):
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
        if not (value := self.__get_value__()):
            return 0
        return int(value.get(self.Keys.count, 0))


class UpdatableChannelStatuses(ChannelStatuses):
    """Updatable REST Channel Statuses"""

    def update(self, value: ChannelStatuses):
        if not isinstance(value, ChannelStatuses):
            raise TypeError("Can only update from another ChannelStatuses")
        # pylint: disable=protected-access
        self.__set_value__(value.__get_value__())
        return self


class P2PInfo(providers.Value[_JSONDict], network_typing.P2PInfo):
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

    __get_value__: providers.FactoryValue[JSON]

    @property
    def enabled(self):
        return (
            True if (value := self.__get_value__()) and value.get(self.Keys.enabled, 0) else False
        )

    @property
    def uid(self):
        if value := self.__get_value__():
            return value.get(self.Keys.uid, "")
        return ""


class NetworkPort(providers.Value[_JSONDict], network_typing.NetworkPort):
    """REST Network Port"""

    class JSON(TypedDict):
        """JSON"""

        Enable: int
        Port: int

    class Keys(Protocol):
        """Keys"""

        enabled: Final = "enable"
        value: Final = "port"

    __slots__ = ()

    __slots__ = ("_mangle_key",)

    def __init__(
        self,
        value: providers.FactoryValue[_JSONDict] | _JSONDict | None = ...,
        /,
        **kwargs: Unpack[mangle.mangler_kwargs],
    ) -> None:
        super().__init__(value, **{k: kwargs[k] for k in kwargs if k not in mangle.mangler_kwkeys})
        self._mangle_key = mangle.mangler(**kwargs)

    __get_value__: providers.FactoryValue[JSON]

    @property
    def value(self):
        if value := self.__get_value__():
            return value.get(self._mangle_key(self.Keys.value), 0)
        return 0

    @property
    def enabled(self):
        if value := self.__get_value__():
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


class NetworkPorts(providers.Value[_JSONDict], network_typing.NetworkPorts):
    """REST Network Ports"""

    __slots__ = ()

    def _port(self, prefix: str):
        return NetworkPort(self.__get_value__, prefix=prefix, titleCase=True)

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


class WifiInfo(providers.Value[_JSONDict], network_typing.WifiInfo):
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

    __get_value__: providers.FactoryValue[JSON]

    @property
    def ssid(self):
        if value := self.__get_value__():
            return value.get(self.Keys.ssid, "")
        return ""

    @property
    def password(self):
        if value := self.__get_value__():
            return value.get(self.Keys.password, "")
        return ""
