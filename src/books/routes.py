from fastapi import APIRouter, status, HTTPException
from src.books.schemas import Book, BookUpdateModel
from src.books.book_data import books_db
from typing import List

book_router = APIRouter()


# GET ALL BOOKS
@book_router.get("/", response_model=List[Book])
async def get_all_books():
    return books_db


# CREATE BOOK
@book_router.post("/", status_code=status.HTTP_201_CREATED)
async def create_book(book_data: Book) -> dict:
    new_book = book_data.model_dump()

    # CHECK IF BOOK ID ALREADY EXISTS
    for book in books_db:
        if book["id"] == new_book["id"]:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail={"message": "Book ID already exists!"},
            )

    books_db.append(new_book)
    return {"message": "Book added successfully"}


# GET BOOK BY ID
@book_router.get("/{book_id}")
async def get_book(book_id: int) -> dict:
    for book in books_db:
        if book_id == book["id"]:
            return book

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail={"message": "Book not found."},
    )


# UPDATE BOOK RECORD
@book_router.patch("/{book_id}")
async def update_book_record(book_id: int, book_update_data: BookUpdateModel) -> dict:
    new_book_data = book_update_data.model_dump()
    for book in books_db:
        if book["id"] == book_id:
            for key, value in new_book_data.items():
                book[key] = value

            return {
                "message": "Book info updated successfully",
                "book_info": book,
            }

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail={"message": "Book not found."}
    )


# DELETE BOOK RECORD
@book_router.delete("/{book_id}", status_code=status.HTTP_200_OK)
async def delete_book(book_id: int) -> dict:
    for book in books_db:
        if book["id"] == book_id:
            books_db.remove(book)
            return {
                "message": "Book's record deleted successfully.",
            }

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail={"message": "Book not found."}
    )
