import pytest
import os
os.environ.setdefault("DATABASE_URL", "postgresql+asyncpg://test:test@localhost/test")
os.environ.setdefault("SECRET_KEY", "testsecretkey1234567890abcdefghij")

from app.modules.auth.schemas import RegisterRequest
from pydantic import ValidationError


def test_register_valid():
    r = RegisterRequest(email="test@example.com", password="Senha123")
    assert r.email == "test@example.com"


def test_register_password_too_short():
    with pytest.raises(ValidationError):
        RegisterRequest(email="test@example.com", password="Ab1")


def test_register_password_no_uppercase():
    with pytest.raises(ValidationError):
        RegisterRequest(email="test@example.com", password="senha123")


def test_register_password_no_number():
    with pytest.raises(ValidationError):
        RegisterRequest(email="test@example.com", password="SenhaSemNumero")


def test_register_invalid_email():
    with pytest.raises(ValidationError):
        RegisterRequest(email="nao_e_email", password="Senha123")
