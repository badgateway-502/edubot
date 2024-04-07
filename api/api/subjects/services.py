from abc import ABC, abstractmethod
from typing import BinaryIO
from httpx import AsyncClient

from datetime import date

from pydantic import NonNegativeFloat
from .exceptions import (
    LectureAccessException,
    LectureAlreadyExistsException,
    LectureNotFoundException,
    SubjectAccessException,
    SubjectAlreadyExistsException,
    SubjectNotFoundException,
    TelegramException,
)
from .models import Lecture, Subject
from .repositories import BaseSubjectsRepository, BaseLecturesRepository
from ..teachers.models import Teacher


from httpx._types import RequestFiles


class BaseTelegramService(ABC):
    @abstractmethod
    async def get_tg_file_id(self, fp: BinaryIO, filename: str) -> str:
        raise NotImplementedError


class HttpxTelegramService(BaseTelegramService):
    def __init__(self, bot_token: str, chat_id: str) -> None:
        self.bot_token = bot_token
        self.chat_id = chat_id
    
    async def get_tg_file_id(self, fp: BinaryIO, filename: str) -> str:
        async with AsyncClient() as client:
            file = {"document": (filename, fp)}
            res = await client.post(f"https://api.telegram.org/bot{self.bot_token}/sendDocument?chat_id={self.chat_id}", files=file)
            if res.status_code == 200:
                return res.json()["result"]["document"]["file_id"]
            else:
                raise TelegramException(res.json())


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
    def __init__(self, lectures_repo: BaseLecturesRepository, telegram_service: BaseTelegramService) -> None:
        self.lectures_repo = lectures_repo
        self.telegram_service = telegram_service

    async def create_new_lecture(
        self, subject: Subject, title: str, text_description: str | None, by: Teacher
    ) -> Lecture:
        if subject.teacher_id != by.id:
            raise SubjectAccessException(id=str(subject.id))
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
    
    async def add_description_file_to_lecture(self, lecture: Lecture, file: BinaryIO, filename: str, by: Teacher):
        if lecture.subject.teacher_id != by.id:
            raise LectureAccessException(id=str(lecture.id))
        file_id = await self.telegram_service.get_tg_file_id(file, filename)
        lecture.description_file_id = file_id
        await self.lectures_repo.add(lecture)

    async def add_video_file_to_lecture(self, lecture: Lecture, file: BinaryIO, filename: str, by: Teacher):
        if lecture.subject.teacher_id != by.id:
            raise LectureAccessException(id=str(lecture.id))
        file_id = await self.telegram_service.get_tg_file_id(file, filename)
        lecture.video_file_id = file_id
        await self.lectures_repo.add(lecture)
    
    async def remove_lecture(self, lecture: Lecture, by: Teacher):
        if lecture.subject.teacher_id != by.id:
            raise LectureAccessException(id=str(lecture.id))
        await self.lectures_repo.remove(lecture)

    async def update_lecture(self, lecture: Lecture, by: Teacher, title: str | None = None, text_description: str | None = None):
        if lecture.subject.teacher_id != by.id:
            raise LectureAccessException(id=str(lecture.id))
        if title is not None:
            l = await self.lectures_repo.get_by_title(lecture.subject_id, title)
            if l is not None:
                raise LectureAlreadyExistsException(title=title)
            lecture.title = title
        if text_description is not None:
            lecture.text_description = text_description
        await self.lectures_repo.add(lecture)

    async def get_lecture_lab(self, lecture: Lecture):
        ...