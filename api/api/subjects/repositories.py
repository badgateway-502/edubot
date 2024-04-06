from abc import ABC, abstractmethod

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from .models import Subject


class BaseSubjectsRepository(ABC):
    @abstractmethod
    async def add(self, subject: Subject):
        raise NotImplementedError

    @abstractmethod
    async def get_by_id(self, subject_id: int) -> Subject | None:
        raise NotImplementedError

    @abstractmethod
    async def get_by_name(self, name: str) -> Subject | None:
        raise NotImplementedError

    @abstractmethod
    async def get_all(
        self,
        offset: int | None = None,
        limit: int | None = None,
        teacher_id: int | None = None,
    ) -> list[Subject]:
        raise NotImplementedError
    
    @abstractmethod
    async def remove(self, subject: Subject) -> None:
        raise NotImplementedError


class SqlalchemySubjectsRepository(BaseSubjectsRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def add(self, subject: Subject):
        self.session.add(subject)
        await self.session.commit()
        await self.session.refresh(subject)

    async def get_by_id(self, subject_id: int) -> Subject | None:
        return await self.session.get(Subject, subject_id)

    async def get_all(
        self,
        offset: int | None = None,
        limit: int | None = None,
        teacher_id: int | None = None,
    ) -> list[Subject]:
        query = select(Subject)
        if teacher_id is not None:
            query = query.where(Subject.teacher_id == teacher_id)
        if offset is not None:
            query = query.offset(offset)
        if limit is not None:
            query = query.limit(limit)
        result = await self.session.execute(query)
        return list(result.scalars().all())

    async def get_by_name(self, name: str) -> Subject | None:
        query = select(Subject).where(Subject.name == name)
        result = await self.session.execute(query)
        return result.scalar_one_or_none()
    
    async def remove(self, subject: Subject) -> None:
        await self.session.delete(subject)
        await self.session.commit()
