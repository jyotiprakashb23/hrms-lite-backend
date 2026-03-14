# hrms-lite-backend
# HRMS Lite Backend

## Project Overview

HRMS Lite is a lightweight Human Resource Management System designed to simulate basic internal HR operations.
This backend application provides RESTful APIs that allow an administrator to manage employee records and track daily attendance.

The project focuses on implementing clean API design, proper validation, structured backend architecture, and persistent storage using a relational database.

---

## Tech Stack Used

### Backend

* Python
* FastAPI
* SQLAlchemy

### Database

* PostgreSQL (Neon)

### Additional Tools

* Pydantic – Data validation
* Uvicorn – ASGI server
* python-dotenv – Environment variable management
* Email-validator – Email format validation

---

## Features

### Employee Management

* Add a new employee
* Automatically generate a unique Employee ID
* View all employees
* Delete an employee
* Prevent duplicate employees using email validation

### Attendance Management

* Mark attendance for an employee
* Attendance status supports **Present** and **Absent**
* View attendance records for a specific employee
* Prevent duplicate attendance for the same employee on the same date
* Ensure attendance can only be recorded for existing employees

### Validation & Error Handling

* Request validation using Pydantic
* Email format validation
* Proper HTTP status codes
* Meaningful error messages
* Prevention of invalid or duplicate data entries

---

## Project Structure

```
hrms-lite-backend/
│
├── main.py            # FastAPI application entry point
├── database.py        # Database connection setup
├── models.py          # SQLAlchemy ORM models
├── schemas.py         # Pydantic schemas for request and response validation
├── crud.py            # Database operation logic
├── requirements.txt   # Project dependencies
└── README.md
```

---

## API Documentation

Once the application is running, interactive API documentation is available at:

```
http://127.0.0.1:8000/docs
```

Swagger UI allows you to explore and test all available API endpoints.

---

## Steps to Run the Project Locally

### 1. Clone the Repository

```
git clone https://github.com/your-username/hrms-lite-backend.git
cd hrms-lite-backend
```

---

### 2. Create a Virtual Environment

```
python -m venv .venv
```

Activate the virtual environment.

**Mac/Linux**

```
source .venv/bin/activate
```

**Windows**

```
.venv\Scripts\activate
```

---

### 3. Install Dependencies

```
pip install -r requirements.txt
```

---

### 4. Configure Environment Variables

Create a `.env` file in the project root.

Example:

```
DATABASE_URL=your_postgresql_connection_string
```

---

### 5. Run the Application

```
uvicorn main:app --reload
```

---

### 6. Access the API

Open the browser and navigate to:

```
http://127.0.0.1:8000/docs
```

This will open the Swagger API documentation interface.

---

## Assumptions / Limitations

* The system assumes a single administrator managing employee records.
* Authentication and authorization are not implemented in this version.
* Attendance status is limited to two values: **Present** and **Absent**.
* The application focuses primarily on backend API functionality.
* Pagination and advanced filtering are not implemented for employee or attendance lists.

---

## Possible Future Improvements

* Add authentication and role-based access control
* Implement a full React frontend dashboard
* Introduce database migrations using Alembic
* Add pagination and search functionality
* Improve logging and monitoring for production environments
