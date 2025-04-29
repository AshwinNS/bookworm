from fastapi.testclient import TestClient

from api.tests.conftest import *


def test_validate_token_invalid_user(client: TestClient, mock_user):
    """
    Test case for validating token with an invalid user.
    This test ensures that when a request is made to the `/validate_token` endpoint
    with an invalid token or a non-existent user, the API responds with a 401 status
    code and an appropriate error message.
    Assertions:
        - The response status code is 401 (Unauthorized).
        - The response JSON contains the error message "Invalid token or user not found."
    """
    
    response = client.get("/validate_token", headers={"Authorization": "Bearer mock::token"})
    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid token or user not found."


def test_token_format(client: TestClient):
    """
    Tests the token format validation endpoint.
    This test sends a GET request to the `/validate_token` endpoint with an
    invalid token format in the `Authorization` header. It verifies that the
    response status code is 401 (Unauthorized) and that the response JSON
    contains the appropriate error message indicating the expected token format.
    Assertions:
        - The response status code is 401.
        - The response JSON contains the error message "Invalid token format. Expected 'username::token'".
    """
    
    response = client.get("/validate_token", headers={"Authorization": "Bearer mock_token"})
    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid token format. Expected 'username::token'"


def test_validate_token_valid_user(client: TestClient, mock_user):
    """
    Test the `/validate_token` endpoint for a valid user.
    This test verifies that when a valid user with a valid authentication token
    makes a GET request to the `/validate_token` endpoint, the server responds
    with a 200 status code and a confirmation message indicating that the token
    is valid.
    Assertions:
        - The response status code is 200.
        - The response JSON contains a message confirming the token's validity.
    """
    
    response = client.get("/validate_token",
                          headers={"Authorization": f"Bearer {mock_user.auth_token}"}
                          )
    assert response.status_code == 200
    assert response.json() == f"{mock_user.username}, Your token is valid."


def test_get_users(client: TestClient):
    """
    Test the retrieval of users via the GET /users endpoint.

    This test ensures that the endpoint returns a 200 status code and that the
    response body is a list, indicating successful retrieval of user data.
    Assertions:
        - The response status code is 200.
        - The response JSON is of type list.
    """
    response = client.get("/users")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_create_user(client: TestClient):
    """
    Test the user creation endpoint.
    This test verifies that a user can be successfully created by sending a POST request
    to the `/user` endpoint with the required user data. It checks that the response
    status code is 200 and that the returned JSON contains the correct username.
    Assertions:
        - The response status code is 200.
        - The response JSON contains the correct username.
    """

    user_data = {"username": "test_user"}
    response = client.post("/user", json=user_data)
    assert response.status_code == 200
    assert response.json()["username"] == "test_user"


def test_create_user_duplicate(client: TestClient):
    """
    Test case for creating a duplicate user.
    This test ensures that attempting to create a user with a username
    that already exists results in a 400 Bad Request response with the
    appropriate error message.
    Steps:
    1. Create a user with a specific username.
    2. Attempt to create another user with the same username.
    3. Verify that the response status code is 400.
    4. Verify that the response contains the error message "User already exists."
    """
    user_data = {"username": "test_user"}
    client.post("/user", json=user_data)  # Create user first
    response = client.post("/user", json=user_data)  # Attempt duplicate creation
    assert response.status_code == 400
    assert response.json()["detail"] == "User already exists."


def test_get_token(client: TestClient):
    """
    Test the functionality of retrieving an authentication token for a user.
    This test performs the following steps:
    1. Creates a new user by sending a POST request to the "/user" endpoint.
    2. Sends a GET request to the "/get_token/{username}" endpoint to retrieve the authentication token.
    3. Asserts that the response status code is 200 (OK).
    4. Asserts that the response JSON contains the key "auth_token".
    Raises:
        AssertionError: If the response status code is not 200 or the "auth_token" key is missing in the response.
    """
    user_data = {"username": "test_user"}
    client.post("/user", json=user_data)  # Create user first
    response = client.get(f"/get_token/{user_data['username']}")
    assert response.status_code == 200
    assert "auth_token" in response.json()


def test_get_token_user_not_found(client: TestClient):
    """
    Test case for the `/get_token/{username}` endpoint when the specified user does not exist.
    This test verifies that the API returns a 404 status code and the appropriate error message
    when attempting to retrieve a token for a non-existent user.
    Assertions:
        - The response status code is 404.
        - The response JSON contains a "detail" field with the value "User not found."
    """
    response = client.get("/get_token/non_existent_user")
    assert response.status_code == 404
    assert response.json()["detail"] == "User not found."
