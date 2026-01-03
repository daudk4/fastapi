from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
from typing import List

server = FastAPI()

# Books database with static data
books_db = [
    {
        "id": 1,
        "title": "Think Python",
        "author": "Allen B. Downey",
        "publisher": "O'Reilly Media",
        "published_date": "2021-01-01",
        "page_count": 1234,
        "language": "English",
    },
    {
        "id": 2,
        "title": "Clean Code",
        "author": "Robert C. Martin",
        "publisher": "Prentice Hall",
        "published_date": "2008-08-01",
        "page_count": 464,
        "language": "English",
    },
    {
        "id": 3,
        "title": "The Pragmatic Programmer",
        "author": "Andrew Hunt, David Thomas",
        "publisher": "Addison-Wesley",
        "published_date": "2019-09-13",
        "page_count": 352,
        "language": "English",
    },
    {
        "id": 4,
        "title": "Design Patterns: Elements of Reusable Object-Oriented Software",
        "author": "Erich Gamma, Richard Helm, Ralph Johnson, John Vlissides",
        "publisher": "Addison-Wesley",
        "published_date": "1994-10-31",
        "page_count": 395,
        "language": "English",
    },
    {
        "id": 5,
        "title": "Introduction to Algorithms",
        "author": "Thomas H. Cormen, Charles E. Leiserson, Ronald L. Rivest, Clifford Stein",
        "publisher": "MIT Press",
        "published_date": "2009-07-31",
        "page_count": 1312,
        "language": "English",
    },
]


class Book(BaseModel):
    id: int
    title: str
    author: str
    publisher: str
    published_date: str
    page_count: int
    language: str


class BookUpdateModel(BaseModel):
    title: str
    author: str
    publisher: str
    published_date: str
    page_count: int
    language: str


# GET ALL BOOKS
@server.get("/books", response_model=List[Book])
async def get_all_books():
    return books_db


# CREATE BOOK
@server.post("/books", status_code=status.HTTP_201_CREATED)
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
@server.get("/books/{book_id}")
async def get_book(book_id: int) -> dict:
    for book in books_db:
        if book_id == book["id"]:
            return book

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail={"message": "Book not found."},
    )


# UPDATE BOOK RECORD
@server.patch("/books/{book_id}")
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
@server.delete("/books/{book_id}", status_code=status.HTTP_200_OK)
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
