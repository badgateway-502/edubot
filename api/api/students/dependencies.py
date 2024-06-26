from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from .repositories import SqlalchemyStudentsRepository
from .services import StudentsService
from ..database import get_database_session


def get_students_service(
    session: Annotated[AsyncSession, Depends(get_database_session)],
) -> StudentsService:
    return StudentsService(students_repo=SqlalchemyStudentsRepository(session))


Students = Annotated[StudentsService, Depends(get_students_service)]
