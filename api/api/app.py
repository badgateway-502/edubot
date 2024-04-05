from fastapi import FastAPI
from starlette.types import ASGIApp

from .teachers.routes import teachers

def get_app() -> ASGIApp:
    app = FastAPI(
        title="Edubot API",
        description="Edubot API",
        version="0.1.0",
    )

    app.include_router(teachers, prefix="/teachers", tags=["teachers"])


    return app
