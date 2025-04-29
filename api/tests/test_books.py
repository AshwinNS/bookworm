from unittest.mock import MagicMock
from fastapi.testclient import TestClient

from api.tests.conftest import *


def test_create_book_with_background_task(session: Session, client: TestClient, monkeypatch):
    """
    Test the creation of a book and the invocation of a background task.
    This test verifies the following:
    1. A book can be successfully created via a POST request to the "/books/" endpoint.
    2. The response contains the correct book details, including title, author, and year published.
    3. A background task (`generate_story`) is called exactly once with the correct arguments.
    """
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


def test_get_books_success(client: TestClient):
    """
    Test the successful retrieval of books from the API.
    This test verifies that a GET request to the "/books/" endpoint
    returns a 200 status code and that the response is a list.
    Assertions:
        - The response status code is 200.
        - The response JSON is of type list.
    """
    response = client.get("/books/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_book_by_id_success(session: Session, client: TestClient, monkeypatch):
    """
    Test the successful retrieval of a book by its ID.
    This test performs the following steps:
    1. Creates a new book entry using the POST endpoint with sample book data.
    2. Extracts the ID of the created book from the response.
    3. Retrieves the book using the GET endpoint with the extracted ID.
    4. Asserts that the response status code is 200 (OK).
    5. Verifies that the retrieved book's details match the original data.
    """
    mock_generate_story = MagicMock()
    monkeypatch.setattr("api.routers.books.generate_story", mock_generate_story)

    book_data = {
        "title": "1984",
        "author": "Deepa Nishant",
        "genre": "Science Fiction",
        "year_published": 1949
    }
    create_response = client.post("/books/", json=book_data)
    book_id = create_response.json()["id"]
    mock_generate_story.assert_called_once_with(book_id, session)

    # Retrieve the book by ID
    response = client.get(f"/books/{book_id}")
    data = response.json()

    assert response.status_code == 200
    assert data["title"] == "1984"
    assert data["author"] == "Deepa Nishant"
    assert data["year_published"] == 1949


def test_get_book_by_id_not_found(client: TestClient):
    """
    Test case for retrieving a book by an ID that does not exist.
    This test ensures that when a GET request is made to the `/books/{id}` endpoint
    with a non-existent book ID, the API responds with a 404 status code and an
    appropriate error message.
    Assertions:
        - The response status code is 404.
        - The response JSON contains a "detail" field with the value "Book not found".
    """
    response = client.get("/books/9999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Book not found"


def test_admin_update_book_success(session: Session, client: TestClient, mock_admin_user, monkeypatch):
    """
    Test case for successfully updating a book as an admin user.

    This test verifies that an admin user can update the details of an existing book
    using the PUT endpoint. It ensures that the response status code is 200 and the
    updated book data reflects the changes.
    Steps:
    1. Create a new book using the POST endpoint and retrieve its ID.
    2. Update the book's title using the PUT endpoint with the admin user's authorization token.
    3. Assert that the response status code is 200.
    4. Assert that the updated book's title matches the new value.
    """
    mock_generate_story = MagicMock()
    monkeypatch.setattr("api.routers.books.generate_story", mock_generate_story)

    book_data = {
        "title": "Aarachar",
        "author": "Kamala Das",
        "genre": "Fiction",
        "year_published": 1960
    }
    create_response = client.post("/books/", json=book_data)
    book_id = create_response.json()["id"]
    mock_generate_story.assert_called_once_with(book_id, session)

    # Update the book
    updated_data = {
        "title": "Aarachar (Updated)"
    }
    response = client.put(
        f"/books/{book_id}",
        json=updated_data,
        headers={"Authorization": f"Bearer {mock_admin_user.auth_token}"}
    )
    data = response.json()

    assert response.status_code == 200
    assert data["title"] == "Aarachar (Updated)"


def test_user_update_book_failure(session: Session, client: TestClient, mock_user, monkeypatch):
    """
    Test case for updating a book with insufficient permissions.

    This test verifies that a user without the necessary permissions cannot update a book's details. 
    It ensures that the API returns a 403 Forbidden status code and an appropriate error message.
    Steps:
    1. Create a book using the API to set up the test scenario.
    2. Attempt to update the book's title using the mock user's credentials.
    3. Assert that the response status code is 403 (Forbidden).
    4. Assert that the response contains the correct error message indicating insufficient permissions.
    """
    mock_generate_story = MagicMock()
    monkeypatch.setattr("api.routers.books.generate_story", mock_generate_story)
    # Create a book to test update
    book_data = {
        "title": "Aarachar",
        "author": "Kamala Das",
        "genre": "Fiction",
        "year_published": 1960
    }
    create_response = client.post("/books/", json=book_data)
    book_id = create_response.json()["id"]
    mock_generate_story.assert_called_once_with(book_id, session)

    # Update the book
    updated_data = {
        "title": "Aarachar (Updated)"
    }
    response = client.put(
        f"/books/{book_id}",
        json=updated_data,
        headers={"Authorization": f"Bearer {mock_user.auth_token}"}
    )

    assert response.status_code == 403
    assert response.json()["detail"] == f"You do not have permission to update this book."


def test_update_book_not_found(client: TestClient, mock_admin_user):
    """
    Test case for updating a book that does not exist in the database.
    This test ensures that when a PUT request is made to update a book with an ID
    that does not exist, the API responds with a 404 status code and an appropriate
    error message.
    Assertions:
        - The response status code is 404.
        - The response JSON contains a "detail" field with the value "Book not found".
    """

    updated_data = {
        "title": "Nonexistent Book",
        "author": "Unknown",
        "genre": "Fiction",
        "year_published": 2000
    }
    response = client.put("/books/9999",
                         json=updated_data,
                         headers={"Authorization": f"Bearer {mock_admin_user.auth_token}"})
    assert response.status_code == 404
    assert response.json()["detail"] == "Book not found"


def test_admin_delete_book_success(session: Session, client: TestClient, mock_admin_user, monkeypatch):
    """
    Test case for successfully deleting a book as an admin user.
    This test verifies that an admin user can delete a book from the system
    using the DELETE endpoint. It ensures that the book is created first,
    then deleted successfully, and the appropriate response is returned.
    Steps:
    1. Create a book using the POST /books/ endpoint.
    2. Extract the book ID from the response.
    3. Send a DELETE request to /books/{book_id} with admin authorization.
    4. Assert that the response status code is 200.
    5. Assert that the response message confirms successful deletion of the book.
    """
    mock_generate_story = MagicMock()
    monkeypatch.setattr("api.routers.books.generate_story", mock_generate_story)

    book_data = {
        "title": "The Catcher in the Rye",
        "author": "J.D. Salinger",
        "genre": "Fiction",
        "year_published": 1951
    }
    create_response = client.post("/books/", json=book_data)
    book_id = create_response.json()["id"]
    mock_generate_story.assert_called_once_with(book_id, session)

    # Delete the book
    response = client.delete(
                    f"/books/{book_id}",
                    headers={"Authorization": f"Bearer {mock_admin_user.auth_token}"}
                )
    assert response.status_code == 200
    assert response.json() == f"Book with ID {book_id} has been deleted successfully."


def test_user_delete_book_failure(session: Session, client: TestClient, mock_user, monkeypatch):
    """
    Test case for attempting to delete a book without proper permissions.
    This test verifies that a user without the necessary permissions cannot delete a book.
    It ensures that the API returns a 403 Forbidden status code and an appropriate error
    message when the deletion is attempted.
    Steps:
    1. Create a book using the POST /books/ endpoint.
    2. Attempt to delete the created book using the DELETE /books/{book_id} endpoint
       with the mock user's authentication token.
    3. Assert that the response status code is 403.
    4. Assert that the response contains the expected error message.
    Expected Result:
    The API should return a 403 status code and a "You do not have permission to delete this book."
    error message.
    """
    mock_generate_story = MagicMock()
    monkeypatch.setattr("api.routers.books.generate_story", mock_generate_story)

    book_data = {
        "title": "The Catcher in the Rye",
        "author": "J.D. Salinger",
        "genre": "Fiction",
        "year_published": 1951
    }
    create_response = client.post("/books/", json=book_data)
    book_id = create_response.json()["id"]
    mock_generate_story.assert_called_once_with(book_id, session)

    # Delete the book
    response = client.delete(
                    f"/books/{book_id}",
                    headers={"Authorization": f"Bearer {mock_user.auth_token}"}
                )
    assert response.status_code == 403
    assert response.json()["detail"] == "You do not have permission to delete this book."


def test_delete_book_not_found(client: TestClient, mock_admin_user):
    """
    Test case for attempting to delete a book that does not exist.
    This test verifies that the API returns a 404 status code and the appropriate error message
    when a DELETE request is made for a book ID that does not exist in the database.
    Assertions:
        - The response status code is 404.
        - The response JSON contains a "detail" field with the value "Book not found".
    """
    
    response = client.delete("/books/9999",
                                headers={"Authorization": f"Bearer {mock_admin_user.auth_token}"})
    assert response.status_code == 404
    assert response.json()["detail"] == "Book not found"
