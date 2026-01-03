from fastapi import FastAPI, HTTPException, status
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


class UpdateStudentModel(BaseModel):
    name: str
    age: int
    semester: int
    cgpa: float


# GET ALL STUDENTS
@server.get("/students", response_model=List[Student])
async def get_all_students():
    return students_db


# CREATE STUDENT
@server.post("/students", status_code=status.HTTP_201_CREATED)
async def create_student(student_data: Student) -> list:
    new_student = student_data.model_dump()
    # LOOP STUDENTS DB
    for student in students_db:
        # CHECK IF STUDENT ID ALREADY EXISTS
        if student["student_id"] == new_student["student_id"]:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail={"message": "Student ID already exists!"},
            )

        # CHECK IF ROLL NUMBER ALREADY EXISTS
        if student["roll_no"].lower() == new_student["roll_no"].lower():
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail={"message": "Roll number already exists!"},
            )

    students_db.append(new_student)
    return {"message": "Student added successfully"}


# GET STUDENT BY ID
@server.get("/students/{student_id}")
async def get_student(student_id: int) -> dict:
    for student in students_db:
        if student_id == student["student_id"]:
            return student

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail={"message": "Student not found."},
    )


# UPDATE STUDENT RECORD
@server.patch("/students/{student_id}")
async def update_student_record(
    student_id: int, student_update_data: UpdateStudentModel
) -> dict:
    new_student_data = student_update_data.model_dump()
    for student in students_db:
        if student["student_id"] == student_id:
            for key, value in new_student_data.items():
                student[key] = value

            return {
                "message": "Student info updated successfully",
                "student_info": student,
            }

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail={"message": "Student not found."}
    )


# DELETE STUDENT RECORD
@server.delete("/student/{student_id}", status_code=status.HTTP_200_OK)
async def delete_student(student_id: int) -> dict:
    for index, student in enumerate(students_db):
        if student["student_id"] == student_id:
            # 👇🏻 This also removes the student from student's list
            students_db.remove(student)
            # removed_student = students_db.pop(index)
            return {
                "message": "Student's record deleted successfully.",
                # "student_info": removed_student,
            }

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail={"message": "Student not found."}
    )
