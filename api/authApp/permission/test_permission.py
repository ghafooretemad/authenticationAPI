from api.main import app
from api.test_main import test_login, client

permission = None

def test_permission_list():
    response = client.post(
        "/users/users/", headers={"Authorization": f'bearer {test_login}'})
    assert response.status_code == 200
