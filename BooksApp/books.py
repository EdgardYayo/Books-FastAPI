from fastapi import FastAPI, Path, Query, HTTPException
from utils.functions import find_book_id
from models.book import Book
from request.book_request import BookRequest
from db.db import BOOKS
from starlette import status

app = FastAPI()

# Query is used to validate query parameters, is used similar that Field
# Path is used to validate path parameters, is used similar that Field

@app.get("/allbooks", status_code=status.HTTP_200_OK)
async def get_all_books():
    return BOOKS

@app.get("/books/{book_id}", status_code=status.HTTP_200_OK)
async def read_book(book_id: int = Path(gt=0)):
    for book in BOOKS:
        if book.id == book_id:
            return book
    raise HTTPException(status_code=404, detail='Book not found')

@app.get("/books/", status_code=status.HTTP_200_OK)
async def read_book_by_rating(book_rating: int = Query(gt=0, lt=6)):
    books_to_return = []
    for book in BOOKS:
        if book.rating == book_rating:
            books_to_return.append(book)
    if len(books_to_return) > 0:
        return books_to_return
    else:
        raise HTTPException(status_code=404, detail='There are no books with that rating')

@app.get("/books_published/{date}", status_code=status.HTTP_200_OK)
async def read_book_by_published_date(date: int = Path(gt=1900)):
    books = []
    for i in range(len(BOOKS)):
        if BOOKS[i].published_date == date:
            books.append(BOOKS[i])
    if len(books) > 0:
        return books
    else:
        raise HTTPException(detail="There is no books published in that date", status_code=404)

@app.post("/create-book", status_code=status.HTTP_201_CREATED)
async def create_book(book_request: BookRequest):
    # This two ** allows to spread the key/value pair in our Book constructor propertly
    new_book = Book(**book_request.model_dump())
    BOOKS.append(find_book_id(new_book))

@app.put("/books/update_book/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_book(book: BookRequest, book_id: int = Path(gt=0)):
    book_found = False
    for i in range(len(BOOKS)):
        if BOOKS[i].id == book_id:
            BOOKS[i] = book
            BOOKS[i].id = book_id
            book_found = True
    if not book_found:
        raise HTTPException(status_code=404, detail='That book does not exist in our database')
            
@app.delete("/books/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(book_id: int = Path(gt=0)):
    book_found = False
    for i in range(len(BOOKS)):
        if BOOKS[i].id == book_id:
            BOOKS.pop(i)
            book_found = True
            break
    if not book_found:
        raise HTTPException(status_code=404, detail='Book not found')