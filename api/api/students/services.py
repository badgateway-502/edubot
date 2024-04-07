from api.students.exceptions import (
    StudentAlreadyExistsException,
    StudentNotFoundException,
)
from .repositories import BaseStudentsRepository
from .models import Student
from ..teachers.models import Teacher


class StudentsService:
    def __init__(self, students_repo: BaseStudentsRepository):
        self.students_repo = students_repo

    async def get_student(self, student_id: int) -> Student:
        student = await self.students_repo.get_by_id(student_id)
        if student is None:
            raise StudentNotFoundException(id=str(student_id))
        return student

    async def add_new_student(self, id: int, firstname: str, lastname: str) -> Student:
        student = await self.students_repo.get_by_id(id)
        if student is not None:
            raise StudentAlreadyExistsException(id=str(id))
        student = Student(id=id, firstname=firstname, lastname=lastname)
        await self.students_repo.add(student)
        return student

    async def get_all_students(self) -> list[Student]:
        return await self.students_repo.get_all()

    async def remove_student(self, student: Student, _by: Teacher):
        await self.students_repo.remove(student)
