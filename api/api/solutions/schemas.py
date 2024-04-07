from typing import Literal
from pydantic import BaseModel

from .models import TeacherResponseStatus


class LabSolutionSchema(BaseModel):
    id: int
    student_id: int
    lab_id: int
    file_id: str
    status: TeacherResponseStatus
    comment: str | None


class CreateLabSolution(BaseModel):
    student_id: int
    lab_id: int
    file_id: str


class UpdateStatusLabSolution(BaseModel):
    status: Literal["right", "wrong"]
    comment: str
