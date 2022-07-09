from enum import Enum

from pydantic import ConstrainedStr, conlist

_MIN_STRING_LENGTH = 1
_MAX_STRING_LENGTH = 300
_MAX_LIST_LENGTH = 10


class NotEmptyString(ConstrainedStr):
    strip_whitespace = True
    min_length = _MIN_STRING_LENGTH
    max_length = _MAX_STRING_LENGTH
    strict = True


ListOfStrings = conlist(
    item_type=NotEmptyString,
    max_items=_MAX_LIST_LENGTH,
    unique_items=True,
)

NotEmptyListOfStrings = conlist(
    item_type=NotEmptyString,
    min_items=1,
    max_items=_MAX_LIST_LENGTH,
    unique_items=True,
)


class TypeEnum(str, Enum):
    ONE = "ONE"
    MANY = "MANY"
    ORDER = "ORDER"
    MATCH = "MATCH"
