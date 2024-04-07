from datetime import date
from typing import Literal
from pydantic import BaseModel, Field

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
    model_config = {"from_attributes": True}

    id: int
    lecture_id: int
    title: str
    text_description: str | None
    description_file_id: str | None


class AnswerVariant(BaseModel):
    model_config = {"from_attributes": True}

    text: str
    is_right: bool


class Question(BaseModel):
    model_config = {"from_attributes": True}

    question: str
    weight: int
    type: Literal["moder", "scalar", "moderfile", "variant"]
    right_answer: str | None
    variants: list[AnswerVariant] | None


class CreateLectureTest(BaseModel):
    result_to_pass: float = Field(ge=0, le=1)


class UpdateLectureTestSchema(BaseModel):
    result_to_pass: float = Field(ge=0, le=1)
    questions: list[Question]


class LectureTestSchema(BaseModel):
    model_config = {"from_attributes": True}

    id: int
    result_to_pass: float = Field(ge=0, le=1)
    questions: list[Question]



class LectureSchema(BaseModel):
    model_config = {"from_attributes": True}

    id: int
    subject_id: int
    number: int
    title: str
    lab: LabSchema | None
    test: LectureTestSchema | None
    text_description: str | None
    description_file_id: str | None
    video_file_id: str | None
    created_at: date
