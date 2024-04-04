from dataclasses import dataclass
from typing import Dict


@dataclass
class Student:
    id: int
    name: str
    surname: str
    academic_performance: Dict[str, str]

    def get_info(self) -> dict:
        return {
            'id': self.id,
            'name': self.name,
            'surname': self.surname,
            'academic_performance': self.academic_performance
        }
