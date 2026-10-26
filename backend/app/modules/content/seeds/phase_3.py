"""Aplicação idempotente do conteúdo versionado da Fase 3."""
from app.modules.content.seeds.phase_3_v1 import PHASE_3_V1
from app.modules.content.seeds.seeder import seed_phase_content


def seed_phase_3(bind, data: dict | None = None) -> None:
    """Insere ou atualiza a Fase 3. Deve ser executada dentro de uma transação."""
    data = data or PHASE_3_V1
    seed_phase_content(bind, data, "seed:phase_3_v1")
