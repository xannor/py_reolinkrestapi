"""Mangled key dictionary"""

from typing import Final, TypeVar, TypedDict, Mapping
from typing_extensions import LiteralString

from .value import Value, _V, FactoryValue

LS = TypeVar("LS", bound=LiteralString)


class mangler_kwargs(TypedDict, total=False):
    """mangler keyword args"""

    prefix: str
    suffix: str
    titleCase: bool


mangler_kwkeys: Final = ("prefix", "suffix", "titleCase")


def mangler(prefix: str = None, suffix: str = None, titleCase=False):
    def mangle(value: LS) -> LS:
        if prefix:
            if not value:
                value = prefix
            elif titleCase:
                value = prefix + value.title()
            else:
                value = prefix + value
        if suffix:
            if not value:
                return suffix
            return value + suffix
        return value

    return mangle


class Mangler:
    """String Mangler"""

    class KwArgs(TypedDict, total=False):
        """Keyword Args"""

        prefix: str
        suffix: str
        titleCase: bool

    __slots__ = ("__prefix", "__suffix", "__titleCase")


class Mangled(Value[Mapping[str, _V]]):
    """Manged key ditionary"""

    class KwArgs(TypedDict, total=False):
        """Keyword Args"""

        prefix: str
        suffix: str
        titleCase: bool

    __slots__ = ("__prefix", "__suffix", "__titleCase")

    def __init__(
        self,
        get_value: FactoryValue[dict[str, _V]],
        /,
        prefix: str = None,
        suffix: str = None,
        titleCase=False,
        **kwargs: any,
    ) -> None:
        super().__init__(get_value, **kwargs)
        self.__prefix = prefix
        self.__suffix = suffix
        self.__titleCase = titleCase

    def _mangle_key(self, key: LS) -> LS:
        if not self.__prefix and not self.__suffix:
            return key
        _new = key
        if self.__prefix:
            if self.__titleCase:
                _new = self.__prefix + key.title()
            else:
                _new = self.__prefix + key
        if self.__suffix:
            _new += self.__suffix
        return _new
