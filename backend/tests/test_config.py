from app.core.config import Settings


def _settings(
    database_url: str, database_url_unpooled: str | None = None
) -> Settings:
    return Settings(
        database_url=database_url,
        database_url_unpooled=database_url_unpooled,
        secret_key="test-secret",
    )


def test_database_url_normalizes_postgres_scheme():
    settings = _settings("postgres://user:pass@host:5432/db?sslmode=require")
    assert settings.database_url == (
        "postgresql+asyncpg://user:pass@host:5432/db?ssl=require"
    )


def test_database_url_normalizes_postgresql_scheme():
    settings = _settings("postgresql://user:pass@host:5432/db")
    assert settings.database_url == "postgresql+asyncpg://user:pass@host:5432/db"


def test_database_url_keeps_asyncpg_scheme():
    url = "postgresql+asyncpg://user:pass@host:5432/db"
    settings = _settings(url)
    assert settings.database_url == url


def test_database_url_removes_channel_binding():
    settings = _settings(
        "postgresql://user:pass@host:5432/db?sslmode=require&channel_binding=require"
    )
    assert settings.database_url == (
        "postgresql+asyncpg://user:pass@host:5432/db?ssl=require"
    )


def test_migration_database_url_prefers_unpooled_neon_url():
    settings = _settings(
        "postgresql://user:pass@pooler.host/db",
        "postgresql://user:pass@direct.host/db",
    )
    assert settings.migration_database_url == (
        "postgresql+asyncpg://user:pass@direct.host/db"
    )
    assert settings.database_url == "postgresql+asyncpg://user:pass@pooler.host/db"
