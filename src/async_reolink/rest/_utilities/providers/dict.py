"""Dict Provider"""

from typing import Callable, TypeVar, overload
from .value import Value, ProvidedValue, T, FactoryValue

from ..missing import MISSING

K = TypeVar("K")

ProvidedDict = ProvidedValue[dict[K, T]]

V = TypeVar("V")


class Dict(Value[dict[K, T]]):
    """dict Provider"""

    @overload
    @staticmethod
    def _get_key_value(
        factory: FactoryValue[dict[K, T]],
        key: K,
        create=False,
    ) -> T:
        ...

    @overload
    @staticmethod
    def _get_key_value(
        factory: FactoryValue[dict[K, T]], key: K, create=False, /, default=Callable[[], V] | V
    ) -> T | V:
        ...

    @staticmethod
    def _get_key_value(
        factory: FactoryValue[dict[K, T]],
        key: K,
        create=False,
        /,
        default: Callable[[], V] | V = MISSING,
    ):
        if (_dict := factory(create)) is None:
            if callable(default):
                return default()
            if default is MISSING:
                raise KeyError()
            return default
        try:
            value = _dict[key]
        except KeyError:
            if callable(default):
                value = default()
            elif default is MISSING:
                raise
            else:
                value = default
            if create:
                _dict[key] = value
        return value
