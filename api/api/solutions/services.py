from typing import BinaryIO, Literal

from .exceptions import LabSolutionAccessDeniedException
from ..subjects.models import LectureLab, LectureTest, Subject
from ..students.models import Student
from .repositories import BaseLabSolutionsRepository, BaseTestSolutionsRepository
from .models import TeacherResponseStatus, LabSolution, TestSolution
from ..subjects.services import BaseTelegramService
from ..teachers.models import Teacher


class SolutionService:
    def __init__(self, labs_solutions_repo: BaseLabSolutionsRepository, tests_solutions_repo: BaseTestSolutionsRepository, telegram_service: BaseTelegramService):
        self.labs_solutions_repo = labs_solutions_repo
        self.tests_solutions_repo = tests_solutions_repo
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
    
    async def get_test_solution_by_subject_and_student(self, subject: Subject, student: Student) -> list[TestSolution]:
        return await self.tests_solutions_repo.get_all_by_subject_and_user(subject.id, student.id)
    
    async def add_test_solution(self, test: LectureTest, student: Student, result: int) -> TestSolution:
        solution = TestSolution(student_id=student.id, test_id=test.id)
        await self.tests_solutions_repo.add(solution)
        return solution
    
    async def get_stdeunt_test_passed_count(self, student: Student, subject: Subject) -> int:
        solutions = await self.tests_solutions_repo.get_all_by_subject_and_user(subject.id, student.id)
        return sum([1 for s in solutions if s.test.result_to_pass > s.result])
        
    async def get_student_passed_labs_count(self, student: Student, subject: Subject) -> int:
        solutions = await self.labs_solutions_repo.get_all_by_subject_and_user(subject.id, student.id)
        return sum([1 for s in solutions if s.status == "right"])
        

