from abc import ABC, abstractmethod

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from ..subjects.models import Lecture, LectureLab, LectureTest

from .models import TeacherResponseStatus, LabSolution, TestSolution


class BaseLabSolutionsRepository(ABC):
    @abstractmethod
    async def add(self, solution: LabSolution):
        raise NotImplementedError
    
    @abstractmethod
    async def get_by_id(self, solution_id: int) -> LabSolution | None:
        raise NotImplementedError
    
    @abstractmethod
    async def get_all_by_subject_and_user(self, student_id: int, subject_id: int) -> list[LabSolution]:
        raise NotImplementedError

    @abstractmethod
    async def get_all(self, status: TeacherResponseStatus | None = None) -> list[LabSolution]:
        raise NotImplementedError
    

class SqlalchemyLabSolutionsRepository(BaseLabSolutionsRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_id(self, solution_id: int) -> LabSolution | None:
        return await self.session.get(LabSolution, solution_id)

    async def get_all_by_subject_and_user(self, student_id: int, subject_id: int) -> list[LabSolution]:
        query = (
            select(LabSolution, LectureLab, Lecture, )
                .where(LabSolution.student_id == student_id)
                .where(LabSolution.lab_id == LectureLab.id)
                .where(LectureLab.lecture_id == Lecture.id)
                .where(Lecture.subject_id == subject_id)
        )
        result = await self.session.execute(query)
        return list(result.scalars().all())

    async def add(self, solution: LabSolution):
        self.session.add(solution)
        await self.session.commit()
        await self.session.refresh(solution)

    async def get_all(self, status: TeacherResponseStatus | None = None) -> list[LabSolution]:
        query = select(LabSolution)
        if status is not None:
            query = query.where(LabSolution.status == status)
        result = await self.session.execute(query)
        return list(result.scalars().all())


class BaseTestSolutionsRepository(ABC):
    @abstractmethod
    async def add(self, solution: TestSolution):
        raise NotImplementedError
    
    @abstractmethod
    async def get_by_id(self, solution_id: int) -> TestSolution | None:
        raise NotImplementedError

    @abstractmethod
    async def get_all_by_subject_and_user(self, student_id: int, subject_id: int) -> list[TestSolution]:
        raise NotImplementedError
    
    @abstractmethod
    async def get_students_tests_solutions(self, student_id: int, test_id: int) -> list[TestSolution]:
        raise NotImplementedError
    

class SqlalchemyTestSolutionsRepository(BaseTestSolutionsRepository):
    def __init__(self, session: AsyncSession):
        self.session = session
    
    async def get_by_id(self, solution_id: int) -> TestSolution | None:
        return await self.session.get(TestSolution, solution_id)
    
    async def add(self, solution: TestSolution):
        self.session.add(solution)
        await self.session.commit()
        await self.session.refresh(solution)
    
    async def get_students_tests_solutions(self, student_id: int, test_id: int) -> list[TestSolution]:
        query = select(TestSolution).where(TestSolution.student_id == student_id).where(TestSolution.test_id == test_id)
        result = await self.session.execute(query)
        return list(result.scalars().all())
    
    async def get_all_by_subject_and_user(self, student_id: int, subject_id: int) -> list[TestSolution]:
        query = (
            select(TestSolution, LectureTest,  Lecture, )
                .where(TestSolution.student_id == student_id)
                .where(TestSolution.test_id == LectureTest.id)
                .where(LectureTest.lecture_id == Lecture.id)
                .where(Lecture.subject_id == subject_id)
        )
        result = await self.session.execute(query)
        return list(result.scalars().all())
