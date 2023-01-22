"""Encoding REST models"""

from typing import Callable, Final, Mapping, Protocol, TypeAlias, TypedDict
from async_reolink.api.typing import StreamTypes
from async_reolink.api.encoding import typing as encoding_typing

from .._utilities.providers import value as providers

from .. import model

from ..encoding.typing import stream_types_str

# pylint:disable=missing-function-docstring

_JSONDict: TypeAlias = dict[str, any]


class StreamEncodingInfo(providers.Value[_JSONDict], encoding_typing.StreamEncodingInfo):
    """REST Stream Encoding Info"""

    class JSON(TypedDict):
        """JSON"""

        bitRate: int
        frameRate: int
        gop: int
        height: int
        width: int
        profile: str
        size: str
        video_type: str

    class Keys(Protocol):
        """Keys"""

        bit_rate: Final = "bitRate"
        frame_rate: Final = "frameRate"
        gop: Final = "gop"
        height: Final = "height"
        width: Final = "width"
        profile: Final = "profile"
        size: Final = "size"
        video_type: Final = "video_type"

    __get_value__: providers.FactoryValue[JSON]

    @property
    def bit_rate(self):
        if value := self.__get_value__():
            return value.get(self.Keys.bit_rate, 0)
        return 0

    @property
    def frame_rate(self):
        if value := self.__get_value__():
            return value.get(self.Keys.frame_rate, 0)
        return 0

    @property
    def gop(self):
        if value := self.__get_value__():
            return value.get(self.Keys.gop, 0)
        return 0

    @property
    def height(self):
        if value := self.__get_value__():
            return value.get(self.Keys.height, 0)
        return 0

    @property
    def width(self):
        if value := self.__get_value__():
            return value.get(self.Keys.width, 0)
        return 0

    @property
    def profile(self):
        if value := self.__get_value__():
            return value.get(self.Keys.profile, "")
        return ""

    @property
    def size(self):
        if value := self.__get_value__():
            return value.get(self.Keys.size, "")
        return ""

    @property
    def video_type(self):
        if value := self.__get_value__():
            return value.get(self.Keys.video_type, "")
        return ""


class _StreamMapping(providers.Value[_JSONDict], Mapping[StreamTypes, StreamEncodingInfo]):
    __slots__ = ()

    def __getitem__(self, __k: StreamTypes):
        return StreamEncodingInfo(self.lookup_factory(self.__get_value__, stream_types_str(__k)))

    def __iter__(self):
        if not (__value := self.__get_value__()):
            return

        for __k in StreamTypes:
            if stream_types_str(__k) in __value:
                yield __k

    def __len__(self):
        if __value := self.__get_value__():
            return len(stream_types_str() & __value.keys())
        return 0


class EncodingInfo(providers.Value[_JSONDict], encoding_typing.EncodingInfo):
    """REST Encoding Info"""

    class JSON(TypedDict):
        """JSON"""

        audio: int

    class Keys(Protocol):
        """Keys"""

        audio: Final = "audio"

    __get_value__: providers.FactoryValue[JSON]

    @property
    def audio(self):
        return True if (value := self.__get_value__()) and value.get(self.Keys.audio, 0) else False

    @property
    def stream(self):
        """stream"""

        return _StreamMapping(self.__get_value__)
