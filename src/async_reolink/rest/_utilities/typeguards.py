"""filter typeguards"""

from typing import Optional, TypeGuard, TypeVar


_T = TypeVar("_T")


def is_not_None(value: Optional[_T]) -> TypeGuard[_T]:
    return value is not None
