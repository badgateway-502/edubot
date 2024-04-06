from typing import TYPE_CHECKING
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

if TYPE_CHECKING:
    from ..teachers.models import Teacher

from ..database import Base


class Subject(Base):
    __tablename__ = "subject"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(unique=True)
    teacher_id: Mapped[int] = mapped_column(ForeignKey("teacher.id"))
    teacher: Mapped["Teacher"] = relationship(lazy="selectin")
