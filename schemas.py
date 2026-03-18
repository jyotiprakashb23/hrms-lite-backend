from pydantic import BaseModel, EmailStr, ConfigDict, Field
from datetime import date
from enum import Enum


class EmployeeCreate(BaseModel):
    full_name: str
    email: EmailStr
    department: str


class AttendanceStatus(str,Enum):
    present = "present"
    absent = "absent"

class AttendanceCreate(BaseModel):
    employee_id: str = Field(
        ...,
        description="Unique employee identifier (e.g., EMP-33894A)"
    )
    date: date
    status: AttendanceStatus

    model_config = ConfigDict(extra="forbid")

class EmployeeResponse(BaseModel):
    employee_id: str
    full_name: str
    email: str
    department: str

    class Config:
        from_attributes = True