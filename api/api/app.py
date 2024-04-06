from fastapi import FastAPI
from starlette.types import ASGIApp

from .teachers.routes import teachers
from .students.routes import students
from .subjects.routes import subjects


def get_app() -> ASGIApp:
    app = FastAPI(
        title="Edubot API",
        description="Edubot API",
        version="0.1.0",
    )

    app.include_router(teachers, prefix="/teachers", tags=["teachers"])
    app.include_router(students, prefix="/students", tags=["students"])
    app.include_router(subjects, prefix="/subjects", tags=["subjects"])

    return app
