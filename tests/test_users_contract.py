"""Contract checks for the documented JSONPlaceholder /users demo dataset.

These are selected structural assertions, not a complete OpenAPI schema.
"""
import pytest
import requests


@pytest.mark.parametrize("user_id", [1, 10])
def test_usuario_contrato_campos_essenciais(api_base_url, user_id):
    response = requests.get(f"{api_base_url}/users/{user_id}", timeout=10)

    assert response.status_code == 200
    assert response.headers["Content-Type"].split(";")[0].strip() == "application/json"

    usuario = response.json()
    assert isinstance(usuario, dict)
    assert type(usuario.get("id")) is int
    assert usuario["id"] == user_id

    for campo in ("name", "username", "email", "phone", "website"):
        assert isinstance(usuario.get(campo), str), f"{campo} deve ser texto"
        assert usuario[campo].strip(), f"{campo} não pode estar vazio"

    assert isinstance(usuario.get("address"), dict)
    assert isinstance(usuario["address"].get("geo"), dict)
    for coordenada in ("lat", "lng"):
        assert isinstance(usuario["address"]["geo"].get(coordenada), str)

    assert isinstance(usuario.get("company"), dict)
    assert isinstance(usuario["company"].get("name"), str)
    assert usuario["company"]["name"].strip()


def test_usuario_apos_limite_dataset_demo_retorna_404(api_base_url):
    # JSONPlaceholder publica dez usuários; 11 é borda do dataset de demonstração.
    response = requests.get(f"{api_base_url}/users/11", timeout=10)

    assert response.status_code == 404
    assert response.json() == {}
