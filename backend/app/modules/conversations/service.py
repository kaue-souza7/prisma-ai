"""Serviço do chat do Mentor.

Persiste a conversa, monta o payload pedagógico e delega a resposta ao
adaptador do Orchestrate. Nenhuma regra de pontos, desbloqueio ou conclusão
passa por aqui.
"""
from __future__ import annotations

from datetime import datetime, timezone

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.shared.models import (
    Competency,
    Conversation,
    Mission,
    Phase,
    Profile,
    User,
)
from app.modules.agents import analyst
from app.modules.conversations import orchestrate

MAX_MESSAGE_LENGTH = 2000


async def _get_or_create_conversation(
    db: AsyncSession, user_id: int, agent: str, mission_id: int | None
) -> Conversation:
    result = await db.execute(
        select(Conversation).where(
            Conversation.user_id == user_id,
            Conversation.agent == agent,
            Conversation.mission_id == mission_id,
        )
    )
    conv = result.scalar_one_or_none()
    if not conv:
        now = datetime.now(timezone.utc)
        conv = Conversation(
            user_id=user_id,
            agent=agent,
            mission_id=mission_id,
            messages=[],
            created_at=now,
            updated_at=now,
        )
        db.add(conv)
        await db.flush()
    return conv


async def _mission_data(db: AsyncSession, mission_id: int | None) -> dict | None:
    if not mission_id:
        return None
    result = await db.execute(
        select(Mission, Phase)
        .join(Phase, Mission.phase_id == Phase.id)
        .where(Mission.id == mission_id)
    )
    row = result.first()
    if not row:
        return None
    mission, phase = row
    competencies_result = await db.execute(
        select(Competency)
        .where(Competency.mission_id == mission.id)
        .order_by(Competency.code)
    )
    competencies = list(competencies_result.scalars().all())
    return {
        "mission": mission,
        "phase": phase,
        "competencies": competencies,
    }


async def get_mentor_context(
    db: AsyncSession, user_id: int, mission_id: int | None = None
) -> dict:
    data = await _mission_data(db, mission_id)
    topics = await analyst.reinforcement_topics(db, user_id)
    profile_result = await db.execute(select(Profile).where(Profile.user_id == user_id))
    profile = profile_result.scalar_one_or_none()

    if data:
        mission = data["mission"]
        phase = data["phase"]
        competencies = data["competencies"]
        opening = (
            f"Estou com você no módulo {phase.number}.{mission.number} — "
            f"{mission.name}. Pode me perguntar sobre o conceito ou sobre o "
            "seu raciocínio; eu não entrego a resposta pronta, ajudo você a chegar nela."
        )
        if topics:
            opening += f" Notei que {topics[0]} apareceu com dificuldade — podemos começar por aí."
        suggestions = [
            (
                f"Me ajude a entender: {competencies[0].name}."
                if competencies
                else "Explique esse conceito com um exemplo."
            ),
            "Por que a minha resposta não estava completa?",
            "Como isso aparece no meu dia a dia?",
            "Me faça uma pergunta para testar se eu entendi.",
        ]
    else:
        opening = (
            "Pode me perguntar sobre qualquer conceito da sua jornada. "
            "Vou explicar com exemplos e fazer perguntas para ajudar você a pensar."
        )
        if topics:
            opening += f" Um ponto que merece atenção é {topics[0]}."
        suggestions = [
            "Como funciona juros compostos?",
            "Como organizar meu orçamento no começo do mês?",
            "Por que poupar antes de investir?",
            "Como identificar um golpe com Pix?",
        ]

    return {
        "mission_id": data["mission"].id if data else None,
        "mission_name": data["mission"].name if data else None,
        "phase_number": data["phase"].number if data else None,
        "phase_name": data["phase"].name if data else None,
        "opening_message": opening,
        "suggestions": suggestions,
        "status": "available" if settings.orchestrate_enabled and settings.orchestrate_url else "preparing",
        "personal_goal": profile.personal_goal if profile else None,
        "reinforcement_topics": topics,
    }


async def build_mentor_payload(
    db: AsyncSession,
    user: User,
    conversation: Conversation,
    content: str,
) -> dict:
    data = await _mission_data(db, conversation.mission_id)
    profile_result = await db.execute(select(Profile).where(Profile.user_id == user.id))
    profile = profile_result.scalar_one_or_none()
    topics = await analyst.reinforcement_topics(db, user.id)

    context = {
        "mission_id": None,
        "mission_name": None,
        "phase_number": None,
        "phase_name": None,
        "competencies": [],
        "reinforcement_topics": topics,
    }
    if data:
        context.update({
            "mission_id": data["mission"].id,
            "mission_name": data["mission"].name,
            "phase_number": data["phase"].number,
            "phase_name": data["phase"].name,
            "competencies": [
                {"code": item.code, "name": item.name}
                for item in data["competencies"]
            ],
        })

    return {
        "agent": "mentor",
        "conversation_id": conversation.id,
        "user_context": {
            "personal_goal": profile.personal_goal if profile else None,
            "knowledge_level": profile.knowledge_level if profile else None,
        },
        "learning_context": context,
        "messages": [
            {"role": item.get("role"), "content": item.get("content")}
            for item in (conversation.messages or [])[-5:]
        ],
        "message": content,
    }


async def send_mentor_message(
    db: AsyncSession,
    user: User,
    content: str,
    mission_id: int | None,
) -> dict:
    content = (content or "").strip()
    if not content:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Escreva uma mensagem antes de enviar.",
        )
    if len(content) > MAX_MESSAGE_LENGTH:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"A mensagem pode ter no máximo {MAX_MESSAGE_LENGTH} caracteres.",
        )

    conv = await _get_or_create_conversation(db, user.id, "mentor", mission_id)
    now = datetime.now(timezone.utc)

    user_message = {
        "role": "user",
        "content": content,
        "timestamp": now.isoformat(),
    }
    conv.messages = [*conv.messages, user_message]
    await db.flush()

    # Recupera thread_id da última mensagem do assistente para continuar o turn.
    prior_thread_id: str | None = None
    for msg in reversed(conv.messages[:-1]):  # exclui a mensagem que acabamos de adicionar
        if msg.get("role") == "assistant" and msg.get("thread_id"):
            prior_thread_id = msg["thread_id"]
            break

    payload = await build_mentor_payload(db, user, conv, content)
    reply = await orchestrate.request_mentor_reply(payload, thread_id=prior_thread_id)

    assistant_message = {
        "role": "assistant",
        "content": reply.content,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "status": reply.status,
        **({"thread_id": reply.thread_id} if reply.thread_id else {}),
    }
    conv.messages = [*conv.messages, assistant_message]
    conv.updated_at = datetime.now(timezone.utc)
    await db.flush()

    return {
        "role": "assistant",
        "content": reply.content,
        "timestamp": assistant_message["timestamp"],
        "status": reply.status,
        "suggestions": reply.suggestions,
        "source": reply.source,
    }


async def get_mentor_history(db: AsyncSession, user_id: int) -> list[Conversation]:
    result = await db.execute(
        select(Conversation)
        .where(Conversation.user_id == user_id, Conversation.agent == "mentor")
        .order_by(Conversation.updated_at.desc())
        .limit(10)
    )
    return list(result.scalars().all())
