from fastapi import Body, FastAPI, Response

app = FastAPI(title="Books RestAPI")

BOOKS = [
    {
        "title": "Python Crash Course",
        "author": "Eric Matthes",
        "category": "Programming"
    },
    {
        "title": "Automate the Boring Stuff with Python",
        "author": "Al Sweigart",
        "category": "Automation"
    },
    {
        "title": "Fluent Python",
        "author": "Luciano Ramalho",
        "category": "Advanced Programming"
    },
    {
        "title": "Effective Python",
        "author": "Brett Slatkin",
        "category": "Best Practices"
    },
    {
        "title": "Python for Data Analysis",
        "author": "Wes McKinney",
        "category": "Data Science"
    },
    {
        "title": "Learning Python",
        "author": "Mark Lutz",
        "category": "Programming Basics"
    }
]


@app.get("/all-books")
async def get_all_books():
    return BOOKS

@app.get("/book/{author}")
async def get_book(author: str):
    for book in BOOKS:
        if book.get('author').casefold() == author.casefold():
            return {"book": book}
        
@app.get("/books/")
async def get_book_by_category(category: str):
    for book in BOOKS:
        if book.get('category').casefold() == category.casefold():
            return {"book": book}

@app.post("/books/create")
async def create_book(new_book=Body()):
    BOOKS.append(new_book)
    return Response(status_code=201, content="Book created successfully")


@app.put("/books/update")
async def update_book(book_data=Body()):
    for i in range(len(BOOKS)):
        if BOOKS[i].get('title').casefold() == book_data.get('title').casefold():
            BOOKS[i] = book_data

@app.delete("/books/delete/{author}")
async def delete_book(author: str):
    for i in range(len(BOOKS)):
        if BOOKS[i].get('author').casefold() == author.casefold():
            BOOKS.pop(i)
            break
