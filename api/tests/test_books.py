from unittest.mock import MagicMock
from fastapi.testclient import TestClient

from api.tests.conftest import *


def test_create_book_with_background_task(session: Session, client: TestClient, monkeypatch):
    # Mock the generate_story function to track calls
    mock_generate_story = MagicMock()
    monkeypatch.setattr("api.routers.books.generate_story", mock_generate_story)

    # Create a book
    response = client.post(
        "/books/",
        json={
            "title": "khasakinda Idihasam",
            "author": "OV Vijayan",
            "genre": "Science Fiction",
            "year_published": 1932
        },
    )
    data = response.json()

    assert response.status_code == 200
    assert data["title"] == "khasakinda Idihasam"
    assert data["author"] == "OV Vijayan"
    assert data["year_published"] == 1932

    # Check if the background task was called
    mock_generate_story.assert_called_once_with(data["id"], session)


def test_get_books_success(session: Session, client: TestClient):
    response = client.get("/books/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_book_by_id_success(session: Session, client: TestClient):
    # Create a book to test retrieval
    book_data = {
        "title": "1984",
        "author": "Deepa Nishant",
        "genre": "Sience Fiction",
        "year_published": 1949
    }
    create_response = client.post("/books/", json=book_data)
    book_id = create_response.json()["id"]

    # Retrieve the book by ID
    response = client.get(f"/books/{book_id}")
    data = response.json()

    assert response.status_code == 200
    assert data["title"] == "1984"
    assert data["author"] == "Deepa Nishant"
    assert data["year_published"] == 1949


def test_get_book_by_id_not_found(session: Session, client: TestClient):
    response = client.get("/books/9999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Book not found"


def test_update_book_success(session: Session, client: TestClient):
    # Create a book to test update
    book_data = {
        "title": "Aarachar",
        "author": "Kamala Das",
        "genre": "Fiction",
        "year_published": 1960
    }
    create_response = client.post("/books/", json=book_data)
    book_id = create_response.json()["id"]

    # Update the book
    updated_data = {
        "title": "Aarachar (Updated)",
        "author": "Kamala Das",
        "genre": "Fiction",
        "year_published": 1960
    }
    response = client.put(f"/books/{book_id}", json=updated_data)
    data = response.json()

    assert response.status_code == 200
    assert data["title"] == "Aarachar (Updated)"


def test_update_book_not_found(session: Session, client: TestClient):
    updated_data = {
        "title": "Nonexistent Book",
        "author": "Unknown",
        "genre": "Fiction",
        "year_published": 2000
    }
    response = client.put("/books/9999", json=updated_data)
    assert response.status_code == 404
    assert response.json()["detail"] == "Book not found"


def test_delete_book_success(session: Session, client: TestClient):
    # Create a book to test deletion
    book_data = {
        "title": "The Catcher in the Rye",
        "author": "J.D. Salinger",
        "genre": "Fiction",
        "year_published": 1951
    }
    create_response = client.post("/books/", json=book_data)
    book_id = create_response.json()["id"]

    # Delete the book
    response = client.delete(f"/books/{book_id}")
    assert response.status_code == 200
    assert response.json() == f"Book with ID {book_id} has been deleted successfully."


def test_delete_book_not_found(session: Session, client: TestClient):
        response = client.delete("/books/9999")
        assert response.status_code == 404
        assert response.json()["detail"] == "Book not found"
