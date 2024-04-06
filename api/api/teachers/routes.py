from fastapi import APIRouter, HTTPException, status

from .schemas import TeacherPublic, TeacherCreate, TeacherUpdate, TeacherPrivate, Token
from .dependencies import Teachers, Me, LoginForm
from .exceptions import (
    TeacherNotFoundException,
    AuthenticationException,
    TeacherAlreadyExistsException,
)


teachers = APIRouter()


@teachers.get("/me", response_model=TeacherPrivate)
async def get_current_teacher(teacher: Me):
    return teacher


@teachers.patch("/me", response_model=TeacherPrivate)
async def update_teachers_profile(data: TeacherUpdate, teacher: Me, service: Teachers):
    await service.update_teacher(teacher, **data.model_dump(exclude_none=True))
    return teacher


@teachers.get("/{teacher_id}", response_model=TeacherPublic)
async def get_teacher_by_id(teacher_id: int, service: Teachers):
    try:
        return await service.get_teacher(teacher_id)
    except TeacherNotFoundException as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(exc.message)
        ) from exc


@teachers.post("/", response_model=TeacherPublic)
async def register_teacher(data: TeacherCreate, service: Teachers):
    try:
        return await service.register_teacher(
            email=data.email,
            password=data.password,
            firstname=data.firstname,
            lastname=data.lastname,
        )
    except TeacherAlreadyExistsException as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail=exc.message
        ) from exc


@teachers.post("/login", response_model=Token)
async def login(form_data: LoginForm, service: Teachers):
    try:
        teacher = await service.authenticate_teacher(
            email=form_data.username, password=form_data.password
        )
    except AuthenticationException as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=exc.message,
        ) from exc
    token = service.create_access_token(teacher)
    return Token(access_token=token, token_type="bearer")
