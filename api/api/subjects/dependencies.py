from typing import Annotated

from .repositories import SqlalchemySubjectsRepository
from .services import SubjectsService
from ..database import get_database_session

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession


def get_subjects_service(
    session: Annotated[AsyncSession, Depends(get_database_session)],
) -> SubjectsService:
    return SubjectsService(subjects_repo=SqlalchemySubjectsRepository(session))


Subjects = Annotated[SubjectsService, Depends(get_subjects_service)]
