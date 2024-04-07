from datetime import date
from api.database import Base
from pydantic import BaseModel
from ..teachers.schemas import TeacherPublic


class CreateSubject(BaseModel):
    name: str


class SubjectSchema(BaseModel):
    model_config = {"from_attributes": True}

    id: int
    name: str
    lectures: list["LectureSchema"]
    teacher: TeacherPublic


class SubjectUpdate(BaseModel):
    name: str | None = None


class CreateLecture(BaseModel):
    title: str
    text_description: str | None = None


class UpdateLecture(BaseModel):
    title: str | None = None
    text_description: str | None = None


class CreateLab(BaseModel):
    title: str
    text_description: str | None = None


class UpdateLab(BaseModel):
    title: str | None = None
    text_description: str | None = None


class LabSchema(BaseModel):
    id: int
    lecture_id: int
    title: str
    text_description: str | None
    description_file_id: str | None


class LectureSchema(BaseModel):
    model_config = {"from_attributes": True}

    id: int
    subject_id: int
    number: int
    title: str
    lab: LabSchema | None
    text_description: str | None
    description_file_id: str | None
    video_file_id: str | None
    created_at: date
