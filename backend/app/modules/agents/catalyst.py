"""Catalisador — lógica determinística de trilha e próximo passo.

Este módulo é a camada que o Catalisador IA vai substituir/estender quando o
watsonx Orchestrate estiver disponível. No MVP ele não usa IA: gera uma trilha
personalizada a partir do onboarding e produz mensagens explícitas de próximo
passo, sempre validadas pelo backend.

Regra central: nenhuma trilha gerada aqui altera pontos, conquistas ou
desbloqueios diretamente. O backend valida a trilha e continua sendo a
autoridade sobre o estado do estudante.
"""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Iterable

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.shared.models import Phase, Profile

DEFAULT_PHASE_ORDER = [1, 2, 3, 4, 5, 6]

# Mapeamento explícito e documentado. A ordem define a sequência das fases na
# trilha; dentro de cada fase, as missões continuam sequenciais.
TRAIL_RULES: dict[str, dict] = {
    "primeiro_salario": {
        "phase_order": [1, 2, 3, 4, 5, 6],
        "rationale": (
            "Começar pelo primeiro salário organiza a base: entender o que "
            "entra, o que sai e como o dinheiro digital funciona."
        ),
        "focus_areas": ["Salário bruto e líquido", "Orçamento", "Meios de pagamento"],
    },
    "dividas": {
        "phase_order": [4, 1, 2, 3, 5, 6],
        "rationale": (
            "Como seu objetivo é sair das dívidas, começar por juros ajuda a "
            "entender o custo real do crédito antes de reorganizar o orçamento."
        ),
        "focus_areas": ["Juros compostos", "Custo de parcelamentos", "Estratégia para sair da dívida"],
    },
    "credito_juros": {
        "phase_order": [4, 1, 2, 3, 5, 6],
        "rationale": (
            "Você quer entender crédito e juros, então a trilha começa pelo "
            "custo do dinheiro no tempo e depois volta para a base do orçamento."
        ),
        "focus_areas": ["Juros simples e compostos", "Parcelamento", "Rotativo"],
    },
    "reserva": {
        "phase_order": [3, 1, 2, 4, 5, 6],
        "rationale": (
            "Para criar uma reserva, a trilha começa por metas e pela diferença "
            "entre imprevisto e desejo, antes de aprofundar juros e investimentos."
        ),
        "focus_areas": ["Meta financeira", "Reserva de emergência", "Equilíbrio do orçamento"],
    },
    "investimentos": {
        "phase_order": [3, 4, 5, 1, 2, 6],
        "rationale": (
            "Investir melhor começa por poupar com objetivo, entender juros e "
            "só então comparar rendimento, prazo, liquidez e risco."
        ),
        "focus_areas": ["Objetivo financeiro", "Juros compostos", "Risco, prazo e liquidez"],
    },
    "protecao_digital": {
        "phase_order": [6, 2, 1, 3, 4, 5],
        "rationale": (
            "Seu foco é proteção digital, então a trilha começa por golpes e "
            "dados pessoais, conecta com o dinheiro digital e depois avança na base."
        ),
        "focus_areas": ["Phishing", "Golpes com Pix", "Proteção de dados"],
    },
    "outro": {
        "phase_order": [1, 2, 3, 4, 5, 6],
        "rationale": (
            "A trilha começa pela base do primeiro salário e avança conforme "
            "você constrói evidências de aprendizagem."
        ),
        "focus_areas": ["Fundamentos", "Orçamento", "Decisões financeiras"],
    },
}

# Ajustes por contexto de vida. Só se aplicam quando o objetivo não tem uma
# ordem própria mais específica (primeiro salário ou outro).
LIFE_CONTEXT_RULES: dict[str, dict] = {
    "primeiro_emprego": {
        "phase_order": [1, 2, 3, 4, 5, 6],
        "rationale": "Seu primeiro emprego pede uma base clara sobre salário, descontos e orçamento.",
    },
    "ja_trabalho": {
        "phase_order": [1, 2, 3, 4, 5, 6],
        "rationale": "Como você já trabalha, a trilha organiza a renda atual e aprofunda as decisões do dia a dia.",
    },
    "autonomo_freelancer": {
        "phase_order": [2, 3, 1, 4, 5, 6],
        "rationale": "Sua renda variável pede atenção primeiro a meios de pagamento, reserva e organização do fluxo de caixa.",
    },
    "estudante_sem_renda": {
        "phase_order": [3, 1, 2, 4, 5, 6],
        "rationale": "Começar por metas e reserva ajuda a construir hábitos antes de lidar com uma renda fixa.",
    },
}

