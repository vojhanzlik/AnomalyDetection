from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class AnomalyDetRequest(_message.Message):
    __slots__ = ("id", "sensor1", "sensor2", "sensor3", "sensor4", "sensor5", "sensor6")
    ID_FIELD_NUMBER: _ClassVar[int]
    SENSOR1_FIELD_NUMBER: _ClassVar[int]
    SENSOR2_FIELD_NUMBER: _ClassVar[int]
    SENSOR3_FIELD_NUMBER: _ClassVar[int]
    SENSOR4_FIELD_NUMBER: _ClassVar[int]
    SENSOR5_FIELD_NUMBER: _ClassVar[int]
    SENSOR6_FIELD_NUMBER: _ClassVar[int]
    id: int
    sensor1: float
    sensor2: float
    sensor3: float
    sensor4: float
    sensor5: float
    sensor6: float
    def __init__(self, id: _Optional[int] = ..., sensor1: _Optional[float] = ..., sensor2: _Optional[float] = ..., sensor3: _Optional[float] = ..., sensor4: _Optional[float] = ..., sensor5: _Optional[float] = ..., sensor6: _Optional[float] = ...) -> None: ...

class AnomalyDetResponse(_message.Message):
    __slots__ = ("id", "result")
    ID_FIELD_NUMBER: _ClassVar[int]
    RESULT_FIELD_NUMBER: _ClassVar[int]
    id: int
    result: bool
    def __init__(self, id: _Optional[int] = ..., result: bool = ...) -> None: ...

class NumpyArray(_message.Message):
    __slots__ = ("values", "rows", "cols")
    VALUES_FIELD_NUMBER: _ClassVar[int]
    ROWS_FIELD_NUMBER: _ClassVar[int]
    COLS_FIELD_NUMBER: _ClassVar[int]
    values: _containers.RepeatedScalarFieldContainer[float]
    rows: int
    cols: int
    def __init__(self, values: _Optional[_Iterable[float]] = ..., rows: _Optional[int] = ..., cols: _Optional[int] = ...) -> None: ...

class Response(_message.Message):
    __slots__ = ("message",)
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    message: str
    def __init__(self, message: _Optional[str] = ...) -> None: ...
