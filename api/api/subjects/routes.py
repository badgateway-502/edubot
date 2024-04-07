from typing import Literal


from api.subjects.exceptions import TelegramException
from fastapi import APIRouter, HTTPException, UploadFile, status

from .schemas import CreateLecture, LectureSchema, SubjectSchema, CreateSubject, SubjectUpdate, UpdateLecture
from ..teachers.dependencies import Me
from .dependencies import CurrentSubject, Subjects, Lectures


subjects = APIRouter()


@subjects.get("/", response_model=list[SubjectSchema])
async def get_all_subjects(service: Subjects, teacher_id: int | None = None):
    return await service.get_subjects(teacher_id)


@subjects.get("/{subject_id}", response_model=SubjectSchema)
async def get_subject_by_id(subject_id: int, service: Subjects):
    return await service.get_subject_by_id(subject_id)



@subjects.post("/", response_model=SubjectSchema)
async def create_new_subject(data: CreateSubject, teacher: Me, service: Subjects):
    return await service.create_new_subject(data.name, teacher)
    


@subjects.patch("/{subject_id}", response_model=SubjectSchema)
async def update_subject(
    subject_id: int, data: SubjectUpdate, teacher: Me, service: Subjects
):
    subject = await service.get_subject_by_id(subject_id)
    await service.update_subject(subject, teacher, **data.model_dump(exclude_none=True))
    return subject


@subjects.delete("/{subject_id}", response_model=Literal["done"])
async def remove_subject(subject_id: int, teacher: Me, service: Subjects):
    subject = await service.get_subject_by_id(subject_id)
    await service.remove_subject(subject, teacher)
    return "done"


@subjects.get("/{subject_id}/lectures/{number}", tags=["lectures"], response_model=LectureSchema)
async def get_lecture_by_number(subject: CurrentSubject, number: int,  service: Lectures):
    return await service.get_lecture_by_number(subject, number)


@subjects.post("/{subject_id}/lectures/", tags=["lectures"], response_model=LectureSchema)
async def create_new_lecture(data: CreateLecture, subject: CurrentSubject, service: Lectures, by: Me):
    return await service.create_new_lecture(subject, data.title, data.text_description, by)


@subjects.post("/{subject_id}/lectures/{number}/upload-description", response_model=LectureSchema)
async def upload_description_file_to_lecture(subject: CurrentSubject, number: int, file: UploadFile, service: Lectures, by: Me):
    lecture = await service.get_lecture_by_number(subject=subject, number=number)
    try:
        await service.add_description_file_to_lecture(lecture=lecture, file=file.file, filename=file.filename or "unknown", by=by)
    except TelegramException as exc:
        raise HTTPException(status_code=status.HTTP_502_BAD_GATEWAY, detail="external service error") from exc
    return lecture


@subjects.post("/{subject_id}/lectures/{number}/upload-video", response_model=LectureSchema)
async def upload_video_file_to_lecture(subject: CurrentSubject, number: int, file: UploadFile, service: Lectures, by: Me):
    lecture = await service.get_lecture_by_number(subject=subject, number=number)
    try:
        await service.add_video_file_to_lecture(lecture=lecture, file=file.file, filename=file.filename or "unknown", by=by)
    except TelegramException as exc:
        raise HTTPException(status_code=status.HTTP_502_BAD_GATEWAY, detail="external service error") from exc
    return lecture


@subjects.patch("/{subject_id}/lectures/{number}", response_model=LectureSchema)
async def update_lecture(data: UpdateLecture, subject: CurrentSubject, number: int, service: Lectures, by: Me):
    lecture = await service.get_lecture_by_number(subject, number)
    await service.update_lecture(lecture, by, data.title, data.text_description)
    return lecture


@subjects.delete("/{subject_id}/lectures/{number}", response_model=Literal["done"])
async def remove_lecture(subject: CurrentSubject, number: int, service: Lectures, by: Me):
    lecture = await service.get_lecture_by_number(subject, number)
    await service.remove_lecture(lecture, by)
    return "done"
