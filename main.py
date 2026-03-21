import time
import logging
from fastapi import FastAPI, Depends, HTTPException, Request, Response
from sqlalchemy.orm import Session
import models, schemas, crud
from database import SessionLocal, engine, Base
from fastapi.middleware.cors import CORSMiddleware

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger(__name__)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)


@app.middleware("http")
async def log_requests(request: Request, call_next):
    start = time.time()
    response = await call_next(request)
    duration = time.time() - start
    logger.info(f"{request.method} {request.url.path} - {response.status_code} ({duration:.3f}s)")
    return response


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Add employee
@app.post("/employees", response_model=schemas.EmployeeResponse, status_code=201)
def add_employee(employee: schemas.EmployeeCreate, db: Session = Depends(get_db)):
    return crud.create_employee(db, employee)


# List employees
@app.get("/employees")
def list_employees(
    response: Response,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
):
    response.headers["Cache-Control"] = "max-age=30"
    return crud.get_employees(db, skip=skip, limit=limit)


# Delete employee
@app.delete("/employees/{employee_id}")
def remove_employee(employee_id: str, db: Session = Depends(get_db)):
    employee = crud.delete_employee(db, employee_id)
    return {"message": "Employee deleted"}


# Mark attendance
@app.post("/attendance")
def mark_attendance(attendance: schemas.AttendanceCreate, db: Session = Depends(get_db)):
    return crud.mark_attendance(db, attendance)


# Get attendance for employee
@app.get("/attendance/{employee_id}")
def view_attendance(
    employee_id: str,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
):
    return crud.get_attendance(db, employee_id, skip=skip, limit=limit)
