"""Aplicação idempotente do conteúdo versionado da Fase 4."""
from app.modules.content.seeds.phase_4_v1 import PHASE_4_V1
from app.modules.content.seeds.seeder import seed_phase_content


def seed_phase_4(bind, data: dict | None = None) -> None:
    """Insere ou atualiza a Fase 4. Deve ser executada dentro de uma transação."""
    data = data or PHASE_4_V1
    seed_phase_content(bind, data, "seed:phase_4_v1")
