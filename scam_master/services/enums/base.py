from enum import Enum


class StrEnum(str, Enum):
    @classmethod
    def _missing_(cls, value):
        value = value.upper()
        for member in cls:
            if member.upper() == value:
                return member
        return None
