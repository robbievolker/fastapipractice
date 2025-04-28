from typing import Optional
from fastapi import FastAPI, Path, Query, HTTPException
from pydantic import BaseModel, Field
from starlette import status

app = FastAPI()

class Book:
    id: int
    title: str
    author: str
    description: str
    rating: int
    published_date: int
    
    def __init__(self, id, title, author, description, rating, published_date):
        self.id = id
        self.title = title
        self.author = author
        self.description = description
        self.rating = rating
        self.published_date = published_date
        

class BookRequest(BaseModel):
    id: Optional[int] = Field(description="The ID of the book is not needed on creation", default=None)
    title: str = Field(min_length=3)
    author: str = Field(min_length=1)
    description: str = Field(min_length=5, max_length=100)
    rating: int = Field(gt=0, lt=6)
    published_date: int 
    
    model_config = {
        "json_schema_extra": {
            "example": {
                "title": "A new book",
                "author": "rob",
                "description": "A new description of a book",
                "rating": 5
                
            }
        }
    }

BOOKS = [
    Book(1, 'Computer Science Pro', 'codingwithroby', 'A very nice book!', 5, 2012),
    Book(2, 'Be Fast with FastAPI', 'codingwithroby', 'A great book!', 5, 2022),
    Book(3, 'Master Endpoints', 'codingwithroby', 'A awesome book!', 5, 2023),
    Book(4, 'HP1', 'Author 1', 'Book Description', 2, 2023),
    Book(5, 'HP2', 'Author 2', 'Book Description', 3, 2022),
    Book(6, 'HP3', 'Author 3', 'Book Description', 1, 2022)
]


#Helper function for generating ids for books.
def gen_book_id(book: Book):
    if len(BOOKS) > 0:
        book.id = BOOKS[-1].id + 1
    else:
        book.id = 1
    return book


@app.get("/books", status_code=status.HTTP_200_OK)
async def get_all_books():
    return BOOKS

@app.post("/create_book", status_code=status.HTTP_201_CREATED)
async def create_book(book_request: BookRequest):
    new_book = Book(**book_request.model_dump())
    BOOKS.append(gen_book_id(book_request))
    
#Note the use of Path() to add additional validation for Path parameters. 
@app.get("/books/{book_id}", status_code=status.HTTP_200_OK)
async def get_book(book_id: int = Path(gt=0)):
    for book in BOOKS:
        if book.id == book_id:
            return book
    raise HTTPException(status_code=404, detail="Book could not be found in the system!") #To raise the HTTPException. 
        

@app.get("/books/year/", status_code=status.HTTP_200_OK)
async def get_book_by_year(year: int = Query(gt=1600, lt=2026)):
    books_to_return = []
    for book in BOOKS:
        if book.published_date == year:
            books_to_return.append(book)
    return books_to_return


@app.get("/books/", status_code=status.HTTP_200_OK)
async def get_book_by_rating(book_rating: int = Query(gt=0, lt=6)):
    books_to_return = []
    for book in BOOKS:
        if book.rating == book_rating:
            books_to_return.append(book)
    return books_to_return


@app.put("/books/update_book", status_code=status.HTTP_204_NO_CONTENT)
async def update_book(book: BookRequest):
    for i in range(len(BOOKS)):
        if BOOKS[i].id == book.id:
            BOOKS[i] = book
            break
    raise HTTPException(status_code=404, detail="Book could not be found")
    

@app.delete("/books/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(book_id: int = Path(gt=0)):
    for i in range(len(BOOKS)):
        if BOOKS[i].id == book_id:
            BOOKS.pop(i)
            break
    raise HTTPException(status_code=404, detail="Book could not be found")
