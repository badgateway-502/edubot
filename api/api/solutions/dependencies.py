from typing import Annotated
from fastapi import Depends

from sqlalchemy.ext.asyncio import AsyncSession


from ..database import get_database_session
from .repositories import SqlalchemyLabSolutionsRepository, SqlalchemyTestSolutionsRepository
from .services import SolutionService
from ..subjects.services import HttpxTelegramService
from ..config import Settings, get_settings


def get_solution_service(
    session: Annotated[AsyncSession, Depends(get_database_session)],
    settings: Annotated[Settings, Depends(get_settings)],
) -> SolutionService:
    return SolutionService(
        labs_solutions_repo=SqlalchemyLabSolutionsRepository(session),
        tests_solutions_repo=SqlalchemyTestSolutionsRepository(session),
        telegram_service=HttpxTelegramService(bot_token=settings.bot_token, chat_id=settings.tg_storage_chat_id),
    )


Solutions = Annotated[SolutionService, Depends(get_solution_service)]
