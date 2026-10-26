"""Aplicação idempotente do conteúdo versionado da Fase 5."""
from app.modules.content.seeds.phase_5_v1 import PHASE_5_V1
from app.modules.content.seeds.seeder import seed_phase_content


def seed_phase_5(bind, data: dict | None = None) -> None:
    """Insere ou atualiza a Fase 5. Deve ser executada dentro de uma transação."""
    data = data or PHASE_5_V1
    seed_phase_content(bind, data, "seed:phase_5_v1")
