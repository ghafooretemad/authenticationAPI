from api.main import app
from api.test_main import test_login, client

permission = None


def test_permission_list():
    response = client.post(
        "/auth/permissions/", headers={"Authorization": f'bearer {test_login}'})
    assert response.status_code == 200


def test_create_permission():
    data = {
        "title": "Test Title Test",
        "description": "this is test decription"
    }
    response = client.post("/auth/permissions/permission", json=data,
                           headers={"Authorization": f'bearer {test_login}'})

    assert response.status_code == 200

    global permission

    permission = response.json()


def test_permission_update():
    data = {
        "title": "Test Permission Updated",
        "description": "test is updated test decription",
        "id": permission['id']
    }
    
    response = client.put(f"/auth/permissions/permission/update/{permission['id']}", json=data, headers={"Authorization": f'bearer {test_login}'})

    assert response.status_code == 200

def test_permission_get():
    response = client.get("/auth/permissions/permission/id/{0}".format(permission['id']), headers={"Authorization": f'bearer {test_login}'})
    
    assert response.status_code == 200

def test_permission_delete():
    response = client.put("/auth/permissions/permission/delete/{0}".format(permission['id']), headers={"Authorization": f'bearer {test_login}'})
    
    assert response.status_code == 200

