from pydantic import BaseModel
from ..teachers.schemas import TeacherPublic


class CreateSubject(BaseModel):
    name: str


class SubjectSchema(BaseModel):
    model_config = {"from_attributes": True}

    id: int
    name: str
    teacher: TeacherPublic


class SubjectUpdate(BaseModel):
    name: str | None = None
