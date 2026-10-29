"""Analista de Progresso — insights pedagógicos e síntese de trilha.

`build_insight_from_competencies()` chama o agente `prisma_analyst`
no Orchestrate em background quando `analyst_enabled=true`, com fallback
determinístico completo. `generate_trail_synthesis()` produz a síntese ao final
de cada trilha (D-A1).

Regra central: o Analista nunca altera pontos, conquistas ou desbloqueios.
Ele apenas lê evidências já calculadas pelo backend e produz recomendações.
"""
from __future__ import annotations

import asyncio
import time
from dataclasses import dataclass, field
from datetime import datetime, timezone

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.logging import logger
from app.core.orchestrate_client import OrchestrateError, chat_completion
from app.core.orchestrate_parser import (
    extract_agent_json,
    validate_analyst_insight_response,
    validate_analyst_synthesis_response,
)
from app.shared.models import (
    Competency,
    TrailSynthesisRecord,
    UserCompetencyProgress,
)


# ─────────────────────────────────────────────
# Sub-tarefa 6 — dataclasses de síntese
# ─────────────────────────────────────────────

@dataclass
class TrailSynthesisFull:
    competencies_demonstrated: list[str] = field(default_factory=list)
    competencies_with_difficulty: list[str] = field(default_factory=list)
    summary: str = ""
    reinforcement_suggestion: str | None = None


@dataclass
class TrailSynthesis:
    """Síntese produzida pelo Analista ao concluir uma trilha (D-A1).

    `short` — frase curta para o Catalisador usar na celebração.
    `full`  — card exibido no painel de progresso.
    """
    short: str
    full: TrailSynthesisFull
    source: str = "fallback"  # "ai" | "fallback"


# ─────────────────────────────────────────────
# Cache de insights (evita chamar o LLM a cada request)
# ─────────────────────────────────────────────

_INSIGHT_TTL_SECONDS = 300.0
_INSIGHT_CACHE: dict[tuple, tuple[float, dict | None]] = {}
_INSIGHT_REFRESH_TASKS: set[asyncio.Task] = set()


def _rows_signature(rows: list[dict]) -> tuple:
    """Assinatura estável das evidências; invalida o cache quando elas mudam."""
    return tuple(
        (
            row.get("code"),
            row.get("status"),
            row.get("correct_count"),
            row.get("incorrect_count"),
            row.get("reinforcement_suggested"),
        )
        for row in rows
    )


def _cache_get(key: tuple) -> tuple[dict | None, bool]:
    entry = _INSIGHT_CACHE.get(key)
    if not entry:
        return None, False
    created_at, value = entry
    if time.monotonic() - created_at > _INSIGHT_TTL_SECONDS:
        _INSIGHT_CACHE.pop(key, None)
        return None, False
    return value, True


def _cache_set(key: tuple, value: dict | None) -> None:
    if len(_INSIGHT_CACHE) > 1000:
        _INSIGHT_CACHE.clear()
    _INSIGHT_CACHE[key] = (time.monotonic(), value)


# ─────────────────────────────────────────────
# Helpers internos
# ─────────────────────────────────────────────

