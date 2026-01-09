from fastapi import APIRouter, status, HTTPException, Depends
import sqlmodel.ext.asyncio.session
from src.books.schemas import Book, BookUpdateModel
from src.books.service import BookService
from src.db.main import get_session
from typing import List

book_router = APIRouter()
book_service = BookService()


# GET ALL BOOKS
@book_router.get("/", response_model=List[Book])
async def get_all_books(session: AsyncSession = Depends(get_session)):
    books = await book_service.get_all_books(session)
    return books


# CREATE BOOK
@book_router.post("/", status_code=status.HTTP_201_CREATED, response_model=Book)
async def create_book(
    book_data: Book, session: AsyncSession = Depends(get_session)
) -> dict:
    new_book = book_service.create_book(book_data, session)
    return new_book


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
