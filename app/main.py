from fastapi import FastAPI, Depends, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from database import get_db
from models import Book, BookResponse, Author, DownloadLink
from crud import get_books

app = FastAPI(title="Project Gutenberg API", version="1.0.0")

@app.get("/books", response_model=BookResponse)
async def read_books(
    db: Session = Depends(get_db),
    book_id: Optional[List[int]] = Query(None),
    language: Optional[List[str]] = Query(None),
    mime_type: Optional[List[str]] = Query(None),
    topic: Optional[List[str]] = Query(None),
    author: Optional[str] = None,
    title: Optional[str] = None,
    page: int = Query(1, ge=1)
):
    """
    Retrieve books based on filter criteria.
    """
    books, total_books = get_books(db, book_id, language, mime_type, topic, author, title, page)

    book_list = []
    for book in books:
        book_dict = dict(book)
        book_list.append(Book(
            id=book_dict["id"],
            title=book_dict["title"],
            author=Author(
                name=book_dict["author_name"],
                birth_year=book_dict["birth_year"],
                death_year=book_dict["death_year"]
            ),
            language=book_dict["language"],
            subjects=book_dict["subjects"],
            bookshelves=book_dict["bookshelves"],
            download_links=[DownloadLink(**link) for link in book_dict["download_links"]]
        ))

    next_page = page + 1 if len(book_list) == 25 else None

    return BookResponse(
        total_books=total_books,
        books=book_list,
        next_page=next_page
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)