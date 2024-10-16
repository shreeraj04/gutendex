from pydantic import BaseModel
from typing import List, Optional

class Author(BaseModel):
    name: str
    birth_year: Optional[int]
    death_year: Optional[int]

class DownloadLink(BaseModel):
    mime_type: str
    url: str

class Book(BaseModel):
    id: int
    title: str
    author: Author
    language: str
    subjects: List[str]
    bookshelves: List[str]
    download_links: List[DownloadLink]

class BookResponse(BaseModel):
    total_books: int
    books: List[Book]
    next_page: Optional[int]