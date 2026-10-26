"""Aplicação idempotente de conteúdo versionado por fase.

As funções de carga das Fases 3 a 6 compartilham esta implementação. O upsert
usa chaves naturais (fase + número da missão, missão + código da competência,
missão + ordem da atividade, missão + tipo + ordem do conteúdo) para preservar
IDs de atividades já respondidas por estudantes.
"""
from datetime import datetime, timezone

import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import JSONB

from app.modules.content.activity_schema import validate_activity_content


metadata = sa.MetaData()

phases = sa.Table(
    "phases",
    metadata,
    sa.Column("id", sa.Integer, primary_key=True),
    sa.Column("number", sa.Integer),
)

missions = sa.Table(
    "missions",
    metadata,
    sa.Column("id", sa.Integer, primary_key=True, autoincrement=True),
    sa.Column("phase_id", sa.Integer),
    sa.Column("number", sa.Integer),
    sa.Column("name", sa.String),
    sa.Column("description", sa.Text),
    sa.Column("order", sa.Integer),
    sa.Column("is_required", sa.Boolean),
    sa.Column("passing_score", sa.Integer),
)

competencies = sa.Table(
    "competencies",
    metadata,
    sa.Column("id", sa.Integer, primary_key=True, autoincrement=True),
    sa.Column("mission_id", sa.Integer),
    sa.Column("code", sa.String),
    sa.Column("name", sa.String),
    sa.Column("description", sa.Text),
    sa.Column("is_essential", sa.Boolean),
)

activities = sa.Table(
    "activities",
    metadata,
    sa.Column("id", sa.Integer, primary_key=True, autoincrement=True),
    sa.Column("mission_id", sa.Integer),
    sa.Column("order", sa.Integer),
    sa.Column("activity_type", sa.String),
    sa.Column("content", JSONB),
    sa.Column("points_value", sa.Integer),
    sa.Column("is_active", sa.Boolean),
)

content_items = sa.Table(
    "content_items",
    metadata,
    sa.Column("id", sa.Integer, primary_key=True, autoincrement=True),
    sa.Column("mission_id", sa.Integer),
    sa.Column("content_type", sa.String),
    sa.Column("title", sa.String),
    sa.Column("body", sa.Text),
    sa.Column("order", sa.Integer),
    sa.Column("is_published", sa.Boolean),
    sa.Column("created_by", sa.String),
    sa.Column("created_at", sa.DateTime(timezone=True)),
    sa.Column("updated_at", sa.DateTime(timezone=True)),
)


def seed_phase_content(bind, data: dict, source_tag: str) -> None:
    """Insere ou atualiza uma fase. Deve ser executada dentro de uma transação."""
    phase_id = bind.execute(
        sa.select(phases.c.id).where(phases.c.number == data["phase_number"])
    ).scalar_one_or_none()
    if phase_id is None:
        raise RuntimeError(
            f"Fase {data['phase_number']} não encontrada. "
            "Aplique a migration 0001 antes."
        )

    now = datetime.now(timezone.utc)

    for mission_data in data["missions"]:
        mission_id = _upsert_mission(bind, phase_id, mission_data)

        for competency_data in mission_data["competencies"]:
            _upsert_competency(bind, mission_id, competency_data)

        known_codes = {
            competency["code"] for competency in mission_data["competencies"]
        }
        for activity_data in mission_data["activities"]:
            validate_activity_content(
                activity_data["activity_type"], activity_data["content"]
            )
            unknown_codes = (
                set(activity_data["content"]["competency_codes"]) - known_codes
            )
            if unknown_codes:
                raise ValueError(
                    f"Atividade {activity_data['order']} da missão "
                    f"{mission_data['number']} usa competências inexistentes: "
                    f"{sorted(unknown_codes)}."
                )
            _upsert_activity(bind, mission_id, activity_data)

        for item_data in mission_data["content_items"]:
            _upsert_content_item(
                bind, mission_id, item_data, now, source_tag
            )


def _upsert_mission(bind, phase_id: int, data: dict) -> int:
    existing_id = bind.execute(
        sa.select(missions.c.id).where(
            missions.c.phase_id == phase_id,
            missions.c.number == data["number"],
        )
    ).scalar_one_or_none()

    values = {
        "phase_id": phase_id,
        "number": data["number"],
        "name": data["name"],
        "description": data["description"],
        "order": data["order"],
        "is_required": data["is_required"],
        "passing_score": data["passing_score"],
    }

    if existing_id is None:
        bind.execute(sa.insert(missions).values(**values))
        return bind.execute(
            sa.select(missions.c.id).where(
                missions.c.phase_id == phase_id,
                missions.c.number == data["number"],
            )
        ).scalar_one()

    bind.execute(
        sa.update(missions).where(missions.c.id == existing_id).values(**values)
    )
    return existing_id


def _upsert_competency(bind, mission_id: int, data: dict) -> None:
    existing_id = bind.execute(
        sa.select(competencies.c.id).where(
            competencies.c.mission_id == mission_id,
            competencies.c.code == data["code"],
        )
    ).scalar_one_or_none()

    values = {
        "mission_id": mission_id,
        "code": data["code"],
        "name": data["name"],
        "description": data["description"],
        "is_essential": data["is_essential"],
    }

    if existing_id is None:
        bind.execute(sa.insert(competencies).values(**values))
    else:
        bind.execute(
            sa.update(competencies)
            .where(competencies.c.id == existing_id)
            .values(**values)
        )


def _upsert_activity(bind, mission_id: int, data: dict) -> None:
    existing_id = bind.execute(
        sa.select(activities.c.id).where(
            activities.c.mission_id == mission_id,
            activities.c.order == data["order"],
        )
    ).scalar_one_or_none()

    values = {
        "mission_id": mission_id,
        "order": data["order"],
        "activity_type": data["activity_type"],
        "content": data["content"],
        "points_value": data["points_value"],
        "is_active": True,
    }

    if existing_id is None:
        bind.execute(sa.insert(activities).values(**values))
    else:
        bind.execute(
            sa.update(activities)
            .where(activities.c.id == existing_id)
            .values(**values)
        )


def _upsert_content_item(
    bind,
    mission_id: int,
    data: dict,
    now: datetime,
    source_tag: str,
) -> None:
    existing_id = bind.execute(
        sa.select(content_items.c.id).where(
            content_items.c.mission_id == mission_id,
            content_items.c.order == data["order"],
            content_items.c.content_type == data["content_type"],
        )
    ).scalar_one_or_none()

    values = {
        "mission_id": mission_id,
        "content_type": data["content_type"],
        "title": data["title"],
        "body": data["body"],
        "order": data["order"],
        "is_published": True,
        "created_by": source_tag,
        "updated_at": now,
    }

    if existing_id is None:
        bind.execute(
            sa.insert(content_items).values(**values, created_at=now)
        )
    else:
        bind.execute(
            sa.update(content_items)
            .where(content_items.c.id == existing_id)
            .values(**values)
        )
