from fastapi import FastAPI, Body
from pydantic import BaseModel


app = FastAPI()


BOOKS = [
    {'title': 'Title One', 'author': 'Author One', 'category': 'science'},
    {'title': 'Title Two', 'author': 'Author Two', 'category': 'science'},
    {'title': 'Title Three', 'author': 'Author Three', 'category': 'history'},
    {'title': 'Title Four', 'author': 'Author Four', 'category': 'math'},
    {'title': 'Title Five', 'author': 'Author Five', 'category': 'math'},
    {'title': 'Title Six', 'author': 'Author Two', 'category': 'math'}
]

class Book(BaseModel):
    title: str
    author: str
    category: str


@app.get("/books")
async def get_all_books():
    return BOOKS


@app.get("/books/")
async def get_books(category: str):
    books_to_return = []
    for book in BOOKS:
        if book['category'].casefold() == category.casefold():
            books_to_return.append(book)
    return {"message" : books_to_return}


@app.get("/books/{author}/")
async def get_books_by_author_category(category: str, author: str):
    books_to_return = []
    for book in BOOKS:
        if book['category'].casefold() == category.casefold() and book['author'].casefold() == author.casefold():
            books_to_return.append(book)
    return {"message" : books_to_return}


@app.get("/books/{book_title}")
async def get_book(book_title: str):
    for book in BOOKS:
        if book['title'].casefold() == book_title.casefold():
            return {"message" : book}
    return {"message" : "Book not found!"}


@app.post("/books/create_book")
async def create_book(new_book=Body()):
    BOOKS.append(new_book)

@app.put("/books/update_book")
async def update_book(new_book=Body()):
    for i in range(len(BOOKS)):
        if BOOKS[i]['title'].casefold() == new_book['title'].casefold() and \
            BOOKS[i]['author'].casefold() == new_book['author'].casefold():
                BOOKS[i] = new_book
    
@app.delete("/books/delete_book/{book_title}")
async def delete_book(book_title: str):
    for i in range(len(BOOKS)):
        if BOOKS[i]['title'].casefold() == book_title.casefold():
            BOOKS.pop(i)
            break 