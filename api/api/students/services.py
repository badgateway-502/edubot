from api.students.exceptions import StudentAlreadyExistsException, StudentNotFoundException
from .repositories import BaseStudentsRepository
from .models import Student


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
