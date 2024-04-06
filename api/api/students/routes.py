from .dependencies import Students
from fastapi import APIRouter

from .schemas import StudentSchema


students = APIRouter()


@students.get("{student_id}", response_model=StudentSchema)
async def get_student(student_id: int, service: Students):
    return await service.get_student(student_id)



@students.post("/", response_model=StudentSchema)
async def add_new_student(data: StudentSchema, service: Students):
    return await service.add_new_student(**data.model_dump())

