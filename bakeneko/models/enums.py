from enum import Enum


class TypeEnumDB(str, Enum):
    ONE = "ONE"
    MANY = "MANY"
    ORDER = "ORDER"
    MATCH = "MATCH"


class TypeEnum(str, Enum):
    ONE = "Выберите один правильный вариант"
    MANY = "Выберите все правильные варианты"
    ORDER = "Перетащите варианты так, чтобы они оказались в правильном порядке"
    MATCH = "Соедините соответствия справа с правильными вариантами"


class StoreType(str, Enum):
    SQLStore = "SQLStore"
