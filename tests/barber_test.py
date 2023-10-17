from fastapi.testclient import TestClient
from app.main import app


client = TestClient(app)

def test_root():

    res = client.get("/")
    print(res.json())


def test_create_barber(authorized_client):
    test_barber_data = {
        "user_id": 1,
        "bio": "Test Barber Bio",
    }
    res = authorized_client.post("/barbers/", json=test_barber_data)
    assert res.status_code == 201
    barber = res.json()
    assert barber["bio"] == test_barber_data["bio"]

def test_get_barbers(test_barber,authorized_client,):
    res = authorized_client.get("/barbers/")
    assert res.status_code == 200
    barbers = res.json()
    assert len(barbers) > 0  

def test_get_specific_barber(test_barber,authorized_client):
    res = authorized_client.get("/barbers/1")
    assert res.status_code == 200
    barber = res.json()
    assert barber["barber_id"] == 1

def test_update_barber(test_barber,authorized_client):
    update_data = {
        "bio": "Updated Barber Bio",   
    }
    res = authorized_client.put("/barbers/1", json=update_data)
    assert res.status_code == 200
    barber = res.json()
    assert barber["bio"] == update_data["bio"]


def test_delete_barber(test_barber,authorized_client):
    res = authorized_client.delete("/barbers/1")
    assert res.status_code == 204

    res = authorized_client.get("/barbers/1")
    assert res.status_code == 404
