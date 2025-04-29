from unittest.mock import MagicMock
from fastapi.testclient import TestClient

from api.tests.conftest import *


@pytest.fixture
def create_mock_book(client: TestClient, monkeypatch):
    mock_generate_story = MagicMock()
    monkeypatch.setattr("api.routers.books.generate_story", mock_generate_story)
    book_data = {
        "title": "Mock Book",
        "author": "Mock Author",
        "genre": "Fiction",
        "year_published": 2023
    }
    create_book_response = client.post("/books/", json=book_data)
    return create_book_response.json()["id"]


def test_get_reviews_book_not_found(session: Session, client: TestClient):
    # Attempt to retrieve reviews for a non-existent book
    response = client.get("/books/999/reviews/")
    assert response.status_code == 404
    assert response.json()["detail"] == "Book not found"


def test_get_reviews_success(session: Session, client: TestClient, create_mock_book):
    # create a book and add reviews for it, check if they are retrieved correctly
    book_id = create_mock_book

    # Add reviews for the book
    review_1 = {"user_id": 1, "review_text": "Great book!", "rating": 5}
    review_2 = {"user_id": 2, "review_text": "Not bad.", "rating": 3}
    client.post(f"/books/{book_id}/reviews/", json=review_1)
    client.post(f"/books/{book_id}/reviews/", json=review_2)

    # Retrieve reviews for the book
    response = client.get(f"/books/{book_id}/reviews/")
    data = response.json()

    assert response.status_code == 200
    assert isinstance(data, list)
    assert len(data) == 2
    assert data[0]["review_text"] == "Great book!"
    assert data[1]["review_text"] == "Not bad."


def test_create_or_update_review_create(client: TestClient, session: Session, create_mock_book):
    # Create a new review for an existing book and check if it is created correctly
    book_id = create_mock_book

    review_data = {
        "user_id": 3,
        "rating": 4,
        "review_text": "Awesome book!"
    }
    response = client.post(f"/books/{book_id}/reviews/", json=review_data)
    data = response.json()
    assert response.status_code == 200
    assert data["review_text"] == "Awesome book!"
    assert data["rating"] == 4


def test_create_or_update_review_update(client: TestClient, session: Session, create_mock_book):
    # Update an existing review for a user and book, check if it updates correctly
    book_id = create_mock_book

    review_data = {
        "user_id": 3,
        "rating": 5,
        "review_text": "Double Awesome book!"
    }
    response = client.post(f"/books/{book_id}/reviews/", json=review_data)
    data = response.json()
    assert response.status_code == 200
    assert data["review_text"] == "Double Awesome book!"
    assert data["rating"] == 5


def test_create_or_update_review_book_not_found(client: TestClient, session: Session):
    # Add review for a non-existent book and check for 404 error
    review_data = {
        "user_id": 1,
        "rating": 5,
        "review_text": "Great book!"
    }
    response = client.post("/books/999/reviews/", json=review_data)
    assert response.status_code == 404
    assert response.json()["detail"] == "Book not found"


def test_get_reviews_for_existing_book(client: TestClient, session: Session, create_mock_book):
    # Add reviews for the book
    book_id = create_mock_book
    review_1 = {"user_id": 1, "review_text": "Great book!", "rating": 5}
    review_2 = {"user_id": 2, "review_text": "Not bad.", "rating": 3}
    client.post(f"/books/{book_id}/reviews/", json=review_1)
    client.post(f"/books/{book_id}/reviews/", json=review_2)

    # Retrieve reviews for the book
    response = client.get(f"/books/{book_id}/reviews/")
    data = response.json()

    assert response.status_code == 200
    assert isinstance(data, list)
    assert len(data) == 2
