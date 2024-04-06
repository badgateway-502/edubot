from datetime import date
from .exceptions import (
    LectureAlreadyExistsException,
    LectureNotFoundException,
    SubjectAccessException,
    SubjectAlreadyExistsException,
    SubjectNotFoundException,
)
from .models import Lecture, Subject
from .repositories import BaseSubjectsRepository, BaseLecturesRepository
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
            raise SubjectNotFoundException(id=str(subject_id))
        return subject

    async def update_subject(
        self, subject: Subject, by: Teacher, name: str | None = None
    ):
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


class LecturesService:
    def __init__(self, lectures_repo: BaseLecturesRepository) -> None:
        self.lectures_repo = lectures_repo

    async def create_new_lecture(
        self, subject: Subject, title: str, text_description: str | None
    ) -> Lecture:
        lecture = await self.lectures_repo.get_by_title(
            subject_id=subject.id, title=title
        )
        if lecture is not None:
            raise LectureAlreadyExistsException(subject=subject.name, title=title)
        max_number = await self.lectures_repo.get_max_number(subject_id=subject.id) or 0
        lecture = Lecture(
            subject_id=subject.id, title=title, text_description=text_description, created_at=date.today(), number=max_number+1
        )
        await self.lectures_repo.add(lecture)
        return lecture

    async def get_lecture_by_number(self, subject: Subject, number: int) -> Lecture:
        lecture = await self.lectures_repo.get_by_number(
            subject_id=subject.id, number=number
        )
        if lecture is None:
            raise LectureNotFoundException(subject=subject.name, number=str(number))
        return lecture
