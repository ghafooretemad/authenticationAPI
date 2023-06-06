from api.main import app
from api.test_main import test_login, client
from random import randint

user = None


def test_user_list():
    response = client.post(
        "/users/users/", headers={"Authorization": f'bearer {test_login}'})
    assert response.status_code == 200


def test_create_user():
    sequence = randint(1, 1000)

    data = {
        "user": {
            "email": f"test{sequence}@gmail.com",
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

    global user
    user = response.json()
    # check for duplicate user
    response = client.post("/users/user", json=data,
                           headers={"Authorization": f'bearer {test_login}'})
    assert response.status_code == 400



def test_get_user_details():
    response = client.get(f"/users/user/userid/{user['id']}",
                          headers={"Authorization": f'bearer {test_login}'})

    assert response.status_code == 200


def test_get_user_details():
    response = client.get(f"/users/user/name/Test",
                          headers={"Authorization": f'bearer {test_login}'})

    assert response.status_code == 200
