"""Avaliação imediata de respostas abertas pelo agente Mentor.

O backend continua sendo a autoridade: apenas o conteúdo aprovado da atividade
(critérios e enunciado) é enviado ao agente. O agente devolve um veredito
estruturado, que é validado antes de chegar ao estudante.
"""
from __future__ import annotations

from dataclasses import dataclass

from app.core.config import settings
from app.core.logging import logger
from app.core.orchestrate_client import OrchestrateError, chat_completion
from app.core.orchestrate_parser import extract_agent_json
from app.shared.models import Activity, Mission, Phase, Profile

VALID_VERDICTS = {"correct", "incorrect", "ambiguous"}
DEFAULT_CLARIFICATION = (
    "Pode complementar sua resposta com um exemplo ou explicar melhor o raciocínio?"
)


@dataclass(frozen=True)
class OpenTextEvaluation:
    verdict: str  # correct | incorrect | ambiguous | unavailable
    is_correct: bool | None
    feedback: str
    source: str = "fallback"


def _fallback(activity: Activity, detail: str | None = None) -> OpenTextEvaluation:
    if detail:
        logger.debug("Avaliação aberta em fallback: %s", detail)
    static = activity.content.get("feedback_static") or (
        "Sua resposta foi registrada. O Mentor não conseguiu avaliá-la agora."
    )
    return OpenTextEvaluation(
        verdict="unavailable",
        is_correct=None,
        feedback=static,
        source="fallback",
    )


def build_open_text_payload(
    *,
    activity: Activity,
    student_answer: str,
    mission: Mission,
    phase: Phase | None,
    profile: Profile | None,
) -> dict:
    """Monta o payload de avaliação usando somente dados aprovados da atividade."""
    content = activity.content
    return {
        "task": "evaluate_open_response",
        "instruction": (
            "Avalie a resposta aberta do estudante usando exclusivamente os "
            "critérios fornecidos. Responda somente um JSON válido, sem markdown, "
            "com as chaves verdict e feedback. Use verdict=correct quando a "
            "resposta atende aos critérios essenciais; incorrect quando não "
            "atende; ambiguous somente quando a resposta for curta ou vaga a "
            "ponto de não permitir uma avaliação segura. O feedback deve ser em "
            "português do Brasil, ter 1 a 3 frases curtas, explicar o que foi "
            "bem ou o que faltou e, se ambiguous, pedir uma complementação "
            "específica. Não revele os critérios literalmente, não invente fatos "
            "e não dê recomendação de investimento."
        ),
        "response_schema": {
            "verdict": "correct | incorrect | ambiguous",
            "feedback": "1 a 3 frases em português do Brasil",
        },
        "activity": {
            "prompt": content.get("prompt"),
            "evaluation_criteria": content.get("evaluation_criteria") or [],
            "competency_codes": content.get("competency_codes") or [],
        },
        "student_answer": student_answer,
        "mission": {
            "number": mission.number,
            "name": mission.name,
        },
        "phase": {
            "number": phase.number if phase else None,
            "name": phase.name if phase else None,
        },
        "user_context": {
            "personal_goal": profile.personal_goal if profile else None,
            "knowledge_level": profile.knowledge_level if profile else None,
        },
    }


def parse_open_text_evaluation(
    data: dict,
) -> OpenTextEvaluation | None:
    """Valida a resposta estruturada do agente.

    Retorna None quando o formato não é utilizável; o chamador decide o fallback.
    """
    verdict_raw = data.get("verdict")
    if isinstance(verdict_raw, bool):
        verdict = "correct" if verdict_raw else "incorrect"
    elif isinstance(verdict_raw, str):
        verdict = verdict_raw.strip().strip(".,:;!?").lower()
    else:
        return None
    if verdict not in VALID_VERDICTS:
        return None

    feedback_raw = data.get("feedback")
    if not isinstance(feedback_raw, str) or not feedback_raw.strip():
        if verdict == "ambiguous":
            feedback = DEFAULT_CLARIFICATION
        else:
            return None
    else:
        feedback = feedback_raw.strip()

    is_correct = {
        "correct": True,
        "incorrect": False,
        "ambiguous": None,
    }[verdict]

    return OpenTextEvaluation(
        verdict=verdict,
        is_correct=is_correct,
        feedback=feedback[:2000],
        source="orchestrate",
    )


async def evaluate_open_text(
    *,
    activity: Activity,
    student_answer: str,
    mission: Mission,
    phase: Phase | None,
    profile: Profile | None,
) -> OpenTextEvaluation:
    """Avalia uma resposta aberta com o Mentor, com fallback honesto."""
    if not settings.mentor_enabled or not settings.orchestrate_url:
        return _fallback(activity, detail="mentor_disabled")

    agent_id = settings.orchestrate_agent_mentor_id
    if not agent_id:
        logger.warning("ORCHESTRATE_AGENT_MENTOR_ID não configurado; usando fallback.")
        return _fallback(activity, detail="missing_agent_id")

    payload = build_open_text_payload(
        activity=activity,
        student_answer=student_answer,
        mission=mission,
        phase=phase,
        profile=profile,
    )

    try:
        data = await chat_completion(
            agent_id=agent_id,
            payload=payload,
            timeout=20.0,
        )
    except OrchestrateError as exc:
        logger.warning(
            "Avaliação de resposta aberta indisponível: %s — %s",
            exc.__class__.__name__,
            exc.detail,
        )
        return _fallback(activity, detail=exc.__class__.__name__)

    parsed = extract_agent_json(data)
    if not parsed:
        logger.warning("Mentor não retornou JSON de avaliação para resposta aberta.")
        return _fallback(activity, detail="invalid_response")

    evaluation = parse_open_text_evaluation(parsed)
    if not evaluation:
        logger.warning(
            "Mentor retornou avaliação inválida para resposta aberta (keys=%s).",
            list(parsed.keys()),
        )
        return _fallback(activity, detail="invalid_schema")

    return evaluation
