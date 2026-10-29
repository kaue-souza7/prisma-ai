"""Catalisador — trilha personalizada, onboarding conversacional e presença contínua.

Este módulo é o ponto de substituição do Catalisador IA no watsonx Orchestrate.
Quando `ORCHESTRATE_ENABLED=true`, as funções `conduct_onboarding()`,
`build_recommendation()` e `celebrate_trail_completion()` chamam o agente
`prisma_catalyst`. Quando desativado ou em erro, usam fallback determinístico
completo — mesmo contrato de entrada/saída.

Regra central: nenhuma função aqui altera pontos, conquistas ou desbloqueios
diretamente. O backend valida a trilha e continua sendo a autoridade sobre o
estado do estudante.

Histórico de mudanças:
  - v1 (original): 6 fases (DEFAULT_PHASE_ORDER = [1..6])
  - v2 (reestruturação 12 trilhas): DEFAULT_PHASE_ORDER = [1..12].
  - v3 (Sub-tarefas 4+5): conduct_onboarding(), build_recommendation() via IA,
    celebrate_trail_completion(), get_trail_mode().
"""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Iterable

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.logging import logger
from app.core.orchestrate_client import OrchestrateError, chat_completion
from app.core.orchestrate_parser import (
    extract_agent_json,
    validate_catalyst_celebrate_response,
    validate_catalyst_next_step_response,
    validate_catalyst_onboarding_response,
)
from app.shared.models import Phase, Profile

DEFAULT_PHASE_ORDER = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]

# Mapeamento explícito e documentado. A ordem define a sequência das trilhas;
# dentro de cada trilha, as missões continuam sequenciais.
# Regra invariante: a trilha 12 (Desafio integrador) é sempre a última.
# Qualquer reordenação deve respeitar essa invariante.
TRAIL_RULES: dict[str, dict] = {
    "primeiro_salario": {
        "phase_order": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
        "rationale": (
            "Começar pelo primeiro salário organiza a base: entender o que "
            "entra, o que sai e como o dinheiro digital funciona."
        ),
        "focus_areas": ["Salário bruto e líquido", "Orçamento", "Meios de pagamento"],
    },
    "dividas": {
        "phase_order": [7, 8, 1, 2, 3, 4, 5, 6, 9, 10, 11, 12],
        "rationale": (
            "Como seu objetivo é sair das dívidas, começar por juros e dívida "
            "ajuda a entender o custo real do crédito antes de reorganizar o orçamento."
        ),
        "focus_areas": ["Juros compostos", "Custo de parcelamentos", "Estratégia para sair da dívida"],
    },
    "credito_juros": {
        "phase_order": [7, 8, 4, 1, 2, 3, 5, 6, 9, 10, 11, 12],
        "rationale": (
            "Você quer entender crédito e juros, então a trilha começa pelo "
            "custo do dinheiro no tempo e depois volta para a base do orçamento."
        ),
        "focus_areas": ["Juros simples e compostos", "CET", "Crédito rotativo"],
    },
    "reserva": {
        "phase_order": [5, 6, 1, 2, 3, 4, 7, 8, 9, 10, 11, 12],
        "rationale": (
            "Para criar uma reserva, a trilha começa por metas e pela diferença "
            "entre imprevisto e desejo, antes de aprofundar juros e investimentos."
        ),
        "focus_areas": ["Meta financeira", "Reserva de emergência", "Equilíbrio do orçamento"],
    },
    "investimentos": {
        "phase_order": [5, 6, 7, 9, 10, 1, 2, 3, 4, 8, 11, 12],
        "rationale": (
            "Investir melhor começa por poupar com objetivo, entender juros e "
            "só então comparar rendimento real, prazo, liquidez e risco."
        ),
        "focus_areas": ["Objetivo financeiro", "Juros compostos", "Risco, prazo e liquidez"],
    },
    "protecao_digital": {
        "phase_order": [11, 3, 4, 1, 2, 5, 6, 7, 8, 9, 10, 12],
        "rationale": (
            "Seu foco é proteção digital, então a trilha começa por golpes e "
            "dados pessoais, conecta com o dinheiro digital e depois avança na base."
        ),
        "focus_areas": ["Phishing", "Golpes com Pix", "Proteção de dados"],
    },
    "outro": {
        "phase_order": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
        "rationale": (
            "A trilha começa pela base do primeiro salário e avança conforme "
            "você constrói evidências de aprendizagem."
        ),
        "focus_areas": ["Fundamentos", "Orçamento", "Decisões financeiras"],
    },
}

