from abc import ABC, abstractmethod

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from .models import TeacherResponseStatus, LabSolution


class BaseLabSolutionsRepository(ABC):
    @abstractmethod
    async def add(self, solution: LabSolution):
        raise NotImplementedError
    
    @abstractmethod
    async def get_by_id(self, solution_id: int) -> LabSolution | None:
        raise NotImplementedError

    @abstractmethod
    async def get_all(self, status: TeacherResponseStatus | None = None) -> list[LabSolution]:
        raise NotImplementedError
    

class SqlalchemyLabSolutionsRepository(BaseLabSolutionsRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_id(self, solution_id: int) -> LabSolution | None:
        return await self.session.get(LabSolution, solution_id)

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
