from api.exceptions import (
    ItemAccessDeniedException,
    ItemAlreadyExistsException,
    ItemException,
    ItemNotFoundException,
)
from fastapi import FastAPI, HTTPException, Request, Response, status
from fastapi.exception_handlers import http_exception_handler
from fastapi.responses import ORJSONResponse
from starlette.types import ASGIApp

from .teachers.routes import teachers
from .students.routes import students
from .subjects.routes import subjects
from .solutions.routes import solutions

async def item_exception_handler(request: Request, exception: Exception) -> Response:
    codes_mapping = {
        ItemNotFoundException: status.HTTP_404_NOT_FOUND,
        ItemAlreadyExistsException: status.HTTP_409_CONFLICT,
        ItemAccessDeniedException: status.HTTP_403_FORBIDDEN,
    }

    for key, status_code in codes_mapping.items():
        if isinstance(exception, key):
            return ORJSONResponse(
                status_code=status_code, content={"detail": exception.message}
            )
    return await http_exception_handler(
        request=request,
        exc=HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="unknown error"
        ),
    )


def get_app() -> ASGIApp:
    app = FastAPI(
        title="Edubot API",
        description="Edubot API",
        version="0.1.0",
    )

    app.include_router(teachers, prefix="/teachers", tags=["teachers"])
    app.include_router(students, prefix="/students", tags=["students"])
    app.include_router(subjects, prefix="/subjects", tags=["subjects"])
    app.include_router(solutions, prefix="/solutions", tags=["solutions"])
    app.add_exception_handler(ItemException, item_exception_handler)

    return app
