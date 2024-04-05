from dataclasses import dataclass
from typing import Dict


@dataclass
class Student:
    id: int
    name: str
    surname: str
    academic_performance: Dict[str, str]
