from models.book import Book
from db.db import BOOKS

# Fucntion that helps to set and id
def find_book_id(book: Book):
    if len(BOOKS) > 0:
        book.id = BOOKS[-1].id + 1
    else:
        book.id = 1

    return book