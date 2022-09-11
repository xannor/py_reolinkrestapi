"""Simple Value Factory Protocol"""

from typing import (
    TYPE_CHECKING,
    Callable,
    Final,
    Generic,
    Protocol,
    TypeVar,
    cast,
    overload,
    runtime_checkable,
)


_T = TypeVar("_T")

# pylint: disable=too-few-public-methods


class _Empty:
    pass


NO_RESULT: Final = _Empty()


class ValueFactoryCall(Protocol[_T]):
    """Simple Value Factory"""

    def __call__(self, can_create: bool = False) -> _T:
        ...


@runtime_checkable
class SupportsLazyFactory(Protocol[_T]):
    """Supports __lazy_factory__"""

    def __lazy_factory__(self, can_create: bool = False) -> _T:
        ...


class LazyValue(SupportsLazyFactory[_T]):
    """Base Lazy value Provider"""

    __slots__ = ("__lazy_factory__",)

    @overload
    def __init__(self, factory: ValueFactoryCall[_T]) -> None:
        ...

    @overload
    def __init__(self, value: _T) -> None:
        ...

    def __init__(self, factory) -> None:
        if not callable(factory):
            value: _T = factory

            def _get(*_):
                return value

            factory = _get

        if TYPE_CHECKING:
            factory = cast(ValueFactoryCall[_T], factory)

        self.__lazy_factory__ = factory


class LazyProperty(Generic[_T]):
    """Lazy property factory"""

    __slots__ = ("factory", "_get_factory")

    def __init__(self, factory: Callable[[ValueFactoryCall], _T]) -> None:
        self.factory = factory
        self._get_factory = self.__get_factory

    def __get_factory(self, obj: SupportsLazyFactory, __type: type = None):
        return obj.__lazy_factory__

    @overload
    def __get__(self, obj: None, _type: type) -> "LazyProperty[_T]":
        ...

    @overload
    def __get__(self, obj: SupportsLazyFactory, _type: type) -> _T:
        ...

    def __get__(self, obj: SupportsLazyFactory, _type=None):
        if obj is None:
            return self
        return self.factory(self._get_factory)

    def __set__(self, obj, value: _T):
        raise AttributeError()

    def __delete__(self, obj):
        raise AttributeError()


def lazy(factory: Callable[[ValueFactoryCall], _T]):
    """Property descriptor for lazy values"""
    return LazyProperty(factory)


class UpdatableLazyValue(LazyValue[_T]):
    """Updateable Lazy value Provider"""

    __slots__ = ()

    @overload
    def update(self, factory: ValueFactoryCall[_T]) -> None:
        ...

    @overload
    def update(self, value: _T) -> None:
        ...

    def update(self, factory):
        """update"""
        if not callable(factory):
            value = factory

            def _get():
                return value

            factory = _get
        self.__lazy_factory__ = factory
