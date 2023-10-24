import pytest
from jose import jwt
from app.models.schemas import user_schema

from app.config.env_variables_config import settings


def test_create_user(client):
    res = client.post(
        "/users/", json={"email": "hello123@gmail.com", "password": "password123", "phone_number": "08890123123",
                         "first_name": "string", "last_name": "string"})

    new_user = user_schema.UserOut(**res.json())
    assert new_user.email == "hello123@gmail.com"
    assert res.status_code == 201


def test_login_user(test_user, client):
    res = client.post(
        "/login", data={"username": test_user['email'], "password": test_user['password']})
    login_res = user_schema.Token(**res.json())
    payload = jwt.decode(login_res.access_token,
                         settings.secret_key, algorithms=[settings.algorithm])
    id = payload.get("user_id")
    assert id == test_user['user_id']
    assert login_res.token_type == "bearer"
    assert res.status_code == 200


@pytest.mark.parametrize("email, password, status_code", [
    ('wrongemail@gmail.com', 'password123', 403),
    ('hello123@gmail.com', 'wrongpassword', 403),
    ('wrongemail@gmail.com', 'wrongpassword', 403),
    (None, 'password123', 422),
    ('sanjeev@gmail.com', None, 422)
])
def test_incorrect_login(test_user, client, email, password, status_code):
    res = client.post(
        "/login", data={"username": email, "password": password})

    assert res.status_code == status_code


def test_update_user_invalid_id(authorized_client):
    res = authorized_client.put("/users/999", json={"email": "new_email@example.com"})
    assert res.status_code == 404


# def test_update_user_invalid_email(authorized_client, test_user):
#     res = authorized_client.put(
#         f"/users/{test_user['user_id']}",
#         json={"email": "invalid_email", "password": "new_password123"}
#     )
#     assert res.status_code == 422 

def test_delete_user(authorized_client):
    res = authorized_client.delete("/users/1")
    assert res.status_code == 204


def test_delete_user_invalid_id(authorized_client):
    res = authorized_client.delete("/users/999")
    assert res.status_code == 404  # Expected HTTP 404 Not Found

# # Test case for deleting a user with insufficient permissions
# def test_delete_user_insufficient_permissions(client, test_user):
#     res = client.delete(f"/users/{test_user['user_id']}")
#     assert res.status_code == 403
