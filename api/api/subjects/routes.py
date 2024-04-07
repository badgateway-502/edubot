from typing import Literal


from api.subjects.exceptions import TelegramException
from fastapi import APIRouter, HTTPException, UploadFile, status

from .schemas import (
    CreateLab,
    CreateLecture,
    CreateLectureTest,
    LabSchema,
    LectureSchema,
    LectureTestSchema,
    SubjectSchema,
    CreateSubject,
    SubjectUpdate,
    UpdateLab,
    UpdateLecture,
    UpdateLectureTestSchema,
)
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


@subjects.get(
    "/{subject_id}/lectures/{number}", tags=["lectures"], response_model=LectureSchema
)
async def get_lecture_by_number(
    subject: CurrentSubject, number: int, service: Lectures
):
    return await service.get_lecture_by_number(subject, number)


@subjects.post(
    "/{subject_id}/lectures/", tags=["lectures"], response_model=LectureSchema
)
async def create_new_lecture(
    data: CreateLecture, subject: CurrentSubject, service: Lectures, by: Me
):
    return await service.create_new_lecture(
        subject, data.title, data.text_description, by
    )


@subjects.post(
    "/{subject_id}/lectures/{number}/upload-description",
    response_model=LectureSchema,
    tags=["lectures"],
)
async def upload_description_file_to_lecture(
    subject: CurrentSubject, number: int, file: UploadFile, service: Lectures, by: Me
):
    lecture = await service.get_lecture_by_number(subject=subject, number=number)
    try:
        await service.add_description_file_to_lecture(
            lecture=lecture, file=file.file, filename=file.filename or "unknown", by=by
        )
    except TelegramException as exc:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY, detail="external service error"
        ) from exc
    return lecture


@subjects.post(
    "/{subject_id}/lectures/{number}/upload-video",
    response_model=LectureSchema,
    tags=["lectures"],
)
async def upload_video_file_to_lecture(
    subject: CurrentSubject, number: int, file: UploadFile, service: Lectures, by: Me
):
    lecture = await service.get_lecture_by_number(subject=subject, number=number)
    try:
        await service.add_video_file_to_lecture(
            lecture=lecture, file=file.file, filename=file.filename or "unknown", by=by
        )
    except TelegramException as exc:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY, detail="external service error"
        ) from exc
    return lecture


@subjects.patch(
    "/{subject_id}/lectures/{number}", response_model=LectureSchema, tags=["lectures"]
)
async def update_lecture(
    data: UpdateLecture, subject: CurrentSubject, number: int, service: Lectures, by: Me
):
    lecture = await service.get_lecture_by_number(subject, number)
    await service.update_lecture(lecture, by, data.title, data.text_description)
    return lecture


@subjects.delete(
    "/{subject_id}/lectures/{number}", response_model=Literal["done"], tags=["lectures"]
)
async def remove_lecture(
    subject: CurrentSubject, number: int, service: Lectures, by: Me
):
    lecture = await service.get_lecture_by_number(subject, number)
    await service.remove_lecture(lecture, by)
    return "done"


@subjects.post(
    "/{subject_id}/lectures/{number}/lab",
    response_model=LabSchema,
    tags=["lectures", "labs"],
)
async def add_lecture_lab(data: CreateLab, subject: CurrentSubject, number: int, service: Lectures, by: Me):
    lecture = await service.get_lecture_by_number(subject, number)
    return await service.add_lecture_lab(lecture, by, data.title, data.text_description)

@subjects.get(
    "/{subject_id}/lectures/{number}/lab",
    response_model=LabSchema,
    tags=["lectures", "labs"],
)
async def get_lecture_lab(subject: CurrentSubject, number: int, service: Lectures):
    lecture = await service.get_lecture_by_number(subject, number)
    return await service.get_lecture_lab(lecture)


@subjects.patch(
    "/{subject_id}/lectures/{number}/lab",
    response_model=LabSchema,
    tags=["lectures", "labs"],
)
async def update_lecture_lab(
    data: UpdateLab, subject: CurrentSubject, number: int, service: Lectures, by: Me
):
    lecture = await service.get_lecture_by_number(subject, number)
    lab = await service.get_lecture_lab(lecture)
    await service.update_lecture_lab(lab, by, data.title, data.text_description)
    return lab


@subjects.delete(
    "/{subject_id}/lectures/{number}/lab",
    response_model=Literal["done"],
    tags=["lectures", "labs"],
)
async def remove_lecture_lab(
    data: UpdateLab, subject: CurrentSubject, number: int, service: Lectures, by: Me
):
    lecture = await service.get_lecture_by_number(subject, number)
    lab = await service.get_lecture_lab(lecture)
    await service.remove_lecture_lab(lab, by)
    return "done"


@subjects.post(
    "/{subject_id}/lectures/{number}/lab/upload-description",
    response_model=LabSchema,
    tags=["lectures", "labs"],
)
async def attach_file_to_lecture_lab(
    file: UploadFile, subject: CurrentSubject, number: int, service: Lectures, by: Me
):
    lecture = await service.get_lecture_by_number(subject, number)
    lab = await service.get_lecture_lab(lecture)
    try:
        await service.attach_file_to_lecture_lab(
            lab=lab, file=file.file, filename=file.filename or "unknown", by=by
        )
    except TelegramException as exc:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY, detail="external service error"
        ) from exc
    return lab


@subjects.get(
    "/{subject_id}/lectures/{number}/test/",
    response_model=LectureTestSchema,
    tags=["lectures", "test"],
)
async def get_lecture_test(subject: CurrentSubject, number: int, service: Lectures):
    lecture = await service.get_lecture_by_number(subject, number)
    return await service.get_lecture_test(lecture)


@subjects.post(
    "/{subject_id}/lectures/{number}/test/",
    response_model=LectureTestSchema,
    tags=["lectures", "test"],
)
async def create_lecture_test(
    data: CreateLectureTest,
    subject: CurrentSubject,
    number: int,
    service: Lectures,
    by: Me,
):
    lecture = await service.get_lecture_by_number(subject, number)
    return await service.create_lecture_test(lecture, by, data.result_to_pass)


@subjects.put(
    "/{subject_id}/lectures/{number}/test/",
    response_model=LectureTestSchema,
    tags=["lectures", "test"],
)
async def update_lecture_test(
    data: UpdateLectureTestSchema,
    subject: CurrentSubject,
    number: int,
    service: Lectures,
    by: Me,
):
    lecture = await service.get_lecture_by_number(subject, number)
    test = await service.get_lecture_test(lecture)
    return await service.update_lecture_test(test, data, by)


@subjects.delete(
    "/{subject_id}/lectures/{number}/test/",
    response_model=Literal["done"],
    tags=["lectures", "test"],
)
async def remove_lecture_test(
    data: LectureTestSchema,
    subject: CurrentSubject,
    number: int,
    service: Lectures,
    by: Me,
):
    lecture = await service.get_lecture_by_number(subject, number)
    test = await service.get_lecture_test(lecture)
    await service.remove_lecture_test(test, by)
    return "done"
