from sqlalchemy.orm import Session
import models, schemas
import uuid
from fastapi import HTTPException

_employees_cache: list | None = None


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

    global _employees_cache
    _employees_cache = None

    return db_employee


def get_employees(db: Session):
    global _employees_cache
    if _employees_cache is not None:
        return _employees_cache
    _employees_cache = db.query(models.Employee).all()
    return _employees_cache


def delete_employee(db: Session, emp_id: str):

    employee = (
        db.query(models.Employee).filter(models.Employee.employee_id == emp_id).first()
    )

    if not employee:
        raise HTTPException(status_code=400, detail="Employee not found")

    db.delete(employee)
    db.commit()

    global _employees_cache
    _employees_cache = None

    return employee


def mark_attendance(db: Session, attendance: schemas.AttendanceCreate):

    employee = (
        db.query(models.Employee)
        .filter(models.Employee.employee_id == attendance.employee_id)
        .first()
    )
    existing_attendance = (
        db.query(models.Attendance)
        .filter(
            models.Attendance.employee_id == attendance.employee_id,
            models.Attendance.date == attendance.date,
        )
        .first()
    )

    if existing_attendance:
        raise HTTPException(
            status_code=400,
            detail="Attendance already marked for this employee on this date"
        )

    if not employee:
        raise HTTPException(
            status_code=404, detail="Employee not found in the database."
        )
    record = models.Attendance(**attendance.dict())

    db.add(record)
    db.commit()
    db.refresh(record)

    return record


def get_attendance(db: Session, emp_id: str):

    return (
        db.query(models.Attendance)
        .filter(models.Attendance.employee_id == emp_id)
        .all()
    )
