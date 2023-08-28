from unittest.mock import patch
from config.app import application
from fastapi.testclient import TestClient


client = TestClient(application)


def test_get_users():

    mock_get_users = {
        "data": [
            {
                "name": "Alejandro",
                "email": "kannder.ziur@gmail.com",
                "is_active": True,
                "user_id": "64eb77d8008278db06caf636"
            }
        ],
        "total_users": 1,
        "msg": "ok"
    }

    with patch("app.user.controller.db_user.get_users", return_value=mock_get_users):
        response = client.get("/apiv1/users/")
        assert response.status_code == 200
        data = response.json()
        assert data == mock_get_users
