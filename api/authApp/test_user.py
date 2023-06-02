from api.main import app
from api.test_main import test_login, client
from random import randint

def test_user_list():
    response = client.post(
        "/users/users/", headers={"Authorization": f'bearer {test_login}'})
    assert response.status_code == 200


def test_create_user():
    id = randint(1, 100)
    data =    {
        "user": {
            "email": f"test{id}@gmail.com",
            "is_active": True,
            "department_id": 0,
            "hashed_password": "secret"
        },
        "profile": {
            "first_name": "Test",
            "last_name": "khan",
            "phone": "0445434543",
            "address": "luedinghausen",
            "dob": "1996-06-02"
        },
        "user_group": [
            {
                "group_id": 4
            }
        ]
    }

    response = client.post("/users/user", json=data,
                           headers={"Authorization": f'bearer {test_login}'})

    assert response.status_code == 201
