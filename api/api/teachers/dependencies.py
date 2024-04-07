from typing import Annotated

from fastapi import Depends, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from .models import Teacher
from ..config import Settings, get_settings
from ..database import get_database_session
from .services import TeacherService, BcryptPasswordService, JoseJWTService
from .repositories import SqlalchemyTeacherRepository
from .exceptions import AuthenticationException


async def get_teacher_service(
    session: Annotated[AsyncSession, Depends(get_database_session)],
    settings: Annotated[Settings, Depends(get_settings)],
) -> TeacherService:
    return TeacherService(
        repo=SqlalchemyTeacherRepository(session=session),
        pwd_service=BcryptPasswordService(),
        jwt_service=JoseJWTService(
            secret_key=settings.access_token_secret_key,
            algorithm=settings.access_token_algorithm,
        ),
        access_token_expires_minutes=settings.access_token_expires_minutes,
    )


Teachers = Annotated[TeacherService, Depends(get_teacher_service)]


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/teachers/login")


async def get_current_teacher(
    service: Teachers, token: Annotated[str, Depends(oauth2_scheme)]
):
    try:
        return await service.get_teacher_by_access_token(token=token)
    except AuthenticationException as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(exc.message),
        )


Me = Annotated[Teacher, Depends(get_current_teacher)]

LoginForm = Annotated[OAuth2PasswordRequestForm, Depends()]
