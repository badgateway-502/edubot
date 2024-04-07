from dataclasses import dataclass
from typing import Dict

# сущность студент имеет 3 атрибута
@dataclass
class Student:
    name: str
    surname: str
    academic_performance: Dict
