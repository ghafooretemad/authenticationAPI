from fastapi import FastAPI
from fastapi.testclient import TestClient
from api.main import app
import pytest


client = TestClient(app)

@pytest.fixture
def test_login():
    logindata = dict(
        grant_type= "",
        username= "admin2",
        password= "secret",
        scope= "",
        client_id= "",
        client_secret= ""
    )
    response = client.post("/token/", data=logindata)
    assert response.status_code == 200
    return response.json()["access_token"]

