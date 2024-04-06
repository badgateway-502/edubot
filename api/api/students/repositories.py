from abc import ABC, abstractmethod

from sqlalchemy.ext.asyncio import AsyncSession

from .models import Student


class BaseStudentsRepository(ABC):
    @abstractmethod
    async def add(self, student: Student):
        raise NotImplementedError

    @abstractmethod
    async def get_by_id(self, student_id: int) -> Student | None:
        raise NotImplementedError


class SqlalchemyStudentsRepository(BaseStudentsRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def add(self, student: Student):
        self.session.add(student)
        await self.session.commit()
        await self.session.refresh(student)

    async def get_by_id(self, student_id: int) -> Student | None:
        return await self.session.get(Student, student_id)
