from abc import ABC, abstractmethod

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from .models import Lecture, LectureLab, Subject


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


class BaseLecturesRepository(ABC):
    @abstractmethod
    async def add(self, lecture: Lecture):
        raise NotImplementedError

    @abstractmethod
    async def get_by_id(self, lecture_id: int) -> Lecture | None:
        raise NotImplementedError

    @abstractmethod
    async def get_by_number(self, subject_id: int, number: int) -> Lecture | None:
        raise NotImplementedError

    @abstractmethod
    async def get_max_number(self, subject_id: int) -> int | None:
        raise NotImplementedError

    @abstractmethod
    async def get_by_title(self, subject_id: int, title: str) -> Lecture | None:
        raise NotImplementedError

    @abstractmethod
    async def get_all(
        self,
        offset: int | None = None,
        limit: int | None = None,
        subject_id: int | None = None,
    ) -> list[Lecture]:
        raise NotImplementedError

    @abstractmethod
    async def remove(self, lecture: Lecture) -> None:
        raise NotImplementedError


class SqlalchemyLecturesRepository(BaseLecturesRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def add(self, lecture: Lecture):
        self.session.add(lecture)
        await self.session.commit()
        await self.session.refresh(lecture)

    async def get_all(
        self,
        offset: int | None = None,
        limit: int | None = None,
        subject_id: int | None = None,
    ) -> list[Lecture]:
        query = select(Lecture)
        if subject_id is not None:
            query = query.where(Lecture.subject_id == subject_id)
        if offset is not None:
            query = query.offset(offset)
        if limit is not None:
            query = query.limit(limit)
        result = await self.session.execute(query)
        return list(result.scalars().all())

    async def get_by_id(self, lecture_id: int) -> Lecture | None:
        return await self.session.get(Lecture, lecture_id)

    async def get_by_number(self, subject_id: int, number: int) -> Lecture | None:
        query = select(Lecture).where(
            Lecture.subject_id == subject_id, Lecture.number == number
        )
        result = await self.session.execute(query)
        return result.scalar_one_or_none()

    async def get_by_title(self, subject_id: int, title: str) -> Lecture | None:
        query = select(Lecture).where(
            Lecture.subject_id == subject_id, Lecture.title == title
        )
        result = await self.session.execute(query)
        return result.scalar_one_or_none()

    async def remove(self, lecture: Lecture) -> None:
        await self.session.delete(lecture)
        await self.session.commit()

    async def get_max_number(self, subject_id: int) -> int | None:
        query = select(func.max(Lecture.number)).where(Lecture.subject_id == subject_id)
        result = await self.session.execute(query)
        return result.scalar_one_or_none()


class BaseLabsRepository(ABC):
    @abstractmethod
    async def get_by_lecture_id(self, lecture_id: int) -> LectureLab | None:
        raise NotImplementedError

    @abstractmethod
    async def add(self, lab: LectureLab):
        raise NotImplementedError
    
    @abstractmethod
    async def remove(self, lab: LectureLab):
        raise NotImplementedError


class SqlalchemyLabsRepository(BaseLabsRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_lecture_id(self, lecture_id: int) -> LectureLab | None:
        query = select(LectureLab).where(LectureLab.lecture_id == lecture_id)
        result = await self.session.execute(query)
        return result.scalar_one_or_none()

    async def add(self, lab: LectureLab):
        self.session.add(lab)
        await self.session.commit()
        await self.session.refresh(lab)
    
    async def remove(self, lab: LectureLab):
        await self.session.delete(lab)
        await self.session.commit()
