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


class AddTestSolution(BaseModel):
    result: int
    student_id: int
    test_id: int


class ProgressSchema(BaseModel):
    student_id: int
    subject_id: int
    labs_passed: str
    tests_passed: str