PACE_BY_LEVEL = {
    "beginner": "supported",
    "intermediate": "steady",
    "advanced": "accelerated",
}


def _valid_order(order: Iterable, available_numbers: set[int]) -> list[int] | None:
    if not isinstance(order, (list, tuple)):
        return None
    cleaned: list[int] = []
    for number in order:
        if isinstance(number, bool) or not isinstance(number, int):
            return None
        if number not in available_numbers or number in cleaned:
            return None
        cleaned.append(number)
    if set(cleaned) != available_numbers:
        return None
    return cleaned


def validate_phase_order(
    order: Iterable, available_numbers: set[int] | None = None
) -> list[int] | None:
    """Valida uma ordem de fases vinda de regra, usuário ou futuro agente IA.

    A ordem só é aceita se contiver exatamente todas as fases ativas, uma vez
    cada. Qualquer outro formato é rejeitado e o backend usa a ordem padrão.
    """
    if available_numbers is None:
        available_numbers = set(DEFAULT_PHASE_ORDER)
    return _valid_order(order, available_numbers)


def _goal_category(profile: Profile) -> str:
    preferences = profile.preferences or {}
    category = preferences.get("goal_category")
    if category in TRAIL_RULES:
        return category
    return "outro"


def build_trail(
    *,
    personal_goal: str | None,
    goal_category: str | None,
    knowledge_level: str | None,
    preferences: dict | None = None,
) -> dict:
    """Gera a trilha determinística inicial a partir do onboarding."""
    preferences = preferences or {}
    category = goal_category if goal_category in TRAIL_RULES else "outro"
    rule = TRAIL_RULES[category]
    phase_order = list(rule["phase_order"])
    rationale = rule["rationale"]
    focus_areas = list(rule["focus_areas"])

    life_context = preferences.get("life_context")
    urgency = preferences.get("urgency")

    if category in {"primeiro_salario", "outro"} and life_context in LIFE_CONTEXT_RULES:
        context_rule = LIFE_CONTEXT_RULES[life_context]
        phase_order = list(context_rule["phase_order"])
        rationale = context_rule["rationale"]

    if urgency == "agora_preciso" and category in {"outro", "primeiro_salario"}:
        # Diante de uma necessidade imediata, poupar e entender o custo do
        # crédito vêm antes de aprofundar investimentos.
        if phase_order[0] not in {3, 4}:
            phase_order = [3, 1, 2, 4, 5, 6]
            rationale = (
                "Como você indicou uma necessidade imediata, a trilha começa "
                "por organização e reserva antes de avançar para investimentos."
            )

    if personal_goal and category == "outro":
        rationale = f"Seu objetivo — {personal_goal} — orienta esta trilha inicial. {rationale}"

    pace = PACE_BY_LEVEL.get(knowledge_level or "beginner", "supported")
    if pace == "accelerated":
        rationale = (
            f"{rationale} Como você já tem alguma base, pode avançar em um ritmo "
            "mais rápido e usar as revisões quando precisar."
        )

    return {
        "source": "rules",
        "version": 1,
        "goal_category": category,
        "phase_order": phase_order,
        "rationale": rationale,
        "focus_areas": focus_areas,
        "pace": pace,
        "knowledge_level": knowledge_level,
        "life_context": life_context,
        "urgency": urgency,
        "generated_at": datetime.now(timezone.utc).isoformat(),
    }


def build_standard_trail() -> dict:
    return {
        "source": "standard",
        "version": 1,
        "goal_category": "primeiro_salario",
        "phase_order": list(DEFAULT_PHASE_ORDER),
        "rationale": (
            "A ordem padrão apresenta os conceitos na sequência em que foram "
            "desenhados para construir uma base sólida."
        ),
        "focus_areas": ["Fundamentos", "Orçamento", "Decisões financeiras"],
        "pace": "steady",
        "generated_at": datetime.now(timezone.utc).isoformat(),
    }


async def get_active_phases(db: AsyncSession) -> list[Phase]:
    result = await db.execute(
        select(Phase).where(Phase.is_active == True).order_by(Phase.order)
    )
    return list(result.scalars().all())


async def get_phase_order(
    db: AsyncSession,
    user_id: int,
    phases: list[Phase] | None = None,
) -> list[int]:
    """Lê a trilha do perfil; sem trilha válida, usa a ordem canônica."""
    phases = phases or await get_active_phases(db)
    available = {phase.number for phase in phases}
    default_order = [
        phase.number for phase in sorted(phases, key=lambda item: item.order)
    ]

    result = await db.execute(select(Profile).where(Profile.user_id == user_id))
    profile = result.scalar_one_or_none()
    trail = (profile.trail if profile else None) or {}
    order = validate_phase_order(trail.get("phase_order"), available)
    return order or default_order


