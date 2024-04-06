from .exceptions import SubjectAccessException, SubjectAlreadyExistsException, SubjectNotFoundException
from .models import Subject
from .repositories import BaseSubjectsRepository
from ..teachers.models import Teacher


class SubjectsService:
    def __init__(self, subjects_repo: BaseSubjectsRepository):
        self.subjects_repo = subjects_repo
    
    async def get_subjects(self, teacher_id: int | None = None) -> list[Subject]:
        return await self.subjects_repo.get_all(teacher_id=teacher_id)

    async def create_new_subject(self, name: str, by: Teacher) -> Subject:
        subject = await self.subjects_repo.get_by_name(name)
        if subject is not None:
            raise SubjectAlreadyExistsException(name=name)
        subject = Subject(name=name, teacher_id=by.id)
        await self.subjects_repo.add(subject)
        return subject
    
    async def get_subject_by_id(self, subject_id: int) -> Subject:
        subject = await self.subjects_repo.get_by_id(subject_id)
        if subject is None:
            raise SubjectNotFoundException
        return subject
    
    async def update_subject(self, subject: Subject, by: Teacher, name: str | None = None):
        if subject.teacher_id != by.id:
            raise SubjectAccessException
        if name is not None:
            s = await self.subjects_repo.get_by_name(name)
            if s is not None:
                raise SubjectAlreadyExistsException(name=name)
            subject.name = name
        await self.subjects_repo.add(subject)
    
    async def remove_subject(self, subject: Subject, by: Teacher):
        if subject.teacher_id != by.id:
            raise SubjectAccessException
        await self.subjects_repo.remove(subject)
