import pytest
import requests


@pytest.mark.parametrize("user_id", [1, 2, 3])
def test_consultar_usuario_existente(api_base_url, user_id):
    response = requests.get(
        f"{api_base_url}/users/{user_id}",
        timeout=10,
    )

    assert response.status_code == 200

    usuario = response.json()

    assert usuario["id"] == user_id
    assert isinstance(usuario["name"], str)
    assert usuario["name"].strip()
    assert isinstance(usuario["email"], str)
    assert "@" in usuario["email"]


@pytest.mark.parametrize("user_id", [0, 999999])
def test_consultar_usuario_inexistente(api_base_url, user_id):
    response = requests.get(
        f"{api_base_url}/users/{user_id}",
        timeout=10,
    )

    assert response.status_code == 404
    assert response.json() == {}
