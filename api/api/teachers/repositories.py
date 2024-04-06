from abc import ABC, abstractmethod

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from .models import Teacher


class BaseTeacherRepository(ABC):
    @abstractmethod
    async def add(self, teacher: Teacher):
        raise NotImplementedError

    @abstractmethod
    async def get_by_email(self, email: str) -> Teacher | None:
        raise NotImplementedError

    @abstractmethod
    async def get_by_id(self, teacher_id: int) -> Teacher | None:
        raise NotImplementedError


class SqlalchemyTeacherRepository(BaseTeacherRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def add(self, teacher: Teacher):
        self.session.add(teacher)
        await self.session.commit()
        await self.session.refresh(teacher)

    async def get_by_email(self, email: str) -> Teacher | None:
        query = select(Teacher).where(Teacher.email == email)
        result = await self.session.execute(query)
        return result.scalar_one_or_none()

    async def get_by_id(self, teacher_id: int) -> Teacher | None:
        return await self.session.get(Teacher, teacher_id)
