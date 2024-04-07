from typing import TYPE_CHECKING, Literal, Optional, get_args
from sqlalchemy import ForeignKey, UniqueConstraint, Enum
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
    lectures: Mapped[list["Lecture"]] = relationship(
        lazy="selectin", cascade="all, delete-orphan"
    )


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
    subject: Mapped[Subject] = relationship(back_populates="lectures")
    title: Mapped[str]
    text_description: Mapped[str | None]
    description_file_id: Mapped[str | None]
    video_file_id: Mapped[str | None]
    lab: Mapped[Optional["LectureLab"]] = relationship(
        back_populates="lecture", lazy="selectin", cascade="all, delete-orphan"
    )
    test: Mapped[Optional["LectureTest"]] = relationship(
        back_populates="lecture", lazy="selectin", cascade="all, delete-orphan"
    )
    created_at: Mapped[date]


class LectureLab(Base):
    __tablename__ = "lecture_lab"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    lecture_id: Mapped[int] = mapped_column(ForeignKey("lecture.id"), unique=True)
    lecture: Mapped[Lecture] = relationship(back_populates="lab")
    title: Mapped[str]
    text_description: Mapped[str | None]
    description_file_id: Mapped[str | None]


class LectureTest(Base):
    __tablename__ = "lecture_test"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    lecture_id: Mapped[int] = mapped_column(ForeignKey("lecture.id"), unique=True)
    lecture: Mapped[Lecture] = relationship(back_populates="test")
    questions: Mapped[list["TestQuestion"]] = relationship(
        back_populates="test", cascade="all, delete-orphan", lazy="selectin"
    )
    result_to_pass: Mapped[float]


QuestionType = Literal["scalar", "moder", "moderfile", "variant"]


class TestQuestion(Base):
    __tablename__ = "test_question"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    test_id: Mapped[int] = mapped_column(ForeignKey("lecture_test.id"))
    test: Mapped[LectureTest] = relationship(back_populates="questions")
    weight: Mapped[int]
    question: Mapped[str]
    right_answer: Mapped[str | None]
    variants: Mapped[list["AnswerVariant"]] = relationship(
        back_populates="question", cascade="all, delete-orphan", lazy="joined"
    )
    type: Mapped[QuestionType] = mapped_column(
        Enum(
            *get_args(QuestionType),
            name="questointype",
            create_constraint=True,
            validate_strings=True,
        )
    )


class AnswerVariant(Base):
    __tablename__ = "answer_variant"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    question_id: Mapped[int] = mapped_column(ForeignKey("test_question.id"))
    question: Mapped[TestQuestion] = relationship(back_populates="variants")
    text: Mapped[str]
    is_right: Mapped[bool]
