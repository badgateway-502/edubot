from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import mapped_column, Mapped
from ..database import Base


class Student(Base):
    __tablename__ = "student"

    id: Mapped[int] = mapped_column(primary_key=True)
    firstname: Mapped[str]
    lastname: Mapped[str]


class StudentsProgress(Base):
    __tablename__ = "students_progress"
    __table_args__ = (
        UniqueConstraint("student_id", ),
    )

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    student_id: Mapped[int] = mapped_column(ForeignKey("student.id"))
    subject_id: Mapped[int] = mapped_column(ForeignKey("subject.id"))
    current_lecture: Mapped[int] = mapped_column(ForeignKey("lecture.id"))


