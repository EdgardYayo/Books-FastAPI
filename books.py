from fastapi import FastAPI
from utils.functions import find_book_id
from models.book import Book
from request.book_request import BookRequest
from db.db import BOOKS

app = FastAPI()


@app.get("/allbooks")
async def get_all_books():
    return BOOKS

@app.get("/books/{book_id}")
async def read_book(book_id: int):
    for book in BOOKS:
        if book.id == book_id:
            return book


@app.get("/books/")
async def read_book_by_rating(book_rating: int):
    books_to_return = []
    for book in BOOKS:
        if book.rating == book_rating:
            books_to_return.append(book)
    return books_to_return

@app.post("/create-book")
async def create_book(book_request: BookRequest):
    # This two ** allows to spread the key/value pair in our Book constructor propertly
    new_book = Book(**book_request.model_dump())
    BOOKS.append(find_book_id(new_book))





