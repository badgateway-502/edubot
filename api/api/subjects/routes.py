from typing import Literal

from api.subjects.exceptions import SubjectAccessException, SubjectAlreadyExistsException, SubjectNotFoundException
from fastapi import APIRouter, HTTPException, status

from .schemas import SubjectSchema, CreateSubject, SubjectUpdate
from ..teachers.dependencies import Me
from .dependencies import Subjects


subjects = APIRouter()


@subjects.get("/", response_model=list[SubjectSchema])
async def get_all_subjects(service: Subjects, teacher_id: int | None = None):
    return await service.get_subjects(teacher_id)


@subjects.get("/{subject_id}", response_model=SubjectSchema)
async def get_subject_by_id(subject_id: int, service: Subjects):
    try:
        return await service.get_subject_by_id(subject_id)
    except SubjectNotFoundException as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=exc.message) from exc


@subjects.post("/", response_model=SubjectSchema)
async def create_new_subject(data: CreateSubject, teacher: Me, service: Subjects):
    try:
        return await service.create_new_subject(data.name, teacher)
    except SubjectAlreadyExistsException as exc:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=exc.message)


@subjects.patch("/{subject_id}", response_model=SubjectSchema)
async def update_subject(
    subject_id: int, data: SubjectUpdate, teacher: Me, service: Subjects
):
    try:
        subject = await service.get_subject_by_id(subject_id)
    except SubjectNotFoundException as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=exc.message) from exc
    try:
        await service.update_subject(subject, teacher, **data.model_dump(exclude_none=True))
    except SubjectAccessException as exc:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=exc.message) from exc
    return subject


@subjects.delete("/{subject_id}", response_model=Literal["done"])
async def remove_subject(subject_id: int, teacher: Me, service: Subjects):
    try:
        subject = await service.get_subject_by_id(subject_id)
    except SubjectNotFoundException as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=exc.message) from exc
    try:
        await service.remove_subject(subject, teacher)
    except SubjectAccessException as exc:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=exc.message) from exc
    return "done"
