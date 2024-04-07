from typing import BinaryIO
from ..subjects.models import LectureLab
from ..students.models import Student
from .repositories import BaseLabSolutionsRepository
from .models import TeacherResponseStatus, LabSolution
from ..subjects.services import BaseTelegramService


class SolutionService:
    def __init__(self, labs_solutions_repo: BaseLabSolutionsRepository, telegram_service: BaseTelegramService):
        self.labs_solutions_repo = labs_solutions_repo
        self.telegram_service = telegram_service
    
    async def get_all_labs_solutions(self, status: TeacherResponseStatus | None = None) -> list[LabSolution]:
        return await self.labs_solutions_repo.get_all(status=status)
    
    async def upload_lab_solution_by_student(self, student: Student, lab: LectureLab, file: BinaryIO, filename: str) -> LabSolution:
        file_id = await self.telegram_service.get_tg_file_id(file, filename)
        solution = LabSolution(student_id=student.id, lab_id=lab.id, file_id=file_id, status="pending")
        await self.labs_solutions_repo.add(solution)
        return solution