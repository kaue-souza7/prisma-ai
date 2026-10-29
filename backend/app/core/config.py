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
