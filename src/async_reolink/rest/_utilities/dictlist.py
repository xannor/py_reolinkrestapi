"""List as a Dictionary"""

from typing import TYPE_CHECKING, Callable, Final, Generator, Mapping, TypeVar, overload
from typing_extensions import LiteralString

from .providers.value import Value, FactoryValue, FactoryValue

_KT = TypeVar("_KT")
_VT = TypeVar("_VT")

V = TypeVar("V")

_VALUE_MISSING: Final = ...


class DictList(Value[list[dict[str, any]]], Mapping[_KT, _VT]):
    """list as a Dictionary"""

    __slots__ = ("__key", "__type")

    def __init__(
        self,
        key: str,
        value: FactoryValue[list[dict[str, any]]] | list[dict[str, any]] | None,
        __type: Callable[[FactoryValue[dict[str, any]]], _VT],
        /,
        **kwargs: any,
    ) -> None:
        super().__init__(value, **kwargs)
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
            self.lookup_key_factory(self.__get_value__, self.__key, __k, default=None)
        )

    def __iter__(self) -> Generator[_KT, None, None]:
        if not (value := self.__get_value__()):
            return
        seen = set()
        for _d in value:
            if isinstance(_d, dict) and (_kv := _d.get(self.__key)) is not None and _kv not in seen:
                seen.add(_kv)
                yield _kv

    def __contains__(self, __o: _KT):
        return self.lookup_key_value(self.__get_value__, self.__key, __o, default=None) is not None

    def __len__(self) -> int:
        if not (value := self.__get_value__()):
            return 0
        return value.__len__()

    @staticmethod
    def lookup_key_value(
        source: FactoryValue[list[dict[str, any]]],
        key: str,
        key_value: _KT,
        /,
        create=False,
        default: any = _VALUE_MISSING,
        default_factory: FactoryValue[any] = None,
    ) -> dict[str, any]:
        if (_list := source(create)) is not None and _list is not _VALUE_MISSING:
            for _value in _list:
                if isinstance(_value, Mapping) and _value.get(key, _VALUE_MISSING) == key_value:
                    break
            else:
                _value: any = _VALUE_MISSING
        else:
            _value = _VALUE_MISSING
        if _value is _VALUE_MISSING:
            if default_factory:
                _value = default_factory(create)
            elif default is _VALUE_MISSING:
                raise KeyError()
            else:
                _value = default
            if create:
                _list.append(_value)
        return _value

    @classmethod
    def lookup_key_factory(
        cls,
        source: FactoryValue[list[dict[str, any]]],
        key: str,
        key_value: _KT,
        /,
        default: any = _VALUE_MISSING,
        default_factory: FactoryValue[any] = None,
    ):
        def factory(create=False):
            return cls.lookup_key_value(
                source, key, key_value, default=default, default_factory=default_factory
            )

        return factory
