from enum import Enum
from enum import unique

@unique
class DataType(Enum):
    VARCHAR = 1
    CHAR = 2
    DATE = 3
    INTEGER = 4
    SMALLINT = 5
    BIGINT = 6
    DECIMAL = 7
    NUMERIC = 8
    FLOAT = 9
    TIMESTAMP = 10
    TIME = 11
    BYTEINT = 12