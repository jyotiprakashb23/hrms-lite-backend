from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
import models, schemas, crud
from database import SessionLocal, engine, Base
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Add employee
@app.post("/employees", response_model=schemas.EmployeeResponse, status_code=201)
def add_employee(employee: schemas.EmployeeCreate, db: Session = Depends(get_db)):

    new_employee = crud.create_employee(db, employee)

    # if not new_employee:
    #     raise HTTPException(status_code=400, detail="Employee already exists")

    return new_employee


# List employees
@app.get("/employees")
def list_employees(db: Session = Depends(get_db)):

    return crud.get_employees(db)


# Delete employee
@app.delete("/employees/{employee_id}")
def remove_employee(employee_id: str, db: Session = Depends(get_db)):

    employee = crud.delete_employee(db, employee_id)

    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")

    return {"message": "Employee deleted"}


# Mark attendance
@app.post("/attendance")
def mark_attendance(attendance: schemas.AttendanceCreate, db: Session = Depends(get_db)):

    return crud.mark_attendance(db, attendance)


# Get attendance for employee
@app.get("/attendance/{employee_id}")
def view_attendance(employee_id: str, db: Session = Depends(get_db)):

    return crud.get_attendance(db, employee_id)