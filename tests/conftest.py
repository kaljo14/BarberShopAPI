import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.config.env_variables_config import settings
from app.database.database import Base
from app.database.database import get_db
from app.main import app
from app.security.oauth2 import create_access_token

# SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:password123@localhost:5432/fastapi_test'
SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}_test'


engine = create_engine(SQLALCHEMY_DATABASE_URL)

TestingSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine)


@pytest.fixture()
def session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture()
def client(session):
    def override_get_db():

        try:
            yield session
        finally:
            session.close()
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)


@pytest.fixture
def test_user(client):
    user_data = {"email": "hello123@gmail.com", "password": "password123","phone_number":"08890123123","first_name": "string","last_name": "string"}
    res = client.post("/users/", json=user_data)

    assert res.status_code == 201

    new_user = res.json()
    new_user['password'] = user_data['password']
    return new_user
@pytest.fixture
def test_user2(client):
    user_data = {"email": "hello23@gmail.com", "password": "password123","phone_number":"088901123123","first_name": "string","last_name": "string"}
    res = client.post("/users/", json=user_data)

    assert res.status_code == 201

    new_user = res.json()
    new_user['password'] = user_data['password']
    return new_user

@pytest.fixture
def test_barber(authorized_client):
    barber_data ={"user_id": 1}
    res = authorized_client.post("/barbers/", json=barber_data)

    assert res.status_code == 201
    barber_data =res.json()
    return barber_data
@pytest.fixture
def test_barber2(authorized_client):
    barber_data ={"user_id": 2}
    res = authorized_client.post("/barbers/", json=barber_data)

    assert res.status_code == 201
    barber_data =res.json()
    return barber_data

# ----------------------- Autorization ----------------------
@pytest.fixture
def token(test_user):
    return create_access_token({"user_id": test_user['user_id']})


@pytest.fixture
def authorized_client(client, token):
    client.headers = {
        **client.headers,
        "Authorization": f"Bearer {token}"
    }

    return client

# ----------------------- Autorization ----------------------

