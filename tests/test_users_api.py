import requests


BASE_URL = "https://jsonplaceholder.typicode.com"


def test_consultar_usuario_existente():
    response = requests.get(
        f"{BASE_URL}/users/1",
        timeout=10,
    )

    assert response.status_code == 200

    usuario = response.json()

    assert usuario["id"] == 1
    assert isinstance(usuario["name"], str)
    assert usuario["name"].strip()
    assert "@" in usuario["email"]


def test_consultar_usuario_inexistente():
    response = requests.get(
        f"{BASE_URL}/users/999999",
        timeout=10,
    )

    assert response.status_code == 404
    assert response.json() == {}
