"""Value provider"""

from typing import Callable, Generic, Protocol, TypeVar

from ..missing import MISSING

T = TypeVar("T")


class FactoryValue(Generic[T], Protocol):
    """Factory Value"""

    def __call__(self, create=False) -> T:
        ...


ProvidedValue = FactoryValue[T] | T


class Value(Generic[T]):
    """Value Provider"""

    __slots__ = ("__factory",)

    def __init__(self, value: ProvidedValue[T] = MISSING) -> None:
        super().__init__()
        self._set_provided_value(value)

    @property
    def _provided_value(self):
        return self._get_provided_value()

    def _get_provided_value(self, create=False):
        if (value := self.__factory(create)) is MISSING:
            raise ValueError()
        return value

    def _set_provided_value(self, value: ProvidedValue[T] = MISSING):
        if not callable(value):
            _value = value

            def factory(*_) -> T:
                return _value

            value = factory

        self.__factory: FactoryValue[T] = value

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}:{repr(self.__factory())}>"
