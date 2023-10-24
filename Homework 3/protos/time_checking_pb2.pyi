from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Course(_message.Message):
    __slots__ = ["id"]
    ID_FIELD_NUMBER: _ClassVar[int]
    id: int
    def __init__(self, id: _Optional[int] = ...) -> None: ...

class CheckTimeRequest(_message.Message):
    __slots__ = ["courses"]
    COURSES_FIELD_NUMBER: _ClassVar[int]
    courses: _containers.RepeatedCompositeFieldContainer[Course]
    def __init__(self, courses: _Optional[_Iterable[_Union[Course, _Mapping]]] = ...) -> None: ...

class CheckTimeResponse(_message.Message):
    __slots__ = ["is_successful"]
    IS_SUCCESSFUL_FIELD_NUMBER: _ClassVar[int]
    is_successful: bool
    def __init__(self, is_successful: bool = ...) -> None: ...
