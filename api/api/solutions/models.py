from typing import TYPE_CHECKING, Literal, get_args
from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import ForeignKey, Enum, UniqueConstraint

from ..database import Base
if TYPE_CHECKING:
    from ..students.models import Student
    from ..subjects.models import LectureLab, LectureTest


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

    lab: Mapped["LectureLab"] = relationship(lazy="selectin")
    student: Mapped["Student"] = relationship(lazy="selectin")


class TestSolution(Base):
    __tablename__ = "test_solution"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    student_id: Mapped[int] = mapped_column(ForeignKey("student.id"))
    test_id: Mapped[int] = mapped_column(ForeignKey("lecture_test.id"))
    result: Mapped[int]

    test: Mapped["LectureTest"] = relationship(lazy="selectin")
    student: Mapped["Student"] = relationship(lazy="selectin")
