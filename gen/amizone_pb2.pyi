from google.api import annotations_pb2 as _annotations_pb2
from google.protobuf import timestamp_pb2 as _timestamp_pb2
from google.type import date_pb2 as _date_pb2
from protoc_gen_openapiv2.options import annotations_pb2 as _annotations_pb2_1
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class AttendanceState(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []
    PENDING: _ClassVar[AttendanceState]
    PRESENT: _ClassVar[AttendanceState]
    ABSENT: _ClassVar[AttendanceState]
    NA: _ClassVar[AttendanceState]
    INVALID: _ClassVar[AttendanceState]
PENDING: AttendanceState
PRESENT: AttendanceState
ABSENT: AttendanceState
NA: AttendanceState
INVALID: AttendanceState

class EmptyMessage(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class ClassScheduleRequest(_message.Message):
    __slots__ = ["date"]
    DATE_FIELD_NUMBER: _ClassVar[int]
    date: _date_pb2.Date
    def __init__(self, date: _Optional[_Union[_date_pb2.Date, _Mapping]] = ...) -> None: ...

class CourseRef(_message.Message):
    __slots__ = ["code", "name"]
    CODE_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    code: str
    name: str
    def __init__(self, code: _Optional[str] = ..., name: _Optional[str] = ...) -> None: ...

class SemesterRef(_message.Message):
    __slots__ = ["semester_ref"]
    SEMESTER_REF_FIELD_NUMBER: _ClassVar[int]
    semester_ref: str
    def __init__(self, semester_ref: _Optional[str] = ...) -> None: ...

class Attendance(_message.Message):
    __slots__ = ["attended", "held"]
    ATTENDED_FIELD_NUMBER: _ClassVar[int]
    HELD_FIELD_NUMBER: _ClassVar[int]
    attended: int
    held: int
    def __init__(self, attended: _Optional[int] = ..., held: _Optional[int] = ...) -> None: ...

class Marks(_message.Message):
    __slots__ = ["have", "max"]
    HAVE_FIELD_NUMBER: _ClassVar[int]
    MAX_FIELD_NUMBER: _ClassVar[int]
    have: float
    max: float
    def __init__(self, have: _Optional[float] = ..., max: _Optional[float] = ...) -> None: ...

class Course(_message.Message):
    __slots__ = ["ref", "type", "attendance", "internal_marks", "syllabus_doc"]
    REF_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    ATTENDANCE_FIELD_NUMBER: _ClassVar[int]
    INTERNAL_MARKS_FIELD_NUMBER: _ClassVar[int]
    SYLLABUS_DOC_FIELD_NUMBER: _ClassVar[int]
    ref: CourseRef
    type: str
    attendance: Attendance
    internal_marks: Marks
    syllabus_doc: str
    def __init__(self, ref: _Optional[_Union[CourseRef, _Mapping]] = ..., type: _Optional[str] = ..., attendance: _Optional[_Union[Attendance, _Mapping]] = ..., internal_marks: _Optional[_Union[Marks, _Mapping]] = ..., syllabus_doc: _Optional[str] = ...) -> None: ...

class Courses(_message.Message):
    __slots__ = ["courses"]
    COURSES_FIELD_NUMBER: _ClassVar[int]
    courses: _containers.RepeatedCompositeFieldContainer[Course]
    def __init__(self, courses: _Optional[_Iterable[_Union[Course, _Mapping]]] = ...) -> None: ...

class AttendanceRecord(_message.Message):
    __slots__ = ["attendance", "course"]
    ATTENDANCE_FIELD_NUMBER: _ClassVar[int]
    COURSE_FIELD_NUMBER: _ClassVar[int]
    attendance: Attendance
    course: CourseRef
    def __init__(self, attendance: _Optional[_Union[Attendance, _Mapping]] = ..., course: _Optional[_Union[CourseRef, _Mapping]] = ...) -> None: ...

class AttendanceRecords(_message.Message):
    __slots__ = ["records"]
    RECORDS_FIELD_NUMBER: _ClassVar[int]
    records: _containers.RepeatedCompositeFieldContainer[AttendanceRecord]
    def __init__(self, records: _Optional[_Iterable[_Union[AttendanceRecord, _Mapping]]] = ...) -> None: ...

class ScheduledClass(_message.Message):
    __slots__ = ["course", "start_time", "end_time", "faculty", "room", "attendance"]
    COURSE_FIELD_NUMBER: _ClassVar[int]
    START_TIME_FIELD_NUMBER: _ClassVar[int]
    END_TIME_FIELD_NUMBER: _ClassVar[int]
    FACULTY_FIELD_NUMBER: _ClassVar[int]
    ROOM_FIELD_NUMBER: _ClassVar[int]
    ATTENDANCE_FIELD_NUMBER: _ClassVar[int]
    course: CourseRef
    start_time: _timestamp_pb2.Timestamp
    end_time: _timestamp_pb2.Timestamp
    faculty: str
    room: str
    attendance: AttendanceState
    def __init__(self, course: _Optional[_Union[CourseRef, _Mapping]] = ..., start_time: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., end_time: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., faculty: _Optional[str] = ..., room: _Optional[str] = ..., attendance: _Optional[_Union[AttendanceState, str]] = ...) -> None: ...

class ScheduledClasses(_message.Message):
    __slots__ = ["classes"]
    CLASSES_FIELD_NUMBER: _ClassVar[int]
    classes: _containers.RepeatedCompositeFieldContainer[ScheduledClass]
    def __init__(self, classes: _Optional[_Iterable[_Union[ScheduledClass, _Mapping]]] = ...) -> None: ...

class AmizoneDiaryEvent(_message.Message):
    __slots__ = ["type", "course_code", "course_name", "faculty", "room", "start", "end"]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    COURSE_CODE_FIELD_NUMBER: _ClassVar[int]
    COURSE_NAME_FIELD_NUMBER: _ClassVar[int]
    FACULTY_FIELD_NUMBER: _ClassVar[int]
    ROOM_FIELD_NUMBER: _ClassVar[int]
    START_FIELD_NUMBER: _ClassVar[int]
    END_FIELD_NUMBER: _ClassVar[int]
    type: str
    course_code: str
    course_name: str
    faculty: str
    room: str
    start: str
    end: str
    def __init__(self, type: _Optional[str] = ..., course_code: _Optional[str] = ..., course_name: _Optional[str] = ..., faculty: _Optional[str] = ..., room: _Optional[str] = ..., start: _Optional[str] = ..., end: _Optional[str] = ...) -> None: ...

class ScheduledExam(_message.Message):
    __slots__ = ["course", "time", "mode"]
    COURSE_FIELD_NUMBER: _ClassVar[int]
    TIME_FIELD_NUMBER: _ClassVar[int]
    MODE_FIELD_NUMBER: _ClassVar[int]
    course: CourseRef
    time: _timestamp_pb2.Timestamp
    mode: str
    def __init__(self, course: _Optional[_Union[CourseRef, _Mapping]] = ..., time: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., mode: _Optional[str] = ...) -> None: ...

class ExaminationSchedule(_message.Message):
    __slots__ = ["title", "exams"]
    TITLE_FIELD_NUMBER: _ClassVar[int]
    EXAMS_FIELD_NUMBER: _ClassVar[int]
    title: str
    exams: _containers.RepeatedCompositeFieldContainer[ScheduledExam]
    def __init__(self, title: _Optional[str] = ..., exams: _Optional[_Iterable[_Union[ScheduledExam, _Mapping]]] = ...) -> None: ...

class Profile(_message.Message):
    __slots__ = ["name", "enrollment_number", "enrollment_validity", "batch", "program", "date_of_birth", "blood_group", "id_card_number", "uuid"]
    NAME_FIELD_NUMBER: _ClassVar[int]
    ENROLLMENT_NUMBER_FIELD_NUMBER: _ClassVar[int]
    ENROLLMENT_VALIDITY_FIELD_NUMBER: _ClassVar[int]
    BATCH_FIELD_NUMBER: _ClassVar[int]
    PROGRAM_FIELD_NUMBER: _ClassVar[int]
    DATE_OF_BIRTH_FIELD_NUMBER: _ClassVar[int]
    BLOOD_GROUP_FIELD_NUMBER: _ClassVar[int]
    ID_CARD_NUMBER_FIELD_NUMBER: _ClassVar[int]
    UUID_FIELD_NUMBER: _ClassVar[int]
    name: str
    enrollment_number: str
    enrollment_validity: _timestamp_pb2.Timestamp
    batch: str
    program: str
    date_of_birth: _timestamp_pb2.Timestamp
    blood_group: str
    id_card_number: str
    uuid: str
    def __init__(self, name: _Optional[str] = ..., enrollment_number: _Optional[str] = ..., enrollment_validity: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., batch: _Optional[str] = ..., program: _Optional[str] = ..., date_of_birth: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., blood_group: _Optional[str] = ..., id_card_number: _Optional[str] = ..., uuid: _Optional[str] = ...) -> None: ...

class Semester(_message.Message):
    __slots__ = ["name", "ref"]
    NAME_FIELD_NUMBER: _ClassVar[int]
    REF_FIELD_NUMBER: _ClassVar[int]
    name: str
    ref: str
    def __init__(self, name: _Optional[str] = ..., ref: _Optional[str] = ...) -> None: ...

class SemesterList(_message.Message):
    __slots__ = ["semesters"]
    SEMESTERS_FIELD_NUMBER: _ClassVar[int]
    semesters: _containers.RepeatedCompositeFieldContainer[Semester]
    def __init__(self, semesters: _Optional[_Iterable[_Union[Semester, _Mapping]]] = ...) -> None: ...

class WifiMacInfo(_message.Message):
    __slots__ = ["addresses", "slots", "free_slots"]
    ADDRESSES_FIELD_NUMBER: _ClassVar[int]
    SLOTS_FIELD_NUMBER: _ClassVar[int]
    FREE_SLOTS_FIELD_NUMBER: _ClassVar[int]
    addresses: _containers.RepeatedScalarFieldContainer[str]
    slots: int
    free_slots: int
    def __init__(self, addresses: _Optional[_Iterable[str]] = ..., slots: _Optional[int] = ..., free_slots: _Optional[int] = ...) -> None: ...

class DeregisterWifiMacRequest(_message.Message):
    __slots__ = ["address"]
    ADDRESS_FIELD_NUMBER: _ClassVar[int]
    address: str
    def __init__(self, address: _Optional[str] = ...) -> None: ...

class RegisterWifiMacRequest(_message.Message):
    __slots__ = ["address", "override_limit"]
    ADDRESS_FIELD_NUMBER: _ClassVar[int]
    OVERRIDE_LIMIT_FIELD_NUMBER: _ClassVar[int]
    address: str
    override_limit: bool
    def __init__(self, address: _Optional[str] = ..., override_limit: bool = ...) -> None: ...

class FillFacultyFeedbackRequest(_message.Message):
    __slots__ = ["rating", "query_rating", "comment"]
    RATING_FIELD_NUMBER: _ClassVar[int]
    QUERY_RATING_FIELD_NUMBER: _ClassVar[int]
    COMMENT_FIELD_NUMBER: _ClassVar[int]
    rating: int
    query_rating: int
    comment: str
    def __init__(self, rating: _Optional[int] = ..., query_rating: _Optional[int] = ..., comment: _Optional[str] = ...) -> None: ...

class FillFacultyFeedbackResponse(_message.Message):
    __slots__ = ["filled_for"]
    FILLED_FOR_FIELD_NUMBER: _ClassVar[int]
    filled_for: int
    def __init__(self, filled_for: _Optional[int] = ...) -> None: ...
