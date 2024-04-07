from typing import Literal
from api.teachers.dependencies import Me
from .dependencies import Students
from fastapi import APIRouter

from .schemas import StudentSchema


students = APIRouter()


@students.get("/{student_id}", response_model=StudentSchema)
async def get_student(student_id: int, service: Students):
    return await service.get_student(student_id)


@students.post("/", response_model=StudentSchema)
async def add_new_student(data: StudentSchema, service: Students):
    return await service.add_new_student(**data.model_dump())


@students.get("/", response_model=list[StudentSchema])
async def get_all_students(service: Students):
    return await service.get_all_students()


@students.delete("/{student_id}", response_model=Literal["done"])
async def remove_student(student_id: int, by: Me, service: Students):
    student = await service.get_student(student_id)
    await service.remove_student(student, by)
    return "done"
