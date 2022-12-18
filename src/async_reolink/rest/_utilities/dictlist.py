"""List as a Dictionary"""

from typing import Callable, Generator, Mapping, TypeVar, overload
from typing_extensions import LiteralString

from .providers.value import Value, ProvidedValue, FactoryValue
from .missing import MISSING

_KT = TypeVar("_KT")
_VT = TypeVar("_VT")

V = TypeVar("V")


class DictList(Value[list[dict[str, any]]], Mapping[_KT, _VT]):
    """list as a Dictionary"""

    __slots__ = ("__key", "__type")

    def __init__(
        self,
        key: str,
        value: ProvidedValue[list[dict[str, any]]] | None,
        __type: Callable[[FactoryValue[dict]], _VT],
    ) -> None:
        super().__init__(value)
        self.__key = key
        self.__type = __type

    def _get_item(self, __k: _KT) -> dict:
        return (
            next(
                (_d for _d in value if isinstance(_d, dict) and _d.get(self.__key, None) == __k),
                None,
            )
            if (value := self._get_value()) is not None
            else None
        )

    def __getitem__(self, __k: _KT):
        return self.__type(
            lambda create: self._find_key_value(
                self._get_provided_value, self.__key, __k, default=None
            )
        )

    def __iter__(self) -> Generator[int, None, None]:
        if not (value := self._provided_value):
            return
        for _d in value:
            if _d.get(self.__key, MISSING):
                yield self.__type(_d)

    def __contains__(self, __o: _KT):
        return (
            self._find_key_value(self._get_provided_value, self.__key, __o, default=None)
            is not None
        )

    def __len__(self) -> int:
        if value := self._provided_value:
            return value.__len__()
        return 0

    @staticmethod
    def _find_key_value(
        factory: FactoryValue[list[dict[str, any]]],
        key: str,
        value: _KT,
        create=False,
        /,
        default: Callable[[], V] | V = MISSING,
    ) -> dict[str, any]:
        if (_list := factory(create)) is None:
            if callable(default):
                return default()
            elif default is MISSING:
                raise KeyError()
            return default
        for _value in _list:
            if _value and _value.get(key, MISSING) == value:
                break
        else:
            if callable(default):
                _value = default()
            elif default is MISSING:
                raise KeyError()
            else:
                _value = default
            if create:
                _list.append(_value)
        return _value
