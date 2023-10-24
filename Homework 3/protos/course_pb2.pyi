from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class CourseRequest(_message.Message):
    __slots__ = ["course_id"]
    COURSE_ID_FIELD_NUMBER: _ClassVar[int]
    course_id: int
    def __init__(self, course_id: _Optional[int] = ...) -> None: ...

class CourseFilterRequest(_message.Message):
    __slots__ = ["implementer", "role", "search"]
    IMPLEMENTER_FIELD_NUMBER: _ClassVar[int]
    ROLE_FIELD_NUMBER: _ClassVar[int]
    SEARCH_FIELD_NUMBER: _ClassVar[int]
    implementer: str
    role: str
    search: str
    def __init__(self, implementer: _Optional[str] = ..., role: _Optional[str] = ..., search: _Optional[str] = ...) -> None: ...

class Lesson(_message.Message):
    __slots__ = ["number", "day_of_week", "string_day", "string_time_interval"]
    NUMBER_FIELD_NUMBER: _ClassVar[int]
    DAY_OF_WEEK_FIELD_NUMBER: _ClassVar[int]
    STRING_DAY_FIELD_NUMBER: _ClassVar[int]
    STRING_TIME_INTERVAL_FIELD_NUMBER: _ClassVar[int]
    number: int
    day_of_week: str
    string_day: str
    string_time_interval: str
    def __init__(self, number: _Optional[int] = ..., day_of_week: _Optional[str] = ..., string_day: _Optional[str] = ..., string_time_interval: _Optional[str] = ...) -> None: ...

class CourseFullResponse(_message.Message):
    __slots__ = ["id", "name", "description", "is_prerecorded_course", "implementer", "roles", "lessons"]
    ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    IS_PRERECORDED_COURSE_FIELD_NUMBER: _ClassVar[int]
    IMPLEMENTER_FIELD_NUMBER: _ClassVar[int]
    ROLES_FIELD_NUMBER: _ClassVar[int]
    LESSONS_FIELD_NUMBER: _ClassVar[int]
    id: int
    name: str
    description: str
    is_prerecorded_course: bool
    implementer: str
    roles: _containers.RepeatedScalarFieldContainer[str]
    lessons: _containers.RepeatedCompositeFieldContainer[Lesson]
    def __init__(self, id: _Optional[int] = ..., name: _Optional[str] = ..., description: _Optional[str] = ..., is_prerecorded_course: bool = ..., implementer: _Optional[str] = ..., roles: _Optional[_Iterable[str]] = ..., lessons: _Optional[_Iterable[_Union[Lesson, _Mapping]]] = ...) -> None: ...

class CourseShort(_message.Message):
    __slots__ = ["id", "name", "is_prerecorded_course"]
    ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    IS_PRERECORDED_COURSE_FIELD_NUMBER: _ClassVar[int]
    id: int
    name: str
    is_prerecorded_course: bool
    def __init__(self, id: _Optional[int] = ..., name: _Optional[str] = ..., is_prerecorded_course: bool = ...) -> None: ...

class CourseListResponse(_message.Message):
    __slots__ = ["courses"]
    COURSES_FIELD_NUMBER: _ClassVar[int]
    courses: _containers.RepeatedCompositeFieldContainer[CourseShort]
    def __init__(self, courses: _Optional[_Iterable[_Union[CourseShort, _Mapping]]] = ...) -> None: ...

class CourseExistsResponse(_message.Message):
    __slots__ = ["exists"]
    EXISTS_FIELD_NUMBER: _ClassVar[int]
    exists: bool
    def __init__(self, exists: bool = ...) -> None: ...
