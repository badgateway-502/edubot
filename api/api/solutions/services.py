from typing import BinaryIO, Literal

from .exceptions import LabSolutionAccessDeniedException
from ..subjects.models import LectureLab
from ..students.models import Student
from .repositories import BaseLabSolutionsRepository
from .models import TeacherResponseStatus, LabSolution
from ..subjects.services import BaseTelegramService
from ..teachers.models import Teacher


class SolutionService:
    def __init__(self, labs_solutions_repo: BaseLabSolutionsRepository, telegram_service: BaseTelegramService):
        self.labs_solutions_repo = labs_solutions_repo
        self.telegram_service = telegram_service
    
    async def get_all_labs_solutions(self, status: TeacherResponseStatus | None = None) -> list[LabSolution]:
        return await self.labs_solutions_repo.get_all(status=status)
    
    async def get_lab_solution_by_id(self, solution_id: int) -> LabSolution:
        solution = await self.labs_solutions_repo.get_by_id(solution_id)
        if solution is None:
            raise LabSolutionAccessDeniedException(id=str(solution_id))
        return solution
    
    async def upload_lab_solution_by_student(self, student: Student, lab: LectureLab, file: BinaryIO, filename: str) -> LabSolution:
        file_id = await self.telegram_service.get_tg_file_id(file, filename)
        solution = LabSolution(student_id=student.id, lab_id=lab.id, file_id=file_id, status="pending")
        await self.labs_solutions_repo.add(solution)
        return solution
    
    async def update_solution_status(self, solution: LabSolution, status: Literal["wrong", "right"], comment: str, by: Teacher):
        if solution.lab.lecture.subject.teacher != by.id:
            raise LabSolutionAccessDeniedException(lab_id=str(solution.lab_id))
        solution.status = status
        solution.comment = comment
        await self.labs_solutions_repo.add(solution)
