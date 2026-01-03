from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List


server = FastAPI()


students_db = [
    {
        "student_id": 1,
        "roll_no": "CS-101",
        "name": "Ali Khan",
        "age": 20,
        "department": "Computer Science",
        "semester": 4,
        "cgpa": 3.45,
    },
    {
        "student_id": 2,
        "roll_no": "CS-102",
        "name": "Sara Ahmed",
        "age": 21,
        "department": "Computer Science",
        "semester": 5,
        "cgpa": 3.78,
    },
    {
        "student_id": 3,
        "roll_no": "SE-201",
        "name": "Usman Raza",
        "age": 22,
        "department": "Software Engineering",
        "semester": 6,
        "cgpa": 3.12,
    },
    {
        "student_id": 4,
        "roll_no": "IT-301",
        "name": "Ayesha Malik",
        "age": 19,
        "department": "Information Technology",
        "semester": 3,
        "cgpa": 3.90,
    },
    {
        "student_id": 5,
        "roll_no": "CS-103",
        "name": "Hassan Ali",
        "age": 20,
        "department": "Computer Science",
        "semester": 4,
        "cgpa": 2.98,
    },
]


class Student(BaseModel):
    student_id: int
    roll_no: str
    name: str
    age: int
    department: str
    semester: int
    cgpa: float


@server.get("/students", response_model=List[Student])
async def get_all_students():
    return students_db


@server.post("/students")
async def create_student(student_data: Student):
    # LOOP STUDENTS DB
    for student in students_db:
        # CHECK IF STUDENT ID ALREADY EXISTS
        if student["student_id"] == student_data.student_id:
            raise HTTPException(
                status_code=400, detail={"message": "Student ID already exists!"}
            )

        # CHECK IF ROLL NUMBER ALREADY EXISTS
        if student["roll_no"].lower() == student_data.roll_no.lower():
            raise HTTPException(
                status_code=400, detail={"message": "Roll number already exists!"}
            )

    students_db.append(student_data.model_dump())
    return {"message": "Student added successfully"}
