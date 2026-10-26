"""Analista de Progresso — recomendações determinísticas no MVP.

O Analista real roda em background no watsonx Orchestrate. Enquanto a
integração não está disponível, este módulo transforma as evidências já
calculadas pelo backend em uma recomendação curta, objetiva e sem julgamento.
O estudante nunca vê a análise bruta — apenas a sugestão de ação.
"""
from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.shared.models import Competency, UserCompetencyProgress


def build_insight_from_competencies(
    competencies: list[dict],
    *,
    scope: str = "mission",
) -> dict | None:
    """Monta a recomendação visível a partir de evidências já calculadas.

    Formato aprovado (D14): 1 frase sobre a dificuldade observada + 1 frase
    com a sugestão de ação.
    """
    if not competencies:
        return None

    reinforcement = [
        item for item in competencies if item.get("reinforcement_suggested")
    ]
    if reinforcement:
        names = [item["name"] for item in reinforcement]
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

    demonstrated = [
        item for item in competencies if item.get("status") == "demonstrated"
    ]
    if demonstrated:
        names = [item["name"] for item in demonstrated]
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

    developing = [
        item for item in competencies if item.get("status") == "developing"
    ]
    if developing:
        names = [item["name"] for item in developing]
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
    rows = await _mission_competency_rows(db, user_id, mission_id)
    return build_insight_from_competencies(rows, scope="mission")


async def overall_insight(db: AsyncSession, user_id: int) -> dict | None:
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
    return build_insight_from_competencies(rows, scope="overall")


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
