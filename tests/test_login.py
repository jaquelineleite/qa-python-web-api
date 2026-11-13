from playwright.sync_api import Page, expect

from data.login_data import (
    VALID_USER,
    VALID_PASSWORD,
    INVALID_PASSWORD,
)
from pages.login_page import LoginPage


def test_login_valido(page: Page):
    login = LoginPage(page)
    login.abrir()
    login.realizar_login(VALID_USER, VALID_PASSWORD)

    expect(page).to_have_url(
        "https://www.saucedemo.com/inventory.html"
    )
    expect(page.locator(".title")).to_have_text("Products")


def test_login_senha_invalida(page: Page):
    login = LoginPage(page)
    login.abrir()
    login.realizar_login(VALID_USER, INVALID_PASSWORD)

    expect(login.mensagem_erro).to_contain_text(
        "Username and password do not match"
    )
