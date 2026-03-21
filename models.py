from sqlalchemy import Column, Integer, String, Date, ForeignKey, DateTime, Index
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime


class Employee(Base):
    __tablename__ = "employees"

    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(String, unique=True, index=True)
    full_name = Column(String)
    email = Column(String, unique=True, index=True)
    department = Column(String)

    created_at = Column(DateTime, default=datetime.utcnow)


class Attendance(Base):
    __tablename__ = "attendance"

    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(String, ForeignKey("employees.employee_id"), index=True)
    date = Column(Date)
    status = Column(String)

    __table_args__ = (
        Index("ix_attendance_employee_date", "employee_id", "date"),
    )
