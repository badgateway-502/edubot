from sqlalchemy import ForeignKey, UniqueConstraint, Enum
from sqlalchemy.orm import mapped_column, Mapped
from ..database import Base
from typing import Literal, get_args


class Student(Base):
    __tablename__ = "student"

    id: Mapped[int] = mapped_column(primary_key=True)
    firstname: Mapped[str]
    lastname: Mapped[str]
