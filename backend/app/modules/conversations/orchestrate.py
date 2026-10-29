"""Ponto único de integração do Mentor com o watsonx Orchestrate.

Quando `ORCHESTRATE_ENABLED=true` (ou `ORCHESTRATE_MENTOR_ENABLED=true`),
envia o payload pedagógico ao agente `prisma_mentor` no Orchestrate e mapeia
a resposta para `MentorReply`.

Quando desativado ou em caso de falha, devolve um fallback explícito com o
mesmo contrato — o dia da conexão é uma troca de implementação, não uma
reescrita do chat, do banco ou da UI.
"""
from __future__ import annotations

from dataclasses import dataclass, field

from app.core.config import settings
from app.core.logging import logger
from app.core.orchestrate_client import (
    OrchestrateError,
    chat_completion,
)
from app.core.orchestrate_parser import (
    extract_agent_content,
    extract_agent_json,
    extract_thread_id,
)

MENTOR_PLACEHOLDER = (
    "O Mentor ainda está em preparação — a integração com a IA não foi ativada. "
    "Sua mensagem foi salva. Enquanto isso, o conteúdo de apoio de cada missão "
    "continua disponível nas etapas de leitura."
)

DEFAULT_SUGGESTIONS = [
    "Explique esse conceito com um exemplo.",
    "Por que a minha resposta não estava completa?",
    "Como isso aparece no meu dia a dia?",
]


@dataclass
class MentorReply:
    content: str
    status: str  # available | preparing | unavailable
    suggestions: list[str] = field(default_factory=lambda: list(DEFAULT_SUGGESTIONS))
    source: str = "fallback"
    detail: str | None = None
    thread_id: str | None = None


def _fallback(status: str, detail: str | None = None) -> MentorReply:
    return MentorReply(
        content=MENTOR_PLACEHOLDER,
        status=status,
        suggestions=list(DEFAULT_SUGGESTIONS),
        source="fallback",
        detail=detail,
    )


async def request_mentor_reply(
    payload: dict,
    *,
    thread_id: str | None = None,
) -> MentorReply:
    """Envia o payload do backend ao agente Mentor no Orchestrate.

    Contrato de entrada (documentado em `docs/AGENTES_INTEGRACAO_ORCHESTRATE.md`
    seção 3.3): `agent`, `conversation_id`, `user_context`, `learning_context`,
    `messages`, `message`.

    Contrato de saída: o agente responde JSON com `content` (campo primário),
    `suggestions` (lista opcional) e `thread_id` (para multi-turn).

    Status de retorno:
    - `preparing`   — mentor desligado por flag
    - `available`   — Orchestrate respondeu com conteúdo válido
    - `unavailable` — erro, timeout ou resposta sem conteúdo textual utilizável
    """
    if not settings.mentor_enabled or not settings.orchestrate_url:
        return _fallback("preparing")

    agent_id = settings.orchestrate_agent_mentor_id
    if not agent_id:
        logger.warning("ORCHESTRATE_AGENT_MENTOR_ID não configurado; usando fallback.")
        return _fallback("preparing", detail="missing_agent_id")

    try:
        data = await chat_completion(
            agent_id=agent_id,
            payload=payload,
            thread_id=thread_id,
            timeout=15.0,
        )
    except OrchestrateError as exc:
        logger.warning("Mentor indisponível: %s — %s", exc.__class__.__name__, exc.detail)
        return _fallback("unavailable", detail=exc.__class__.__name__)

    # Tenta extrair JSON estruturado (com content + suggestions).
    parsed = extract_agent_json(data)
    if parsed:
        content = parsed.get("content") or parsed.get("text") or ""
        suggestions = parsed.get("suggestions")
    else:
        content = extract_agent_content(data) or ""
        suggestions = None

    if not content:
        logger.warning("Mentor respondeu sem conteúdo textual utilizável: %s", list(data.keys()))
        return _fallback("unavailable", detail="empty_response")

    if not isinstance(suggestions, list) or not suggestions:
        suggestions = list(DEFAULT_SUGGESTIONS)

    return MentorReply(
        content=content,
        status="available",
        suggestions=suggestions,
        source="orchestrate",
        thread_id=extract_thread_id(data),
    )
