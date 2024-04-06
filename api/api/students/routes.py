from api.students.exceptions import StudentAlreadyExistsException, StudentNotFoundException
from .dependencies import Students
from fastapi import APIRouter, HTTPException, status

from .schemas import StudentSchema


students = APIRouter()


@students.get("{student_id}", response_model=StudentSchema)
async def get_student(student_id: int, service: Students):
    try:
        return await service.get_student(student_id)
    except StudentNotFoundException as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=exc.message
        ) from exc


@students.post("/")
async def add_new_student(data: StudentSchema, service: Students):
    try:
        return await service.add_new_student(**data.model_dump())
    except StudentAlreadyExistsException as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail=exc.message
        ) from exc