def _build_fallback_insight(competencies: list[dict]) -> dict | None:
    """Insight determinístico a partir de evidências já calculadas."""
    if not competencies:
        return None

    reinforcement = [c for c in competencies if c.get("reinforcement_suggested")]
    if reinforcement:
        names = [c["name"] for c in reinforcement]
        listed = ", ".join(names[:2])
        return {
            "agent": "analyst",
            "severity": "attention",
            "action": "review",
            "competencies": names,
            "message": (
                f"Percebi que {listed} apareceu com dificuldade em mais de uma "
                "atividade. Uma boa próxima ação é revisar esse ponto antes de seguir."
            ),
        }

    demonstrated = [c for c in competencies if c.get("status") == "demonstrated"]
    if demonstrated:
        names = [c["name"] for c in demonstrated]
        listed = ", ".join(names[:2])
        return {
            "agent": "analyst",
            "severity": "positive",
            "action": "advance",
            "competencies": names,
            "message": (
                f"Você demonstrou {listed} nesta etapa. Um bom próximo passo é "
                "aplicar o conceito em uma decisão real e seguir para a próxima missão."
            ),
        }

    developing = [c for c in competencies if c.get("status") == "developing"]
    if developing:
        names = [c["name"] for c in developing]
        listed = ", ".join(names[:2])
        return {
            "agent": "analyst",
            "severity": "neutral",
            "action": "continue",
            "competencies": names,
            "message": (
                f"Você está construindo {listed}. Revisar o conteúdo da missão "
                "antes de avançar pode consolidar o aprendizado."
            ),
        }

    return None


async def _request_analyst_insight(
    competencies: list[dict],
    scope: str,
    *,
    timeout: float = 8.0,
) -> dict | None:
    """Chama o agente Analista no Orchestrate em background.

    Retorna o insight estruturado ou None em qualquer falha — o chamador
    usa o fallback determinístico nesse caso.
    """
    if not settings.analyst_enabled or not settings.orchestrate_url:
        return None

    agent_id = settings.orchestrate_analyst_agent_id
    if not agent_id:
        return None

    payload = {
        "agent": "analyst",
        "action": "insight",
        "scope": scope,
        "competencies": competencies,
    }

    try:
        data = await chat_completion(
            agent_id=agent_id,
            payload=payload,
            timeout=min(timeout, settings.orchestrate_timeout_seconds),
        )
    except OrchestrateError as exc:
        logger.warning("Analista insight indisponível: %s — %s", exc.__class__.__name__, exc.detail)
        return None

    parsed = extract_agent_json(data)
    if parsed and validate_analyst_insight_response(parsed):
        return parsed

    logger.warning("Analista insight respondeu sem JSON válido: %s", list(data.keys()))
    return None


# ─────────────────────────────────────────────
# API pública
# ─────────────────────────────────────────────

def build_insight_from_competencies(
    competencies: list[dict],
    *,
    scope: str = "mission",
) -> dict | None:
    """Monta a recomendação visível a partir de evidências já calculadas.

    Esta função é síncrona e retorna o insight determinístico. Para a versão
    assíncrona com chamada ao Orchestrate em background, use
    `build_insight_from_competencies_async()`.

    Formato aprovado (D14): 1 frase sobre a dificuldade observada + 1 frase
    com a sugestão de ação.
    """
    return _build_fallback_insight(competencies)


async def build_insight_from_competencies_async(
    competencies: list[dict],
    *,
    scope: str = "mission",
    timeout: float = 8.0,
) -> dict | None:
    """Versão assíncrona de `build_insight_from_competencies`.

    Quando `ORCHESTRATE_ENABLED=true`: chama o agente Analista no Orchestrate
    em background. O resultado é awaited mas não bloqueia o fluxo principal —
    o chamador deve usar `asyncio.create_task()` se quiser comportamento
    verdadeiramente não-bloqueante.

    Em qualquer falha: retorna o insight determinístico.
    """
    ai_insight = await _request_analyst_insight(competencies, scope, timeout=timeout)
    if ai_insight:
        return {
            "agent": "analyst",
            "severity": ai_insight.get("severity", "neutral"),
            "action": ai_insight.get("action", "continue"),
            "competencies": ai_insight.get("competencies", []),
            "message": ai_insight.get("message", ""),
        }
    return _build_fallback_insight(competencies)


def build_reinforcement_insight(
    competency_names: list[str], attempt_number: int
) -> dict | None:
    """Sugestão imediata após erro repetido, sem revelar gabarito."""
    if not competency_names:
        return None
    if attempt_number < 2:
        return None
    listed = ", ".join(competency_names[:2])
    return {
        "agent": "analyst",
        "severity": "attention",
        "action": "review",
        "competencies": competency_names,
        "message": (
            f"Esse conceito apareceu com dificuldade: {listed}. Antes de tentar "
            "de novo, releia o trecho da missão e tente explicar com suas palavras."
        ),
    }


