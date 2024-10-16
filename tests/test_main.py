from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_read_books():
    response = client.get("/books")
    assert response.status_code == 200
    assert "total_books" in response.json()
    assert "books" in response.json()
    assert "next_page" in response.json()

def test_read_books_with_filter():
    response = client.get("/books?language=en&topic=Fiction")
    assert response.status_code == 200
    assert "total_books" in response.json()
    assert "books" in response.json()
    assert "next_page" in response.json()