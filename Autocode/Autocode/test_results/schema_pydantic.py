from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class Employees(BaseModel):
    id: int = Field(default=..., description="Integer column")
    name: str = Field(default=..., description="String column")
    email: str = Field(default=..., description="String column (appears to contain email addresses)")
    age: int = Field(default=..., description="Integer column")
    salary: int = Field(default=..., description="Integer column")
    department: str = Field(default=..., description="String column")
    is_active: bool = Field(default=..., description="Boolean column")
    hire_date: str = Field(default=..., description="String column")