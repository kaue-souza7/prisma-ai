"""Ponto único de integração do Mentor com o watsonx Orchestrate.

Enquanto o spike D7 não estiver concluído, este módulo não faz chamada de IA.
Ele devolve um fallback explícito e honesto, com o mesmo contrato que a
integração real usará. Assim, o dia da conexão é uma troca de implementação —
não uma reescrita do chat, do banco ou da UI.
"""
from __future__ import annotations

from dataclasses import dataclass, field

import httpx

from app.core.config import settings
from app.core.logging import logger

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


def _fallback(status: str, detail: str | None = None) -> MentorReply:
    return MentorReply(
        content=MENTOR_PLACEHOLDER,
        status=status,
        suggestions=list(DEFAULT_SUGGESTIONS),
        source="fallback",
        detail=detail,
    )


async def request_mentor_reply(payload: dict) -> MentorReply:
    """Envia o payload do backend ao Mentor.

    Contrato de entrada (definido em `docs/AGENTES_INTEGRACAO_ORCHESTRATE.md`):
    objetivo, trilha, missão, competências com dificuldade, últimas mensagens.
    Contrato de saída esperado do Orchestrate: `{ "content": "..." }` ou
    `{ "output": "..." }`. O mapeamento exato será ajustado no spike, sem
    alterar o restante da aplicação.
    """
    if not settings.orchestrate_enabled or not settings.orchestrate_url:
        return _fallback("preparing")

    headers = {"Content-Type": "application/json"}
    if settings.orchestrate_api_key:
        headers["Authorization"] = f"Bearer {settings.orchestrate_api_key}"

    try:
        async with httpx.AsyncClient(timeout=settings.orchestrate_timeout_seconds) as client:
            response = await client.post(
                settings.orchestrate_url,
                json=payload,
                headers=headers,
            )
            response.raise_for_status()
            data = response.json()
    except Exception as exc:  # noqa: BLE001 — fallback nunca deve derrubar o chat
        logger.warning("Orchestrate indisponível: %s", exc.__class__.__name__)
        return _fallback("unavailable", detail=exc.__class__.__name__)

    content = data.get("content") or data.get("output") or data.get("response")
    if not isinstance(content, str) or not content.strip():
        logger.warning("Orchestrate respondeu sem conteúdo textual utilizável.")
        return _fallback("unavailable", detail="empty_response")

    return MentorReply(
        content=content.strip(),
        status="available",
        suggestions=list(data.get("suggestions") or DEFAULT_SUGGESTIONS),
        source="orchestrate",
    )
