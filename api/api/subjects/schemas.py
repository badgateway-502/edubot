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


class ScalarQuestion(BaseModel):
    model_config = {"from_attributes": True}

    question: str
    right_answer: str
    type: Literal["scalar"]


class ModerQuestion(BaseModel):
    model_config = {"from_attributes": True}

    question: str
    type: Literal["moder"]


class ModerFileQuestion(BaseModel):
    model_config = {"from_attributes": True}

    question: str
    type: Literal["moderfile"]


class AnswerVariant(BaseModel):
    model_config = {"from_attributes": True}

    text: str
    is_right: bool


class VariantQuestion(BaseModel):
    model_config = {"from_attributes": True}

    question: str
    type: Literal["moder"]
    variants: list[AnswerVariant]


class LectureTestSchema(BaseModel):
    model_config = {"from_attributes": True}

    result_to_pass: float = Field(ge=0, le=1)
    questions: list[ScalarQuestion | ModerQuestion | ModerQuestion | VariantQuestion]
