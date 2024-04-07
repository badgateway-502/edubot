from typing import Annotated

from api.config import Settings, get_settings
from api.subjects.exceptions import SubjectNotFoundException
from api.subjects.models import Subject

from .repositories import (
    SqlalchemyLabsRepository,
    SqlalchemySubjectsRepository,
    SqlalchemyLecturesRepository,
)
from .services import HttpxTelegramService, LecturesService, SubjectsService
from ..database import get_database_session

from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession


Session = Annotated[AsyncSession, Depends(get_database_session)]


def get_subjects_service(
    session: Session,
) -> SubjectsService:
    return SubjectsService(
        subjects_repo=SqlalchemySubjectsRepository(session),
    )


Subjects = Annotated[SubjectsService, Depends(get_subjects_service)]


async def get_current_subject(subject_id: int, service: Subjects) -> Subject:
    try:
        return await service.get_subject_by_id(subject_id)
    except SubjectNotFoundException as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=exc.message)


CurrentSubject = Annotated[Subject, Depends(get_current_subject)]


async def get_lectures_service(
    session: Session, settings: Annotated[Settings, Depends(get_settings)]
) -> LecturesService:
    return LecturesService(
        lectures_repo=SqlalchemyLecturesRepository(session),
        telegram_service=HttpxTelegramService(
            bot_token=settings.bot_token, chat_id=settings.tg_storage_chat_id
        ),
        labs_repo=SqlalchemyLabsRepository(session),
    )


Lectures = Annotated[LecturesService, Depends(get_lectures_service)]
