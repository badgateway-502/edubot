from typing import Literal, get_args
from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy import ForeignKey, Enum

from ..database import Base


TeacherResponseStatus = Literal["right", "wrong", "pending"]

class LabSolution(Base):
    __tablename__ = "lab_solution"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    student_id: Mapped[int] = mapped_column(ForeignKey("student.id"))
    lab_id: Mapped[int] = mapped_column(ForeignKey("lecture_lab.id"))
    file_id: Mapped[str]
    status: Mapped[TeacherResponseStatus] = mapped_column(
        Enum(
            *get_args(TeacherResponseStatus),
            name="teacherresponsestatus",
            create_constraint=True,
            validate_strings=True,
        )
    )
    comment: Mapped[str | None]
