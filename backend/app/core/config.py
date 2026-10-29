from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import computed_field, field_validator
from sqlalchemy.engine import make_url
from sqlalchemy.exc import ArgumentError
from typing import List


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # Banco de dados
    database_url: str
    # Neon fornece uma URL direta (sem pooler) para migrations.
    database_url_unpooled: str | None = None

    @field_validator("database_url", "database_url_unpooled", mode="before")
    @classmethod
    def normalize_database_url(cls, value: str | None) -> str | None:
        """Garante o driver asyncpg mesmo quando o provedor envia URL síncrona.

        Render/Neon costumam entregar `postgres://` ou `postgresql://`.
        O SQLAlchemy interpreta essas URLs como psycopg2, incompatível com
        `create_async_engine()`. Normalizamos o driver e os parâmetros SSL
        aceitos pelo asyncpg, sem registrar a URL ou credenciais.
        """
        if value is None:
            return None
        if not isinstance(value, str) or not value.strip():
            return value

        try:
            url = make_url(value.strip())
        except ArgumentError as exc:
            # Não inclui a URL na mensagem para não vazar credenciais.
            raise ValueError("DATABASE_URL inválida.") from exc

        if url.drivername in {
            "postgres",
            "postgresql",
            "postgresql+psycopg",
            "postgresql+psycopg2",
            "postgresql+psycopg2cffi",
        }:
            url = url.set(drivername="postgresql+asyncpg")

        query = dict(url.query)
        # O asyncpg não aceita channel_binding como parâmetro de conexão.
        query.pop("channel_binding", None)
        # O asyncpg recebe o modo SSL como `ssl`, não como `sslmode`.
        sslmode = query.pop("sslmode", None)
        if sslmode is not None:
            query.setdefault("ssl", sslmode)

        return url.set(query=query).render_as_string(hide_password=False)

    @computed_field
    @property
    def async_database_url(self) -> str:
        """URL sempre pronta para `create_async_engine()`."""
        normalized = self.normalize_database_url(self.database_url)
        if normalized is None:
            raise ValueError("DATABASE_URL não configurada.")
        return normalized

    @computed_field
    @property
    def migration_database_url(self) -> str:
        """URL usada por migrations: direta no Neon, com fallback para a normal."""
        return self.database_url_unpooled or self.database_url

    # JWT
    secret_key: str
    access_token_expire_minutes: int = 60
    refresh_token_expire_days: int = 7

    # Ambiente
    environment: str = "development"
    # Log de SQL é opt-in para evitar vazamento de parâmetros em logs locais.
    sql_echo: bool = False

    # CORS
    allowed_origins: str = "http://localhost:5173"

    @computed_field
    @property
    def allowed_origins_list(self) -> List[str]:
        return [o.strip() for o in self.allowed_origins.split(",")]

    # IA — watsonx Orchestrate
    orchestrate_enabled: bool = False
    orchestrate_url: str = ""
    orchestrate_api_key: str = ""
    # Legado: mantido para compatibilidade com configs existentes.
    orchestrate_agent_id: str = ""
    # Agente Mentor — UUID no Orchestrate (obrigatório quando mentor está ligado).
    orchestrate_agent_mentor_id: str = ""
    # Agente Catalisador — UUID no Orchestrate.
    orchestrate_catalyst_agent_id: str = ""
    # Agente Analista — UUID no Orchestrate.
    orchestrate_analyst_agent_id: str = ""
    # Agente do Estúdio — UUID no Orchestrate (geração de revisão/flashcards/exercícios).
    orchestrate_studio_agent_id: str = ""
    orchestrate_timeout_seconds: float = 15.0
    # Estúdio: geração de conteúdo ainda não tem agente implementado.
    # Mantenha desligado para o endpoint devolver 503 sem cobrar Prismas.
    orchestrate_studio_enabled: bool = False
    # Flags por agente. Cada uma cai de volta para orchestrate_enabled quando
    # não definida explicitamente, permitindo rollout e rollback granular.
    orchestrate_mentor_enabled: bool | None = None
    orchestrate_catalyst_enabled: bool | None = None
    orchestrate_analyst_enabled: bool | None = None

    @computed_field
    @property
    def mentor_enabled(self) -> bool:
        if self.orchestrate_mentor_enabled is not None:
            return self.orchestrate_mentor_enabled
        return self.orchestrate_enabled

    @computed_field
    @property
    def catalyst_enabled(self) -> bool:
        if self.orchestrate_catalyst_enabled is not None:
            return self.orchestrate_catalyst_enabled
        return self.orchestrate_enabled

    @computed_field
    @property
    def analyst_enabled(self) -> bool:
        if self.orchestrate_analyst_enabled is not None:
            return self.orchestrate_analyst_enabled
        return self.orchestrate_enabled

    # E-mail
    # Enquanto a confirmação por e-mail estiver desativada, o cadastro cria
    # o usuário já verificado e libera o acesso imediatamente.
    require_email_verification: bool = False
    mail_enabled: bool = False
    mail_from: str = "noreply@ell-ibm.local"
    mail_server: str = ""
    mail_port: int = 587
    mail_username: str = ""
    mail_password: str = ""
    mail_tls: bool = True

    @computed_field
    @property
    def is_development(self) -> bool:
        return self.environment == "development"


settings = Settings()
