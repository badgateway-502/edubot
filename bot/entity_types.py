from typing import TypedDict, List


# типы сущностей
class TeacherType(TypedDict):
    id: int
    firstname: str
    lastname: str


class LectureType(TypedDict):
    id: int
    subject_id: int
    number: int
    title: str
    text_description: str
    description_file_id: None | int
    video_file_id: None | int
    created_at: str


class SubjectType(TypedDict):
    id: int
    name: str
    lectures: List[LectureType]
    teacher: TeacherType


class SubjectTitle_IdType(TypedDict):
    name: int


class StudentType(TypedDict):
    id: int
    firstname: str
    lastname: str
