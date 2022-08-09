import unittest
from fastapi.testclient import TestClient
from api.main import app


client = TestClient(app)


class TestMain(unittest.TestCase):
    def test_main_home(self):
        response = client.get("/")
        assert response.status_code == 200

    def test_main_fetch(self):
        response = client.get("/?query=3")
        assert response.status_code == 200
        assert len(response.json()) == 3

    def test_main_search(self):
        response = client.get("/search?query=Hello World")
        assert response.status_code == 200
        assert str(response.json()).__contains__("Hello") and str(response.json()).__contains__("World")

        response = client.get("/search?query=Hello Worlddafdfaafadfd")
        assert response.status_code == 200
        assert response.json() == []

        response = client.get("/search?query=Hello World\"")
        assert response.status_code == 400

        response = client.get("/search?query=13")
        assert response.status_code == 200
