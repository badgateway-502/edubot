from fastapi import APIRouter, HTTPException, UploadFile, status

from ..students.dependencies import Students
from ..subjects.dependencies import Lectures

from .models import TeacherResponseStatus
from .dependencies import Solutions

from .schemas import LabSolutionSchema
from ..subjects.services import TelegramException

solutions = APIRouter()


@solutions.get("/labs", response_model=list[LabSolutionSchema])
async def get_all_solutions(service: Solutions, status: TeacherResponseStatus | None = None):
    return await service.get_all_labs_solutions(status=status)


@solutions.post("/labs", response_model=LabSolutionSchema)
async def upload_lab_solution(file: UploadFile, student_id: int, lab_id: int, solutions_service: Solutions, lectures_service: Lectures, students_service: Students):
    student = await students_service.get_student(student_id)
    lab = await lectures_service.get_lecture_lab_by_id(lab_id)
    try:
        return await solutions_service.upload_lab_solution_by_student(student, lab, file.file, file.filename or "unknown")
    except TelegramException as exc:
        raise HTTPException(status_code=status.HTTP_502_BAD_GATEWAY, detail="external service error") from exc

