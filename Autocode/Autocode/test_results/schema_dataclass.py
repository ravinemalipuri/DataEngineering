from dataclasses import dataclass
from typing import Optional
from datetime import datetime

@dataclass
class Employees:
    id: int
    name: str
    email: str
    age: int
    salary: int
    department: str
    is_active: bool
    hire_date: str