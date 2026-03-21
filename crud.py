from sqlalchemy.orm import Session
from sqlalchemy import exists
import models, schemas
import uuid
import threading
import time
from fastapi import HTTPException

_employees_cache: list | None = None
_cache_timestamp: float = 0.0
_cache_lock = threading.Lock()
_CACHE_TTL = 60  # seconds


def _invalidate_cache():
    global _employees_cache, _cache_timestamp
    with _cache_lock:
        _employees_cache = None
        _cache_timestamp = 0.0


def create_employee(db: Session, employee: schemas.EmployeeCreate):
    existing = (
        db.query(models.Employee)
        .filter(models.Employee.email == employee.email)
        .first()
    )

    if existing:
        raise HTTPException(
            status_code=400, detail="Employee with this email already exists"
        )

    employee_id = "EMP-" + uuid.uuid4().hex[:6].upper()
    db_employee = models.Employee(
        employee_id=employee_id,
        full_name=employee.full_name,
        email=employee.email,
        department=employee.department,
    )

    db.add(db_employee)
    db.commit()
    db.refresh(db_employee)

    _invalidate_cache()

    return db_employee


def get_employees(db: Session, skip: int = 0, limit: int = 100):
    global _employees_cache, _cache_timestamp
    with _cache_lock:
        if _employees_cache is None or (time.time() - _cache_timestamp) >= _CACHE_TTL:
            _employees_cache = db.query(models.Employee).all()
            _cache_timestamp = time.time()
        return _employees_cache[skip: skip + limit]


def delete_employee(db: Session, emp_id: str):
    employee = (
        db.query(models.Employee).filter(models.Employee.employee_id == emp_id).first()
    )

    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")

    db.delete(employee)
    db.commit()

    _invalidate_cache()

    return employee


def mark_attendance(db: Session, attendance: schemas.AttendanceCreate):
    employee_exists = db.query(
        exists().where(models.Employee.employee_id == attendance.employee_id)
    ).scalar()

    if not employee_exists:
        raise HTTPException(status_code=404, detail="Employee not found in the database.")

    duplicate_exists = db.query(
        exists().where(
            models.Attendance.employee_id == attendance.employee_id,
            models.Attendance.date == attendance.date,
        )
    ).scalar()

    if duplicate_exists:
        raise HTTPException(
            status_code=400,
            detail="Attendance already marked for this employee on this date",
        )

    record = models.Attendance(**attendance.model_dump())

    db.add(record)
    db.commit()
    db.refresh(record)

    return record


def get_attendance(db: Session, emp_id: str, skip: int = 0, limit: int = 100):
    return (
        db.query(models.Attendance)
        .filter(models.Attendance.employee_id == emp_id)
        .offset(skip)
        .limit(limit)
        .all()
    )
