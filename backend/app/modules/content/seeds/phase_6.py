"""Aplicação idempotente do conteúdo versionado da Fase 6."""
from app.modules.content.seeds.phase_6_v1 import PHASE_6_V1
from app.modules.content.seeds.seeder import seed_phase_content


def seed_phase_6(bind, data: dict | None = None) -> None:
    """Insere ou atualiza a Fase 6. Deve ser executada dentro de uma transação."""
    data = data or PHASE_6_V1
    seed_phase_content(bind, data, "seed:phase_6_v1")