async def get_trail_view(db: AsyncSession, user_id: int) -> dict | None:
    """Devolve a trilha persistida com os dados de fase usados pela UI."""
    result = await db.execute(select(Profile).where(Profile.user_id == user_id))
    profile = result.scalar_one_or_none()
    trail = (profile.trail if profile else None) or None
    if not trail:
        return None

    phases = await get_active_phases(db)
    available = {phase.number for phase in phases}
    order = validate_phase_order(trail.get("phase_order"), available)
    if not order:
        return None

    by_number = {phase.number: phase for phase in phases}
    return {
        **trail,
        "phase_order": order,
        "phases": [
            {
                "number": by_number[number].number,
                "name": by_number[number].name,
                "description": by_number[number].description,
            }
            for number in order
        ],
    }


async def apply_generated_trail(
    db: AsyncSession,
    user_id: int,
    generated: dict,
    *,
    source: str = "ai",
) -> dict:
    """Ponto de entrada para uma trilha gerada pelo Catalisador IA.

    O agente propõe `phase_order`, `rationale` e `focus_areas`; o backend
    valida a ordem contra as fases ativas e só então persiste. Uma trilha
    inválida é rejeitada com `ValueError` — nunca desbloqueia fases por engano.
    """
    phases = await get_active_phases(db)
    available = {phase.number for phase in phases}
    order = validate_phase_order(generated.get("phase_order"), available)
    if not order:
        raise ValueError("Ordem de fases inválida para a trilha.")

    result = await db.execute(select(Profile).where(Profile.user_id == user_id))
    profile = result.scalar_one_or_none()
    if not profile:
        raise ValueError("Perfil não encontrado.")

    profile.trail = {
        **generated,
        "source": source,
        "version": generated.get("version", 1),
        "phase_order": order,
        "rationale": generated.get("rationale") or "Trilha sugerida pelo Catalisador.",
        "focus_areas": generated.get("focus_areas") or [],
        "pace": generated.get("pace") or "steady",
        "generated_at": datetime.now(timezone.utc).isoformat(),
    }
    await db.flush()
    view = await get_trail_view(db, user_id)
    return view or profile.trail


def build_recommendation(
    *,
    trail: dict | None,
    mission_name: str | None,
    mission_id: int | None,
    phase_number: int | None,
    phase_name: str | None,
    is_in_progress: bool,
    has_mission: bool,
    reinforcement_topics: list[str] | None = None,
    trail_position: int | None = None,
    trail_size: int | None = None,
) -> dict:
    """Mensagem determinística do Catalisador para o próximo passo."""
    reinforcement_topics = reinforcement_topics or []

    if not has_mission:
        return {
            "kind": "complete",
            "message": (
                "Você concluiu o que está disponível nesta trilha. Seu progresso "
                "está salvo; as próximas fases entram quando o conteúdo for publicado."
            ),
            "mission_id": None,
            "mission_name": None,
            "phase_number": None,
            "phase_name": None,
            "trail_position": trail_position,
            "trail_size": trail_size,
        }

    if reinforcement_topics:
        topics = ", ".join(reinforcement_topics[:2])
        message = (
            f"Antes de avançar, vale revisar {topics}. Você pode voltar ao "
            "conteúdo da missão e tentar de novo sem pressa."
        )
        kind = "review"
    elif is_in_progress:
        message = f"Retome “{mission_name}” de onde parou. Cada etapa concluída fica salva."
        kind = "continue"
    elif trail and trail.get("source") != "standard" and trail_position == 1:
        message = (
            f"Sua trilha começa por {phase_name}. {trail.get('rationale', '')}".strip()
        )
        kind = "start"
    elif phase_number:
        message = (
            f"O próximo passo é “{mission_name}”, na fase {phase_number}. "
            "Essa missão conecta com o que você praticou até aqui."
        )
        kind = "start"
    else:
        message = "Seu próximo passo está pronto. Comece quando quiser."
        kind = "start"

    return {
        "kind": kind,
        "message": message,
        "mission_id": mission_id,
        "mission_name": mission_name,
        "phase_number": phase_number,
        "phase_name": phase_name,
        "trail_position": trail_position,
        "trail_size": trail_size,
    }
