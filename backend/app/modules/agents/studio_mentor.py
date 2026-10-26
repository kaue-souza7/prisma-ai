"""Mentor de Estúdio — ponto único de integração da geração de conteúdo.

Enquanto o watsonx Orchestrate não estiver ativo, o Estúdio não gera conteúdo:
o router devolve uma mensagem honesta e não consome Prismas. Este módulo já
define, porém, o contrato de entrada e a validação de saída para que a troca
para a IA real seja apenas uma implementação de `call_orchestrate`.
"""
from __future__ import annotations

from app.core.logging import logger

STUDIO_UNAVAILABLE_MESSAGE = (
    "O Estúdio estará disponível assim que o Mentor for ativado. "
    "Continue acumulando suas Prismas."
)

STUDIO_FORMATS = ("revisao", "flashcards", "exercicios")


def build_studio_payload(
    *,
    format: str,
    phase,
    mission,
    style_hint: str | None,
    competencies: list[dict],
    content_items: list[dict],
    profile,
) -> dict:
    """Monta o payload que o Orchestrate receberá.

    O backend é a autoridade: apenas conteúdo aprovado do módulo/fase entra no
    payload. A IA nunca consulta o banco diretamente.
    """
    return {
        "format": format,
        "phase_number": phase.number,
        "mission_number": mission.number if mission else None,
        "style_hint": style_hint,
        "competencies": [
            {
                "code": item.get("code"),
                "name": item.get("name"),
                "status": item.get("status", "not_started"),
            }
            for item in competencies
        ],
        "content_items": [
            {"title": item.get("title"), "body": item.get("body")}
            for item in content_items
        ],
        "user_goal": profile.personal_goal if profile else None,
        "knowledge_level": profile.knowledge_level if profile else None,
    }


def build_fallback_content(
    format: str,
    phase_name: str,
    mission_name: str | None,
) -> dict:
    """Conteúdo estruturado de fallback, sem simular uma resposta de IA."""
    scope = mission_name or phase_name
    base = {
        "type": format,
        "message": STUDIO_UNAVAILABLE_MESSAGE,
        "generated_by": "fallback",
    }
    if format == "revisao":
        return {
            **base,
            "title": f"Revisão de {scope}",
            "sections": [],
            "summary": [],
        }
    if format == "flashcards":
        return {**base, "cards": []}
    if format == "exercicios":
        return {**base, "questions": []}
    raise ValueError("formato_desconhecido")


async def call_orchestrate(payload: dict) -> dict:
    """Chamada real ao Orchestrate (Etapa 2).

    Contrato esperado por formato:
    - revisao: {type, title, sections:[{title, body}], summary:[str]}
    - flashcards: {type, cards:[{front, back}]}
    - exercicios: {type, questions:[{prompt, options, correct_answer,
      feedback_correct, feedback_incorrect, competency_codes}]}
    """
    raise NotImplementedError(STUDIO_UNAVAILABLE_MESSAGE)


def validate_generated_content(format: str, content: dict) -> dict:
    """Valida a estrutura mínima antes de persistir conteúdo gerado."""
    if not isinstance(content, dict) or content.get("type") != format:
        raise ValueError("estrutura_invalida")

    if format == "revisao":
        sections = content.get("sections")
        summary = content.get("summary")
        if not isinstance(sections, list) or not sections:
            raise ValueError("estrutura_invalida")
        if not isinstance(summary, list):
            raise ValueError("estrutura_invalida")
        for section in sections:
            if not isinstance(section, dict) or not section.get("title") or not section.get("body"):
                raise ValueError("estrutura_invalida")
        if not all(isinstance(item, str) for item in summary):
            raise ValueError("estrutura_invalida")

    elif format == "flashcards":
        cards = content.get("cards")
        if not isinstance(cards, list) or not cards:
            raise ValueError("estrutura_invalida")
        for card in cards:
            if not isinstance(card, dict) or not card.get("front") or not card.get("back"):
                raise ValueError("estrutura_invalida")

    elif format == "exercicios":
        questions = content.get("questions")
        if not isinstance(questions, list) or not questions:
            raise ValueError("estrutura_invalida")
        for question in questions:
            if not isinstance(question, dict) or not question.get("prompt"):
                raise ValueError("estrutura_invalida")
            options = question.get("options")
            # Questões objetivas exigem alternativas e gabarito. Sem
            # alternativas, a questão é tratada como resposta aberta.
            if options:
                if not isinstance(options, list) or len(options) < 2:
                    raise ValueError("estrutura_invalida")
                if not question.get("correct_answer"):
                    raise ValueError("estrutura_invalida")
            if not isinstance(question.get("competency_codes", []), list):
                raise ValueError("estrutura_invalida")

    else:
        raise ValueError("formato_desconhecido")

    return content


def log_orchestrate_failure(exc: Exception) -> None:
    logger.warning("Geração do Estúdio indisponível: %s", exc.__class__.__name__)