async def _mission_competency_rows(
    db: AsyncSession, user_id: int, mission_id: int
) -> list[dict]:
    result = await db.execute(
        select(UserCompetencyProgress, Competency)
        .join(Competency, UserCompetencyProgress.competency_id == Competency.id)
        .where(
            UserCompetencyProgress.user_id == user_id,
            Competency.mission_id == mission_id,
        )
        .order_by(Competency.code)
    )
    return [
        {
            "code": row.Competency.code,
            "name": row.Competency.name,
            "status": row.UserCompetencyProgress.status.value,
            "correct_count": row.UserCompetencyProgress.correct_count,
            "incorrect_count": row.UserCompetencyProgress.incorrect_count,
            "reinforcement_suggested": row.UserCompetencyProgress.reinforcement_suggested,
        }
        for row in result.all()
    ]


async def mission_insight(
    db: AsyncSession, user_id: int, mission_id: int
) -> dict | None:
    """Insight da missão com IA e fallback; cacheado por evidência."""
    rows = await _mission_competency_rows(db, user_id, mission_id)
    key = ("mission", user_id, mission_id, _rows_signature(rows))
    cached, found = _cache_get(key)
    if found:
        return cached

    insight = await build_insight_from_competencies_async(
        rows, scope="mission", timeout=8.0
    )
    _cache_set(key, insight)
    return insight


async def overall_insight(db: AsyncSession, user_id: int) -> dict | None:
    """Insight geral com IA em background e fallback imediato.

    O painel de progresso nunca espera o LLM: devolve o fallback (ou o cache)
    imediatamente e atualiza o cache em background.
    """
    result = await db.execute(
        select(UserCompetencyProgress, Competency)
        .join(Competency, UserCompetencyProgress.competency_id == Competency.id)
        .where(UserCompetencyProgress.user_id == user_id)
        .order_by(Competency.code)
    )
    rows = [
        {
            "code": row.Competency.code,
            "name": row.Competency.name,
            "status": row.UserCompetencyProgress.status.value,
            "correct_count": row.UserCompetencyProgress.correct_count,
            "incorrect_count": row.UserCompetencyProgress.incorrect_count,
            "reinforcement_suggested": row.UserCompetencyProgress.reinforcement_suggested,
        }
        for row in result.all()
    ]

    key = ("overall", user_id, _rows_signature(rows))
    cached, found = _cache_get(key)
    if found:
        return cached

    fallback = _build_fallback_insight(rows)
    _cache_set(key, fallback)

    async def _refresh() -> None:
        try:
            insight = await build_insight_from_competencies_async(
                rows, scope="overall", timeout=8.0
            )
            _cache_set(key, insight)
        except Exception as exc:  # noqa: BLE001 — nunca derruba o painel
            logger.warning("Analista overall refresh falhou: %s", exc.__class__.__name__)

    task = asyncio.create_task(_refresh())
    _INSIGHT_REFRESH_TASKS.add(task)
    task.add_done_callback(_INSIGHT_REFRESH_TASKS.discard)
    return fallback


async def reinforcement_topics(db: AsyncSession, user_id: int) -> list[str]:
    result = await db.execute(
        select(Competency.name)
        .join(
            UserCompetencyProgress,
            UserCompetencyProgress.competency_id == Competency.id,
        )
        .where(
            UserCompetencyProgress.user_id == user_id,
            UserCompetencyProgress.reinforcement_suggested == True,
        )
        .order_by(Competency.code)
    )
    return list(dict.fromkeys(result.scalars().all()))


