import pytest
from jose import jwt
from app.models.schemas import role_schema

from app.config.env_variables_config import settings



# def test_get_all_roles(authorized_client, test_roles):
#     res = authorized_client.get("/posts/")

#     def validate(post):
#         return role_schema.RoleOut(**post)
#     posts_map = map(validate, res.json())
#     posts_list = list(posts_map)

#     assert len(res.json()) == len(test_roles)
#     assert res.status_code == 200



def test_create_role(authorized_client):
    test_role_data = {"role_name":"Admin"}
    res = authorized_client.post("/roles/", json=test_role_data)
    
    new_role = role_schema.RoleOut(**res.json())
    assert new_role.role_name == test_role_data["role_name"]
    assert res.status_code == 201


def test_get_roles_empty(authorized_client):
    res = authorized_client.get("/roles/")
    assert res.status_code == 404


def test_get_roles_after_creating_one(authorized_client):
    # First, create a role
    test_role_data = {"role_name":"Admin"}
    authorized_client.post("/roles/", json=test_role_data)

    # Fetch roles
    res = authorized_client.get("/roles/")
    assert res.status_code == 200
    roles = [role_schema.RoleOut(**role) for role in res.json()]
    
    assert len(roles) == 1
    assert roles[0].role_name == test_role_data["role_name"]
    
