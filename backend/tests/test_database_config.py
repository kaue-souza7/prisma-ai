"""Garante que a DATABASE_URL sempre use o driver assíncrono asyncpg."""
from sqlalchemy.engine import make_url
from sqlalchemy.ext.asyncio import create_async_engine

from app.core.config import Settings


def _settings(database_url: str, **kwargs) -> Settings:
    return Settings(
        _env_file=None,
        database_url=database_url,
        secret_key="test-secret-key-with-at-least-32-characters",
        **kwargs,
    )


def test_postgres_scheme_is_converted_to_asyncpg():
    settings = _settings("postgres://user:password@db.example.com:5432/app")
    url = make_url(settings.async_database_url)

    assert url.drivername == "postgresql+asyncpg"
    assert url.username == "user"
    assert url.database == "app"


def test_psycopg2_scheme_is_converted_to_asyncpg():
    settings = _settings(
        "postgresql+psycopg2://user:password@db.example.com:5432/app"
    )
    url = make_url(settings.async_database_url)

    assert url.drivername == "postgresql+asyncpg"


def test_sslmode_and_channel_binding_are_adapted_for_asyncpg():
    settings = _settings(
        "postgresql://user:password@db.example.com:5432/app"
        "?sslmode=require&channel_binding=require"
    )
    query = dict(make_url(settings.async_database_url).query)

    assert query["ssl"] == "require"
    assert "sslmode" not in query
    assert "channel_binding" not in query


def test_unpooled_url_is_also_normalized_for_migrations():
    settings = _settings(
        "postgresql://user:password@pooler.example.com:5432/app",
        database_url_unpooled=(
            "postgresql://user:password@direct.example.com:5432/app"
            "?sslmode=require&channel_binding=require"
        ),
    )
    migration_url = make_url(settings.migration_database_url)

    assert migration_url.drivername == "postgresql+asyncpg"
    assert migration_url.host == "direct.example.com"
    assert dict(migration_url.query)["ssl"] == "require"
    assert "channel_binding" not in dict(migration_url.query)


def test_create_async_engine_uses_asyncpg_dialect():
    settings = _settings("postgresql://user:password@db.example.com:5432/app")
    engine = create_async_engine(settings.async_database_url)

    assert engine.dialect.driver == "asyncpg"
    assert engine.dialect.is_async is True
