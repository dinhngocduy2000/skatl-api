from enum import Enum


class OrderDirection(Enum):
    ASC = "asc"
    DESC = "desc"

    @classmethod
    def from_str(cls, status: str) -> "OrderDirection":
        return cls[status.upper()]
    