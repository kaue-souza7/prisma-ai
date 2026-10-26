import os

# Valores mínimos para permitir importar a aplicação em execuções locais.
# Em Docker, o .env e as variáveis do compose prevalecem.
os.environ.setdefault("DATABASE_URL", "postgresql+asyncpg://test:test@localhost/test")
os.environ.setdefault("SECRET_KEY", "testsecretkey1234567890abcdefghij")

import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlalchemy import select
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.pool import NullPool

from app.core.config import settings
from app.core.database import get_db
from app.main import app
from app.shared.models import User


@pytest_asyncio.fixture
async def db_context():
    """
    Mantém cada teste em uma transação externa revertida ao final.

    A aplicação usa sessões curtas e faz commit por requisição; o modo
    create_savepoint preserva essas transações internas sem deixar dados no
    banco de desenvolvimento.
    """
    engine = create_async_engine(settings.database_url, poolclass=NullPool)
    try:
        connection = await engine.connect()
    except Exception as exc:
        await engine.dispose()
        pytest.skip(
            "PostgreSQL de teste indisponível "
            f"({exc.__class__.__name__}). Execute os testes com "
            "'docker compose exec backend pytest' para incluir a integração."
        )

    transaction = await connection.begin()
    session_factory = async_sessionmaker(
        bind=connection,
        expire_on_commit=False,
        join_transaction_mode="create_savepoint",
    )

    async def override_get_db():
        async with session_factory() as session:
            try:
                yield session
                await session.commit()
            except Exception:
                await session.rollback()
                raise

    app.dependency_overrides[get_db] = override_get_db
    try:
        yield session_factory
    finally:
        app.dependency_overrides.pop(get_db, None)
        await transaction.rollback()
        await connection.close()
        await engine.dispose()


@pytest_asyncio.fixture
async def db_session(db_context):
    async with db_context() as session:
        yield session


@pytest_asyncio.fixture
async def client(db_context):
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as http_client:
        yield http_client


async def register_verified_user(client: AsyncClient, db_session, password: str = "Senha123"):
    """Cria, verifica e autentica um usuário único para o teste."""
    from uuid import uuid4

    email = f"teste.{uuid4().hex}@example.com"
    register = await client.post(
        "/api/v1/auth/register",
        json={"email": email, "password": password},
    )
    assert register.status_code == 201, register.text

    result = await db_session.execute(select(User).where(User.email == email))
    user = result.scalar_one()
    verify = await client.get(f"/api/v1/auth/verify-email?token={user.verification_token}")
    assert verify.status_code == 200, verify.text

    login = await client.post(
        "/api/v1/auth/login",
        json={"email": email, "password": password},
    )
    assert login.status_code == 200, login.text
    tokens = login.json()
    return user, tokens


def auth_headers(tokens: dict) -> dict:
    return {"Authorization": f"Bearer {tokens['access_token']}"}
