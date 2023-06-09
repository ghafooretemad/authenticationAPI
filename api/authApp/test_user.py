from api.main import app
from api.test_main import test_login, client
from random import randint

user = None
sequence = randint(1, 1000)
group = None

def test_user_list():
    response = client.post(
        "/auth/users/", headers={"Authorization": f'bearer {test_login}'})
    assert response.status_code == 200


def test_create_user():

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

    response = client.post("/auth/users/user", json=data,
                           headers={"Authorization": f'bearer {test_login}'})

    assert response.status_code == 201

    global user
    user = response.json()
    # check for duplicate user
    response = client.post("/auth/users/user", json=data,
                           headers={"Authorization": f'bearer {test_login}'})
    assert response.status_code == 400


def test_get_user_details():
    response = client.get(f"/auth/users/user/userid/{user['id']}",
                          headers={"Authorization": f'bearer {test_login}'})

    assert response.status_code == 200


def test_get_user_details():
    response = client.get(f"/auth/users/user/name/Test",
                          headers={"Authorization": f'bearer {test_login}'})

    assert response.status_code == 200


def test_update_user():
    data = {
        "email": f"test{sequence}@gmail.com",
        "is_active": True,
        "department_id": 0,
        "hashed_password": "secret"
    }

    response = client.put(f"/auth/users/user/update/{user['id']}", json=data, headers={
                          "Authorization": f'bearer {test_login}'})

    assert response.status_code == 200


def test_user_group_update():
    data = [
        {
            "group_id": 3
        },
        {
            "group_id": 4
        }
    ]
    client.post(f"/user-group/update/{user['id']}", json=data,
                headers={"Authorization": f'bearer {test_login}'})


def test_group_create():
    data = {
        "group": {
            "title": "Testing Group",
            "description": "Testing Group description"
        },
        "group_role": [
            {
                "group_id": 0,
                "role_id": 2
            },
            {
                "group_id": 0,
                "role_id": 5
            }
        ]
    }
    
    response = client.post("/auth/groups/group", json=data, headers={"Authorization": f'bearer {test_login}'})
    
    assert response.status_code == 200
    
    global group
    
    group = response.json()


def test_user_group_delete():

    response = client.put(f"/auth/users/user-group/delete/{group['id']}", headers={"Authorization": f'bearer {test_login}'})
    assert response.status_code == 200


def test_user_group_get():

    response = client.get(f"/auth/users/user-group/{user['id']}", headers={"Authorization": f'bearer {test_login}'})
    assert response.status_code == 200
    
    response = client.get(f"/auth/users/user-group/0", headers={"Authorization": f'bearer {test_login}'})
    assert response.json() == []
    
    

def test_user_permission_get():

    response = client.get(f"/auth/users/user-permission/{user['id']}", headers={"Authorization": f'bearer {test_login}'})
    assert response.status_code == 200
    
    response = client.get(f"/auth/users/user-permission/0", headers={"Authorization": f'bearer {test_login}'})
    assert response.json() == []