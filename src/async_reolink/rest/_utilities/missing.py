"""Missing"""


class _Missing:
    def __bool__(self):
        return False

    def __int__(self):
        return 0

    def __index__(self):
        return 0

    def __str__(self):
        return ""

    def __repr__(self):
        return "<MISSING>"


MISSING = _Missing()
