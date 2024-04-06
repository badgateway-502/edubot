from abc import ABC, abstractmethod

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from .models import Student


class BaseStudentsRepository(ABC):
    @abstractmethod
    async def add(self, student: Student):
        raise NotImplementedError

    @abstractmethod
    async def get_by_id(self, student_id: int) -> Student | None:
        raise NotImplementedError
    
    @abstractmethod
    async def get_all(self, offset: int | None = None, limit: int | None = None):
        raise NotImplementedError
    
    @abstractmethod
    async def remove(self, student: Student):
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

    async def get_all(self, offset: int | None = None, limit: int | None = None) -> list[Student]:
        query = select(Student)
        if offset is not None:
            query = query.offset(offset)
        if limit is not None:
            query = query.limit(limit)
        result = await self.session.execute(query)
        return list(result.scalars().all())
    
    async def remove(self, student: Student):
        await self.session.delete(student)
        await self.session.commit()