# Ajustes por contexto de vida. Só se aplicam quando o objetivo não tem uma
# ordem própria mais específica (primeiro salário ou outro).
# A trilha 12 (Desafio integrador) é sempre mantida ao final.
LIFE_CONTEXT_RULES: dict[str, dict] = {
    "primeiro_emprego": {
        "phase_order": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
        "rationale": "Seu primeiro emprego pede uma base clara sobre salário, descontos e orçamento.",
    },
    "ja_trabalho": {
        "phase_order": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
        "rationale": "Como você já trabalha, a trilha organiza a renda atual e aprofunda as decisões do dia a dia.",
    },
    "autonomo_freelancer": {
        "phase_order": [2, 6, 3, 1, 5, 4, 7, 8, 9, 10, 11, 12],
        "rationale": "Sua renda variável pede atenção primeiro ao orçamento, separação do dinheiro e meios de pagamento antes de aprofundar crédito.",
    },
    "estudante_sem_renda": {
        "phase_order": [5, 6, 1, 2, 3, 4, 7, 8, 9, 10, 11, 12],
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

    A ordem só é aceita se contiver exatamente todas as trilhas ativas, uma vez
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
        # crédito vêm antes de aprofundar investimentos. A trilha 12 permanece última.
        if phase_order[0] not in {5, 6, 7, 8}:
            phase_order = [5, 6, 1, 2, 3, 4, 7, 8, 9, 10, 11, 12]
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


# ─────────────────────────────────────────────
# Onboarding conversacional via Orchestrate (Sub-tarefa 4)
# ─────────────────────────────────────────────

VALID_TRAIL_MODES = {"express", "standard", "full"}


@dataclass
class CatalystOnboardingReply:
    """Resultado do onboarding conduzido pelo Catalisador.

    Produzido pela IA quando ORCHESTRATE_ENABLED=true, ou pelo fallback
    determinístico quando desativado ou em caso de erro.
    """
    phase_order: list[int]                    # sempre [1..12]
    trail_modes: dict[str, str]               # ex: {"1": "express", "2": "standard"}
    trail_1_auto_concluded: bool
    rationale: str
    next_message: str
    source: str = "ai"                        # "ai" ou "fallback"
    focus_areas: list[str] = field(default_factory=list)


@dataclass
class AdaptiveQuestionsReply:
    """Perguntas adaptativas do onboarding (D-C1).

    O Catalisador gera até 8 perguntas abertas a partir das respostas fixas.
    """
    questions: list[str] = field(default_factory=list)
    source: str = "fallback"  # "ai" ou "fallback"


def _fallback_adaptive_questions(fixed_answers: dict) -> list[str]:
    """Perguntas adaptativas determinísticas quando a IA não está disponível."""
    difficulty = fixed_answers.get("main_difficulty") or ""
    goal_12m = fixed_answers.get("goal_12m") or ""
    life_context = fixed_answers.get("life_context") or ""
    goal_category = fixed_answers.get("goal_category") or fixed_answers.get("objetivo") or ""

    questions: list[str] = []
    if goal_12m:
        questions.append(
            f"O que precisa acontecer para você sentir que está mais perto de {goal_12m}?"
        )
    else:
        questions.append(
            "O que você gostaria de conseguir fazer com o seu dinheiro nos próximos 12 meses?"
        )

    if difficulty:
        questions.append(
            f"O que você já tentou para lidar com {difficulty}?"
        )
    else:
        questions.append("Como você organiza seus gastos hoje?")

    if life_context == "estudante_sem_renda":
        questions.append(
            "Como você pretende organizar o dinheiro quando começar a receber?"
        )
    elif life_context == "autonomo_freelancer":
        questions.append(
            "Como você lida com a variação de renda entre os meses?"
        )
    elif goal_category == "investimentos":
        questions.append(
            "Você já investiu em algo? O que funcionou e o que não funcionou?"
        )
    else:
        questions.append(
            "Qual é a decisão financeira que você mais adia hoje?"
        )

    return questions[:3]


def _fallback_onboarding(
    fixed_answers: dict,
) -> CatalystOnboardingReply:
    """Fallback determinístico baseado nas respostas fixas do onboarding."""
    knowledge_level = fixed_answers.get("knowledge_level_declared") or "beginner"
    life_context = fixed_answers.get("life_context") or ""
    goal_category = fixed_answers.get("objetivo") or "outro"

    # Determina trail_1_auto_concluded: apenas quando há trabalho formal declarado.
    trail_1_auto_concluded = life_context in {"ja_trabalho", "primeiro_emprego"}

    # Modo das trilhas baseado no knowledge_level declarado.
    if knowledge_level == "advanced":
        default_mode = "express"
    elif knowledge_level == "beginner":
        default_mode = "full"
    else:
        default_mode = "standard"

    trail_modes = {str(i): default_mode for i in range(1, 13)}
    # Trilha 1 em express se auto-concluída (usuário já tem a base).
    if trail_1_auto_concluded:
        trail_modes["1"] = "express"

    # Rationale a partir do objetivo.
    rule = TRAIL_RULES.get(goal_category, TRAIL_RULES["outro"])
    rationale = rule["rationale"]
    focus_areas = list(rule.get("focus_areas", []))

    next_message = (
        "Sua jornada está pronta! Você já domina o básico do contracheque — "
        "vamos direto para o que vai fazer diferença agora."
        if trail_1_auto_concluded
        else "Sua trilha personalizada está pronta. Vamos começar!"
    )

    return CatalystOnboardingReply(
        phase_order=list(DEFAULT_PHASE_ORDER),
        trail_modes=trail_modes,
        trail_1_auto_concluded=trail_1_auto_concluded,
        rationale=rationale,
        next_message=next_message,
        source="fallback",
        focus_areas=focus_areas,
    )


async def conduct_onboarding(
    db: AsyncSession,
    fixed_answers: dict,
    conversation_history: list[dict],
) -> CatalystOnboardingReply:
    """Conduz o onboarding via Catalisador IA ou fallback determinístico.

    Quando catalyst_enabled=true: chama `prisma_catalyst` via Orchestrate
    com o payload documentado em `docs/AGENTES_INTEGRACAO_ORCHESTRATE.md` §5.1.

    Quando desativado ou em caso de erro: retorna fallback determinístico
    baseado em `build_trail()` com source="fallback".

    O banco não é tocado aqui — o chamador é responsável por persistir o
    resultado via `apply_generated_trail()`.
    """
    if not settings.catalyst_enabled or not settings.orchestrate_url:
        return _fallback_onboarding(fixed_answers)

    agent_id = settings.orchestrate_catalyst_agent_id
    if not agent_id:
        logger.warning("ORCHESTRATE_CATALYST_AGENT_ID não configurado; usando fallback.")
        return _fallback_onboarding(fixed_answers)

    payload = {
        "agent": "catalyst",
        "action": "onboarding",
        "fixed_answers": fixed_answers,
        "conversation_history": conversation_history,
    }

    try:
        data = await chat_completion(
            agent_id=agent_id,
            payload=payload,
            timeout=20.0,
        )
    except OrchestrateError as exc:
        logger.warning("Catalisador onboarding indisponível: %s — %s", exc.__class__.__name__, exc.detail)
        return _fallback_onboarding(fixed_answers)

    parsed = extract_agent_json(data)
    if not parsed or not validate_catalyst_onboarding_response(parsed):
        logger.warning("Catalisador onboarding respondeu sem JSON válido: %s", list(data.keys()))
        return _fallback_onboarding(fixed_answers)

    # Valida e normaliza os campos do JSON retornado pelo agente.
    phases = await get_active_phases(db)
    available = {phase.number for phase in phases}
    phase_order = validate_phase_order(parsed.get("phase_order"), available)
    if not phase_order:
        logger.warning("Catalisador onboarding devolveu phase_order inválido; usando fallback.")
        return _fallback_onboarding(fixed_answers)

    raw_modes = parsed.get("trail_modes") or {}
    trail_modes: dict[str, str] = {}
    for i in range(1, 13):
        key = str(i)
        mode = raw_modes.get(key, "standard")
        trail_modes[key] = mode if mode in VALID_TRAIL_MODES else "standard"

    return CatalystOnboardingReply(
        phase_order=phase_order,
        trail_modes=trail_modes,
        trail_1_auto_concluded=bool(parsed.get("trail_1_auto_concluded", False)),
        rationale=parsed.get("rationale") or "Trilha sugerida pelo Catalisador.",
        next_message=parsed.get("next_message") or "Sua trilha está pronta!",
        source="ai",
        focus_areas=parsed.get("focus_areas") or [],
    )


async def generate_adaptive_questions(
    fixed_answers: dict,
    conversation_history: list[dict],
) -> AdaptiveQuestionsReply:
    """Gera até 8 perguntas adaptativas a partir das respostas fixas (D-C1).

    A IA recebe as respostas fixas e o histórico; o backend limita a quantidade
    e valida o formato. Em falha, devolve perguntas determinísticas.
    """
    if not settings.catalyst_enabled or not settings.orchestrate_url:
        return AdaptiveQuestionsReply(
            questions=_fallback_adaptive_questions(fixed_answers),
            source="fallback",
        )

    agent_id = settings.orchestrate_catalyst_agent_id
    if not agent_id:
        return AdaptiveQuestionsReply(
            questions=_fallback_adaptive_questions(fixed_answers),
            source="fallback",
        )

    payload = {
        "agent": "catalyst",
        "action": "adaptive_questions",
        "fixed_answers": fixed_answers,
        "conversation_history": conversation_history,
        "max_questions": 8,
    }

    try:
        data = await chat_completion(
            agent_id=agent_id,
            payload=payload,
            timeout=15.0,
        )
    except OrchestrateError as exc:
        logger.warning(
            "Catalisador adaptive_questions indisponível: %s — %s",
            exc.__class__.__name__,
            exc.detail,
        )
        return AdaptiveQuestionsReply(
            questions=_fallback_adaptive_questions(fixed_answers),
            source="fallback",
        )

    parsed = extract_agent_json(data)
    raw_questions = parsed.get("questions") if isinstance(parsed, dict) else None
    if not isinstance(raw_questions, list):
        logger.warning(
            "Catalisador adaptive_questions respondeu sem JSON válido: %s",
            list(data.keys()),
        )
        return AdaptiveQuestionsReply(
            questions=_fallback_adaptive_questions(fixed_answers),
            source="fallback",
        )

    questions: list[str] = []
    for question in raw_questions:
        if not isinstance(question, str):
            continue
        cleaned = question.strip()
        if cleaned and cleaned not in questions:
            questions.append(cleaned)

    if not questions:
        return AdaptiveQuestionsReply(
            questions=_fallback_adaptive_questions(fixed_answers),
            source="fallback",
        )

    return AdaptiveQuestionsReply(questions=questions[:8], source="ai")


async def apply_generated_trail(
    db: AsyncSession,
    user_id: int,
    generated: dict,
    *,
    source: str = "ai",
) -> dict:
    """Ponto de entrada para uma trilha gerada pelo Catalisador IA.

    O agente propõe `phase_order`, `rationale`, `focus_areas`, `trail_modes` e
    `trail_1_auto_concluded`; o backend valida a ordem contra as trilhas ativas
    e só então persiste. Uma trilha inválida é rejeitada com `ValueError` —
    nunca desbloqueia fases por engano.
    """
    phases = await get_active_phases(db)
    available = {phase.number for phase in phases}
    order = validate_phase_order(generated.get("phase_order"), available)
    if not order:
        raise ValueError("Ordem de trilhas inválida para a trilha.")

    result = await db.execute(select(Profile).where(Profile.user_id == user_id))
    profile = result.scalar_one_or_none()
    if not profile:
        raise ValueError("Perfil não encontrado.")

    # Normaliza trail_modes: garante que só valores válidos sejam persistidos.
    raw_modes = generated.get("trail_modes") or {}
    trail_modes: dict[str, str] = {}
    for i in range(1, 13):
        key = str(i)
        mode = raw_modes.get(key, "standard")
        trail_modes[key] = mode if mode in VALID_TRAIL_MODES else "standard"

    profile.trail = {
        **generated,
        "source": source,
        "version": generated.get("version", 2),
        "phase_order": order,
        "trail_modes": trail_modes,
        "trail_1_auto_concluded": bool(generated.get("trail_1_auto_concluded", False)),
        "rationale": generated.get("rationale") or "Trilha sugerida pelo Catalisador.",
        "focus_areas": generated.get("focus_areas") or [],
        "pace": generated.get("pace") or "steady",
        "generated_at": datetime.now(timezone.utc).isoformat(),
    }
    await db.flush()
    view = await get_trail_view(db, user_id)
    return view or profile.trail


# ─────────────────────────────────────────────
# Sub-tarefa 7 — modos de profundidade de trilha
# ─────────────────────────────────────────────

def get_trail_mode(profile: Profile, trail_id: int) -> str:
    """Retorna o modo de profundidade da trilha para o perfil dado.

    Lê `trail_modes` do JSONB `profiles.trail`. Valores válidos: express,
    standard, full. Padrão para `standard` quando ausente ou inválido.
    """
    if not profile or not profile.trail:
        return "standard"
    trail_modes = profile.trail.get("trail_modes") or {}
    mode = trail_modes.get(str(trail_id), "standard")
    return mode if mode in VALID_TRAIL_MODES else "standard"


# ─────────────────────────────────────────────
# Sub-tarefa 5 — presença contínua e celebração
# ─────────────────────────────────────────────

def _fallback_recommendation(
    *,
    trail: dict | None,
    mission_name: str | None,
    mission_id: int | None,
    phase_number: int | None,
    phase_name: str | None,
    is_in_progress: bool,
    has_mission: bool,
    reinforcement_topics: list[str],
    trail_position: int | None,
    trail_size: int | None,
    analyst_signals: list[dict] | None = None,
) -> dict:
    """Recomendação determinística — usada como fallback quando o Catalisador IA
    está desativado ou indisponível."""
    if not has_mission:
        return {
            "kind": "complete",
            "message": (
                "Você concluiu o que está disponível nesta trilha. Seu progresso "
                "está salvo; as próximas trilhas entram quando o conteúdo for publicado."
            ),
            "mission_id": None,
            "mission_name": None,
            "phase_number": None,
            "phase_name": None,
            "trail_position": trail_position,
            "trail_size": trail_size,
        }

    signal_types = {
        signal.get("tipo") for signal in (analyst_signals or [])
    }
    if "trail_1_review" in signal_types:
        return {
            "kind": "trail_1_review",
            "message": (
                "Percebi uma dificuldade recorrente em competências da Trilha 1. "
                "Que tal revisar o contracheque antes de seguir?"
            ),
            "mission_id": mission_id,
            "mission_name": mission_name,
            "phase_number": phase_number,
            "phase_name": phase_name,
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
        message = f"Retome \"{mission_name}\" de onde parou. Cada etapa concluída fica salva."
        kind = "continue"
    elif trail and trail.get("source") != "standard" and trail_position == 1:
        message = (
            f"Sua trilha começa por {phase_name}. {trail.get('rationale', '')}".strip()
        )
        kind = "start"
    elif phase_number:
        message = (
            f"O próximo passo é \"{mission_name}\", na trilha {phase_number}. "
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


async def build_recommendation(
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
    completed_trails: list[int] | None = None,
    current_trail: int | None = None,
    last_session_hours_ago: int | None = None,
    analyst_signals: list[dict] | None = None,
) -> dict:
    """Mensagem do Catalisador para o próximo passo.

    Quando `catalyst_enabled=true`: chama `prisma_catalyst` via Orchestrate
    com o payload documentado em `docs/AGENTES_INTEGRACAO_ORCHESTRATE.md` §5.2.
    Retorna 5 tipos: start | continue | review | celebrate | trail_1_review.

    Quando desativado ou em erro: fallback determinístico
    (tipos: start | continue | review | complete).
    """
    reinforcement_topics = reinforcement_topics or []

    def _fb():
        return _fallback_recommendation(
            trail=trail,
            mission_name=mission_name,
            mission_id=mission_id,
            phase_number=phase_number,
            phase_name=phase_name,
            is_in_progress=is_in_progress,
            has_mission=has_mission,
            reinforcement_topics=reinforcement_topics,
            trail_position=trail_position,
            trail_size=trail_size,
            analyst_signals=analyst_signals,
        )

    if not settings.catalyst_enabled or not settings.orchestrate_url:
        return _fb()

    agent_id = settings.orchestrate_catalyst_agent_id
    if not agent_id:
        logger.warning("ORCHESTRATE_CATALYST_AGENT_ID não configurado; usando fallback.")
        return _fb()

    payload = {
        "agent": "catalyst",
        "action": "next_step",
        "user_context": {
            "personal_goal": trail.get("rationale") if trail else None,
            "trail_modes": trail.get("trail_modes") if trail else {},
            "trail_1_auto_concluded": trail.get("trail_1_auto_concluded", False) if trail else False,
        },
        "progress": {
            "completed_trails": completed_trails or [],
            "current_trail": current_trail or phase_number,
            "current_mission": mission_id,
            "last_session_hours_ago": last_session_hours_ago,
        },
        "analyst_signals": analyst_signals or [],
        "reinforcement_topics": reinforcement_topics,
    }

    try:
        data = await chat_completion(
            agent_id=agent_id,
            payload=payload,
            timeout=8.0,
        )
    except OrchestrateError as exc:
        logger.warning("Catalisador next_step indisponível: %s — %s", exc.__class__.__name__, exc.detail)
        return _fb()

    parsed = extract_agent_json(data)
    if not parsed or not validate_catalyst_next_step_response(parsed):
        logger.warning("Catalisador next_step respondeu sem JSON válido: %s", list(data.keys()))
        return _fb()

    valid_kinds = {"start", "continue", "review", "celebrate", "trail_1_review", "complete"}
    kind = parsed.get("tipo") or parsed.get("kind") or "start"
    if kind not in valid_kinds:
        kind = "start"

    return {
        "kind": kind,
        "message": parsed.get("mensagem") or parsed.get("message") or "Seu próximo passo está pronto.",
        "mission_id": parsed.get("missao_id") or mission_id,
        "mission_name": mission_name,
        "phase_number": parsed.get("trilha_id") or phase_number,
        "phase_name": phase_name,
        "trail_position": trail_position,
        "trail_size": trail_size,
        "rationale": parsed.get("rationale"),
    }


async def celebrate_trail_completion(
    db: AsyncSession,
    user_id: int,
    trail_id: int,
    trail_name: str,
    analyst_synthesis: dict | None = None,
    next_trail_id: int | None = None,
    next_trail_name: str | None = None,
) -> dict:
    """Mensagem de celebração do Catalisador ao concluir uma trilha.

    Quando `ORCHESTRATE_ENABLED=true`: chama `prisma_catalyst` com síntese do
    Analista e informações da próxima trilha (payload §5.3 da documentação).

    Quando desativado ou em erro: retorna mensagem determinística.
    """
    fallback_message = (
        f"Parabéns! Você concluiu a trilha \"{trail_name}\". "
        "Cada missão completada aqui fortalece sua base financeira."
    )
    fallback = {
        "kind": "celebrate",
        "message": fallback_message,
        "celebration_message": fallback_message,
        "next_step_message": (
            "A próxima trilha já está disponível quando você quiser continuar."
            if not next_trail_name
            else f"Agora vem \"{next_trail_name}\" — a continuação natural do que você aprendeu."
        ),
        "badge_label": f"{trail_name} — concluída",
        "source": "fallback",
    }

    if not settings.catalyst_enabled or not settings.orchestrate_url:
        return fallback

    agent_id = settings.orchestrate_catalyst_agent_id
    if not agent_id:
        return fallback

    payload = {
        "agent": "catalyst",
        "action": "celebrate_trail",
        "trail_id": trail_id,
        "trail_name": trail_name,
        "analyst_synthesis": analyst_synthesis or {},
        "next_trail": (
            {"id": next_trail_id, "name": next_trail_name}
            if next_trail_id
            else None
        ),
    }

    try:
        data = await chat_completion(
            agent_id=agent_id,
            payload=payload,
            timeout=settings.orchestrate_timeout_seconds,
        )
    except OrchestrateError as exc:
        logger.warning("Catalisador celebrate_trail indisponível: %s — %s", exc.__class__.__name__, exc.detail)
        return fallback

    parsed = extract_agent_json(data)
    if not parsed or not validate_catalyst_celebrate_response(parsed):
        logger.warning("Catalisador celebrate_trail respondeu sem JSON válido: %s", list(data.keys()))
        return fallback

    celebration_message = (
        parsed.get("celebration_message") or fallback["celebration_message"]
    )
    return {
        "kind": "celebrate",
        "message": celebration_message,
        "celebration_message": celebration_message,
        "next_step_message": parsed.get("next_step_message") or fallback["next_step_message"],
        "badge_label": parsed.get("badge_label") or fallback["badge_label"],
        "source": "ai",
    }
