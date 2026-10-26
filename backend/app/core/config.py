from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import computed_field
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

    # IA — watsonx Orchestrate (integração real bloqueada até o spike D7)
    orchestrate_enabled: bool = False
    orchestrate_url: str = ""
    orchestrate_api_key: str = ""
    orchestrate_agent_id: str = ""
    orchestrate_timeout_seconds: float = 15.0

    # E-mail
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
