"""Value provider"""

from typing import (
    Callable,
    Final,
    Generic,
    Mapping,
    MutableMapping,
    MutableSequence,
    Protocol,
    Sequence,
    overload,
)
from typing_extensions import TypeVar, Self

_T = TypeVar("_T", infer_variance=True)
_K = TypeVar("_K", infer_variance=True)
_V = TypeVar("_V", infer_variance=True)
_R = TypeVar("_R", infer_variance=True)

_VALUE_MISSING: Final = ...


class FactoryValue(Generic[_T], Protocol):
    """Factory Value"""

    def __call__(self, create=False) -> _T:
        ...

    def __get__(self, obj: any, type: type = None) -> Self:
        ...


class Value(Generic[_T]):
    """Value Provider"""

    # __get_value__: FactoryValue[T]

    __slots__ = ("__factory", "__value")

    def __init__(self, value: FactoryValue[_T] | _T | None = ..., /, **kwargs: any) -> None:
        super().__init__(**kwargs)
        self.__set_value__(value)

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}:{repr(self.__get_value__())}>"

    def __default_factory__(self, create=False):
        if self is not None and not isinstance(self, type):
            self.__set_value__(None)
        return None

    def __set_value__(self, value: _T | FactoryValue[_T] | None):
        if value is ...:
            value = self.__default_factory__
        if callable(value):
            self.__factory = value
            self.__value: _T = ...
        else:
            self.__factory = None
            self.__value = value

    def __get_value__(self, create=False) -> _T:
        if self.__value is not ...:
            return self.__value
        return self.__factory(create)

    @staticmethod
    def create_factory(
        value: _T = _VALUE_MISSING, default_factory: Callable[[], _T] = None
    ) -> FactoryValue[_T]:
        if value is not _VALUE_MISSING and not default_factory:

            def echo_value(_create=False):
                return value

            return echo_value

        if not default_factory:

            def no_factory(_create=False):
                if value is _VALUE_MISSING:
                    return None
                return value

            return no_factory

        def factory(create=False):
            nonlocal value
            if value is _VALUE_MISSING:
                if create:
                    value = default_factory()
                else:
                    return None
            return value

        return factory

    @overload
    @staticmethod
    def lookup_value(source: FactoryValue[Mapping[_K, _V]], key: _K, /, create=False) -> _V:
        ...

    @overload
    @staticmethod
    def lookup_value(
        source: FactoryValue[Mapping[_K, _V]], key: _K, /, default: _R, create=False
    ) -> _V | _R:
        ...

    @overload
    @staticmethod
    def lookup_value(
        source: FactoryValue[Sequence[_V]],
        key: int,
        /,
        default_factory: Callable[[], _R],
        create=False,
    ) -> _V | _R:
        ...

    @overload
    @staticmethod
    def lookup_value(source: FactoryValue[Sequence[_V]], key: int, /, create=False) -> _V:
        ...

    @overload
    @staticmethod
    def lookup_value(
        source: FactoryValue[Sequence[_V]], key: int, /, default: _R, create=False
    ) -> _V | _R:
        ...

    @overload
    @staticmethod
    def lookup_value(
        source: FactoryValue[Sequence[_V]],
        key: int,
        /,
        default_factory: Callable[[], _R],
        create=False,
    ) -> _V | _R:
        ...

    @staticmethod
    def lookup_value(
        source: FactoryValue[Mapping | Sequence],
        key: any,
        /,
        create=False,
        default: any = _VALUE_MISSING,
        default_factory: Callable[[], any] = None,
    ):
        if default is not _VALUE_MISSING and default_factory:
            raise ValueError(
                "Cannot provide both a default value and default value factory arguments"
            )

        if (container := source(create)) is not None and container is not _VALUE_MISSING:
            try:
                value = container[key]
            except (IndexError, KeyError):
                value: any = _VALUE_MISSING
        else:
            value = _VALUE_MISSING
        if value is _VALUE_MISSING:
            if default_factory:
                value = default_factory()
            elif default is _VALUE_MISSING:
                if isinstance(container, Sequence):
                    raise IndexError()
                else:
                    raise KeyError()
            else:
                value = default
            if create and isinstance(container, (MutableMapping, MutableSequence)):
                container[key] = value
        return value

    @overload
    @classmethod
    def lookup_factory(cls, source: FactoryValue[Mapping[_K, _V]], key: _K) -> FactoryValue[_V]:
        ...

    @overload
    @classmethod
    def lookup_factory(
        cls, source: FactoryValue[Mapping[_K, _V]], key: _K, /, default: _R
    ) -> FactoryValue[_V | _R]:
        ...

    @overload
    @classmethod
    def lookup_factory(
        cls,
        source: FactoryValue[Sequence[_V]],
        key: int,
        /,
        default_factory: FactoryValue[_R],
    ) -> FactoryValue[_V | _R]:
        ...

    @overload
    @classmethod
    def lookup_factory(cls, source: FactoryValue[Sequence[_V]], key: int) -> FactoryValue[_V]:
        ...

    @overload
    @classmethod
    def lookup_factory(
        cls, source: FactoryValue[Sequence[_V]], key: int, /, default: _R
    ) -> FactoryValue[_V | _R]:
        ...

    @overload
    @classmethod
    def lookup_factory(
        cls,
        source: FactoryValue[Sequence[_V]],
        key: int,
        /,
        default_factory: FactoryValue[_R],
    ) -> FactoryValue[_V | _R]:
        ...

    @classmethod
    def lookup_factory(
        cls,
        source: FactoryValue[Mapping | Sequence],
        key: any,
        /,
        default: any = _VALUE_MISSING,
        default_factory: FactoryValue[any] = None,
    ):
        def factory(create=False):
            if default_factory:
                _default_factory: Callable[[], any] = lambda: default_factory(create)
            else:
                _default_factory = None
            return cls.lookup_value(
                source, key, create=create, default=default, default_factory=_default_factory
            )

        return factory
