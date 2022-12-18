from typing import Callable, TypeVar, overload
from .value import Value, ProvidedValue, T, FactoryValue
from ..missing import MISSING

ProvidedList = ProvidedValue[list[T]]

V = TypeVar("V")


class List(Value[list[T]]):
    @overload
    @staticmethod
    def _get_index_value(
        factory: FactoryValue[list[T]],
        index: int,
        create=False,
    ) -> T:
        ...

    @overload
    @staticmethod
    def _get_index_value(
        factory: FactoryValue[list[T]], index: int, create=False, /, default=Callable[[], V] | V
    ) -> T | V:
        ...

    @staticmethod
    def _get_index_value(
        factory: FactoryValue[list],
        index: int,
        create=False,
        /,
        default: Callable[[], V] | V = MISSING,
    ):
        if (_list := factory(create)) is None:
            if callable(default):
                return default()
            if default is MISSING:
                raise IndexError()
            return default
        try:
            value = _list[index]
        except IndexError:
            if callable(default):
                value = default()
            elif default is MISSING:
                raise
            else:
                value = default
            if create:
                _list[index] = value
        return value
