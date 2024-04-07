from typing import Literal
from fastapi import APIRouter, HTTPException, UploadFile, status

from ..students.dependencies import Students
from ..subjects.dependencies import Lectures, Subjects
from ..teachers.dependencies import Me
from .models import TeacherResponseStatus
from .dependencies import Solutions

from .schemas import AddTestSolution, LabSolutionSchema, ProgressSchema, UpdateStatusLabSolution
from ..subjects.services import TelegramException


solutions = APIRouter()


@solutions.get("/labs", response_model=list[LabSolutionSchema])
async def get_all_solutions(service: Solutions, status: TeacherResponseStatus | None = None):
    return await service.get_all_labs_solutions(status=status)


@solutions.post("/labs", response_model=LabSolutionSchema)
async def upload_lab_solution(file: UploadFile, student_id: int, lab_id: int, solutions_service: Solutions, lectures_service: Lectures, students_service: Students):
    student = await students_service.get_student(student_id)
    lab = await lectures_service.get_lecture_lab_by_id(lab_id)
    try:
        return await solutions_service.upload_lab_solution_by_student(student, lab, file.file, file.filename or "unknown")
    except TelegramException as exc:
        raise HTTPException(status_code=status.HTTP_502_BAD_GATEWAY, detail="external service error") from exc


@solutions.put("/labs/{solution_id}", response_model=LabSolutionSchema)
async def update_solution_status(solution_id: int, data: UpdateStatusLabSolution, service: Solutions, by: Me):
    solution = await service.get_lab_solution_by_id(solution_id)
    await service.update_solution_status(solution, data.status, data.comment, by)
    return solution


@solutions.post("/tests")
async def add_test_solution(result: AddTestSolution, service: Solutions, lectures_service: Lectures, students_service: Students):
    student = await students_service.get_student(result.student_id)
    test = await lectures_service.get_lecture_test_by_id(result.test_id)
    return await service.add_test_solution(test, student, result.result)


@solutions.get("/progress", response_model=list[ProgressSchema])
async def get_progress(student_id: int, service: Solutions, students_service: Students, subject_service: Subjects):
    student = await students_service.get_student(student_id)
    subjects = await subject_service.get_subjects()

    res = []

    for subject in subjects:
        tests_passed = await service.get_stdeunt_test_passed_count(student, subject)
        tests_count = len(await subject_service.get_all_subjects_tests(subject))

        labs_passed = await service.get_student_passed_labs_count(student, subject)
        labs_count = len(await subject_service.get_all_subjects_labs(subject))

        progress = ProgressSchema(
            subject_id=subject.id,
            student_id=student_id,
            tests_passed=f"{tests_passed}/{tests_count}",
            labs_passed=f"{labs_passed}/{labs_count}",
        )
        res.append(progress)
        
    return res

