from sqlalchemy.orm import Session
from sqlalchemy import text
from typing import List, Optional

def get_books(db: Session, book_id: Optional[List[int]] = None, language: Optional[List[str]] = None,
              mime_type: Optional[List[str]] = None, topic: Optional[List[str]] = None,
              author: Optional[str] = None, title: Optional[str] = None, 
              page: int = 1, items_per_page: int = 25):
    
    offset = (page - 1) * items_per_page
    query = """
    SELECT b.id, b.title, a.name as author_name, a.birth_year, a.death_year,
           bl.code, b.download_count,
           array_agg(DISTINCT s.name) as subjects,
           array_agg(DISTINCT bs.name) as bookshelves,
           json_agg(json_build_object('mime_type', f.mime_type, 'url', f.url)) as download_links
    FROM books_book b
    JOIN books_author a ON b.id = a.id
    LEFT JOIN books_subject bs ON b.id = bs.id
    LEFT JOIN books_bookshelf bb ON b.id = bb.id
    LEFT JOIN books_format f ON b.id = f.id
	LEFT JOIN books_book_languages bbl on b.id = bbl.id
	LEFT JOIN books_language bl on bbl.id = bl.id
    WHERE 1=1
    """
    params = {}

    if book_id:
        query += " AND b.id = ANY(:book_id)"
        params["book_id"] = book_id
    if language:
        query += " AND b.language = ANY(:language)"
        params["language"] = language
    if mime_type:
        query += " AND f.mime_type = ANY(:mime_type)"
        params["mime_type"] = mime_type
    if topic:
        query += " AND (s.name ILIKE ANY(:topic) OR bs.name ILIKE ANY(:topic))"
        params["topic"] = [f"%{t}%" for t in topic]
    if author:
        query += " AND a.name ILIKE :author"
        params["author"] = f"%{author}%"
    if title:
        query += " AND b.title ILIKE :title"
        params["title"] = f"%{title}%"

    query += """
    GROUP BY b.id, b.title, a.name, a.birth_year, a.death_year, b.language, b.download_count
    ORDER BY b.download_count DESC
    LIMIT :limit OFFSET :offset
    """
    params["limit"] = items_per_page
    params["offset"] = offset

    result = db.execute(text(query), params)
    books = result.fetchall()

    count_query = f"SELECT COUNT(*) FROM ({query}) as subquery"
    total_books = db.execute(text(count_query), params).scalar()

    return books, total_books