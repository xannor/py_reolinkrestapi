"""3.11 StrEnum"""

from enum import Enum


class ReprEnum(Enum):
    """Only changes the repr(), leaving str() and format() to the mixed-in type."""


class StrEnum(str, ReprEnum):
    """Enum where members are also (and must be) strs"""

    def __new__(cls, *values):
        # not doing the validation of the str args, str should do that
        value = str(*values)
        member = str.__new__(cls, value)
        member._value_ = value
        return member

    # pylint: disable=no-self-argument
    def _generate_next_value_(name, start, count, last_values):
        """
        Return the lower-cased version of the member name.
        """
        return name.lower()