async def competency_names_for_codes(
    db: AsyncSession, mission_id: int, codes: list[str]
) -> list[str]:
    if not codes:
        return []
    result = await db.execute(
        select(Competency.name).where(
            Competency.mission_id == mission_id,
            Competency.code.in_(codes),
        )
    )
    return list(result.scalars().all())


def _synthesis_from_record(record: TrailSynthesisRecord) -> TrailSynthesis:
    full = record.full or {}
    return TrailSynthesis(
        short=record.short,
        full=TrailSynthesisFull(
            competencies_demonstrated=full.get("competencies_demonstrated") or [],
            competencies_with_difficulty=full.get("competencies_with_difficulty") or [],
            summary=full.get("summary") or "",
            reinforcement_suggestion=full.get("reinforcement_suggestion"),
        ),
        source=record.source,
    )


async def get_cached_trail_synthesis(
    db: AsyncSession, user_id: int, trail_id: int
) -> TrailSynthesis | None:
    """Lê a síntese persistida da trilha, se existir."""
    result = await db.execute(
        select(TrailSynthesisRecord).where(
            TrailSynthesisRecord.user_id == user_id,
            TrailSynthesisRecord.trail_id == trail_id,
        )
    )
    record = result.scalar_one_or_none()
    return _synthesis_from_record(record) if record else None


async def invalidate_trail_synthesis(
    db: AsyncSession, user_id: int, trail_id: int
) -> None:
    """Remove a síntese cacheada para forçar atualização após novas evidências."""
    result = await db.execute(
        select(TrailSynthesisRecord).where(
            TrailSynthesisRecord.user_id == user_id,
            TrailSynthesisRecord.trail_id == trail_id,
        )
    )
    record = result.scalar_one_or_none()
    if record:
        await db.delete(record)
        await db.flush()


async def save_trail_synthesis(
    db: AsyncSession,
    user_id: int,
    trail_id: int,
    synthesis: TrailSynthesis,
) -> None:
    """Persiste ou atualiza a síntese da trilha (idempotente)."""
    result = await db.execute(
        select(TrailSynthesisRecord).where(
            TrailSynthesisRecord.user_id == user_id,
            TrailSynthesisRecord.trail_id == trail_id,
        )
    )
    record = result.scalar_one_or_none()
    full = {
        "competencies_demonstrated": synthesis.full.competencies_demonstrated,
        "competencies_with_difficulty": synthesis.full.competencies_with_difficulty,
        "summary": synthesis.full.summary,
        "reinforcement_suggestion": synthesis.full.reinforcement_suggestion,
    }
    if record:
        record.short = synthesis.short
        record.full = full
        record.source = synthesis.source
        record.generated_at = datetime.now(timezone.utc)
    else:
        db.add(
            TrailSynthesisRecord(
                user_id=user_id,
                trail_id=trail_id,
                short=synthesis.short,
                full=full,
                source=synthesis.source,
            )
        )
    await db.flush()


