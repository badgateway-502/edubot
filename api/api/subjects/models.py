from typing import TYPE_CHECKING
from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import date


if TYPE_CHECKING:
    from ..teachers.models import Teacher

from ..database import Base


class Subject(Base):
    __tablename__ = "subject"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(unique=True)
    teacher_id: Mapped[int] = mapped_column(ForeignKey("teacher.id"))
    teacher: Mapped["Teacher"] = relationship(lazy="selectin")
    lectures: Mapped[list["Lecture"]] = relationship(lazy="selectin")


class Lecture(Base):
    __tablename__ = "lecture"
    __table_args__ = (
        UniqueConstraint(
            "number",
            "subject_id",
        ),
        UniqueConstraint(
            "title",
            "subject_id",
        ),
    )

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    number: Mapped[int]
    subject_id: Mapped[int] = mapped_column(ForeignKey("subject.id"))
    title: Mapped[str]
    text_description: Mapped[str | None]
    description_file_id: Mapped[str | None]
    video_file_id: Mapped[str | None]
    lab: Mapped["LectureLab"] = relationship(back_populates="lecture", lazy="selectin")
    created_at: Mapped[date]


class LectureLab(Base):
    __tablename__ = "lecture_lab"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    lecture_id: Mapped[int] = mapped_column(ForeignKey("lecture.id"))
    lecture: Mapped[Lecture] = relationship(back_populates="lab")
    title: Mapped[str]
    text_description: Mapped[str | None]
    description_file_id: Mapped[str | None]
