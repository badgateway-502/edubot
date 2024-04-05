from fastapi import APIRouter, HTTPException, status

from .schemas import TeacherPublic, TeacherCreate, TeacherUpdate, TeacherPrivate
from .dependencies import Teachers, Me
from .exceptions import TeacherNotFoundException, AuthenticationException


teachers = APIRouter()


@teachers.get("/me", response_model=TeacherPrivate)
async def get_current_teacher(teacher: Me):
    return teacher


@teachers.get("/{teacher_id}", response_model=TeacherPublic)
async def get_teacher_by_id(teacher_id: int, service: Teachers):
    try:
        return await service.get_teacher(teacher_id)
    except TeacherNotFoundException as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(exc.message)
        ) from exc