async def generate_trail_synthesis(
    db: AsyncSession,
    user_id: int,
    trail_id: int,
    *,
    use_cache: bool = True,
    allow_ai: bool = True,
    save: bool = True,
) -> TrailSynthesis:
    """Gera a síntese de competências ao final de uma trilha (D-A1).

    - `use_cache=True`: devolve a síntese persistida, se existir.
    - `allow_ai=False`: força o fallback determinístico (útil para resposta
      imediata enquanto a versão com IA roda em background).
    - `save=True`: persiste o resultado para as próximas consultas.
    """
    if use_cache:
        cached = await get_cached_trail_synthesis(db, user_id, trail_id)
        if cached:
            return cached

    # Coleta todas as competências da trilha (phase_id = trail_id)
    from app.shared.models import Mission

    missions_result = await db.execute(
        select(Mission).where(Mission.phase_id == trail_id)
    )
    missions = missions_result.scalars().all()
    mission_ids = [m.id for m in missions]

    if not mission_ids:
        synthesis = TrailSynthesis(
            short="Você concluiu esta trilha.",
            full=TrailSynthesisFull(),
            source="fallback",
        )
        if save:
            await save_trail_synthesis(db, user_id, trail_id, synthesis)
        return synthesis

    comp_result = await db.execute(
        select(UserCompetencyProgress, Competency)
        .join(Competency, UserCompetencyProgress.competency_id == Competency.id)
        .where(
            UserCompetencyProgress.user_id == user_id,
            Competency.mission_id.in_(mission_ids),
        )
        .order_by(Competency.code)
    )
    rows = comp_result.all()

    demonstrated_codes = [
        r.Competency.code for r in rows
        if r.UserCompetencyProgress.status.value == "demonstrated"
    ]
    difficulty_codes = [
        r.Competency.code for r in rows
        if r.UserCompetencyProgress.reinforcement_suggested
    ]

    # Tenta o agente Analista no Orchestrate.
    agent_id = settings.orchestrate_analyst_agent_id
    if allow_ai and settings.analyst_enabled and settings.orchestrate_url and agent_id:
        competencies_payload = [
            {
                "code": r.Competency.code,
                "name": r.Competency.name,
                "status": r.UserCompetencyProgress.status.value,
                "reinforcement_suggested": r.UserCompetencyProgress.reinforcement_suggested,
            }
            for r in rows
        ]
        payload = {
            "agent": "analyst",
            "action": "trail_synthesis",
            "trail_id": trail_id,
            "competencies": competencies_payload,
        }

        try:
            data = await chat_completion(
                agent_id=agent_id,
                payload=payload,
                timeout=min(10.0, settings.orchestrate_timeout_seconds),
            )
            parsed = extract_agent_json(data)
            if parsed and validate_analyst_synthesis_response(parsed):
                full_data = parsed.get("full") or {}
                synthesis = TrailSynthesis(
                    short=parsed.get("short") or "Você concluiu esta trilha.",
                    full=TrailSynthesisFull(
                        competencies_demonstrated=full_data.get("competencies_demonstrated") or demonstrated_codes,
                        competencies_with_difficulty=full_data.get("competencies_with_difficulty") or difficulty_codes,
                        summary=full_data.get("summary") or "",
                        reinforcement_suggestion=full_data.get("reinforcement_suggestion"),
                    ),
                    source="ai",
                )
                if save:
                    await save_trail_synthesis(db, user_id, trail_id, synthesis)
                return synthesis
            logger.warning("Analista trail_synthesis respondeu sem JSON válido: %s", list(data.keys()))
        except OrchestrateError as exc:
            logger.warning("Analista trail_synthesis indisponível: %s — %s", exc.__class__.__name__, exc.detail)

    # Fallback determinístico
    if demonstrated_codes:
        short = f"Você demonstrou {len(demonstrated_codes)} competência(s) nesta trilha."
    else:
        short = "Você concluiu esta trilha."

    synthesis = TrailSynthesis(
        short=short,
        full=TrailSynthesisFull(
            competencies_demonstrated=demonstrated_codes,
            competencies_with_difficulty=difficulty_codes,
            summary="",
            reinforcement_suggestion=(
                "Algumas competências podem ser consolidadas revisitando o conteúdo."
                if difficulty_codes else None
            ),
        ),
        source="fallback",
    )
    if save:
        await save_trail_synthesis(db, user_id, trail_id, synthesis)
    return synthesis


def has_trail_1_difficulty(competencies: list[dict], trail_1_codes_prefix: str = "1.") -> bool:
    """Detecta dificuldade recorrente em competências da Trilha 1.

    Usado para disparar o sinal `trail_1_review` no Catalisador — sinaliza
    que um usuário com `trail_1_auto_concluded=true` pode precisar revisitar
    a Trilha 1.
    """
    for comp in competencies:
        code = comp.get("code") or ""
        if code.startswith(trail_1_codes_prefix) and comp.get("reinforcement_suggested"):
            return True
    return False
