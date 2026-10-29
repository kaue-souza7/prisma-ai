"""Gera conjuntos de perguntas 2 e 3 para missões que só têm o conjunto 1.

Este script é um **paliativo de conteúdo** para destravar a rotação D-Q1 nas
Trilhas 2–12. Ele clona as atividades do conjunto 1, embaralha a ordem das
alternativas (quando aplicável) e marca o conteúdo como variante gerada. As
perguntas não são novas: o time de conteúdo deve substituí-las por itens
autorais antes do piloto.

Uso (dentro do container do backend):

    docker compose exec -T backend python scripts/backfill_question_sets.py --dry-run
    docker compose exec -T backend python scripts/backfill_question_sets.py

Uso com reforço (question_set=4, opcional):

    docker compose exec -T backend python scripts/backfill_question_sets.py --sets 2,3,4
"""
from __future__ import annotations

import argparse
import asyncio
import copy
import random
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from sqlalchemy import select

from app.core.database import AsyncSessionLocal
from app.shared.models import Activity, Mission


def _shuffle_options(content: dict, rng: random.Random) -> dict:
    """Embaralha alternativas e remapeia o gabarito para os novos values."""
    options = content.get("options")
    if not isinstance(options, list) or len(options) < 2:
        return content

    correct_key = "correct_answer" if "correct_answer" in content else "correct_choice"
    correct = content.get(correct_key)
    indexed = list(enumerate(options))
    rng.shuffle(indexed)

    new_options: list[dict] = []
    mapping: dict[str, str] = {}
    for new_index, (_, option) in enumerate(indexed):
        new_value = chr(ord("a") + new_index)
        if isinstance(option, dict):
            old_value = option.get("value")
            mapping[str(old_value)] = new_value
            new_options.append({**option, "value": new_value})
        else:
            new_options.append(option)

    content["options"] = new_options
    if correct is not None:
        content[correct_key] = mapping.get(str(correct), correct)
    return content


def _variant_content(activity: Activity, target_set: int) -> dict:
    content = copy.deepcopy(activity.content or {})
    rng = random.Random(f"{activity.mission_id}:{activity.order}:{target_set}")
    if activity.activity_type in {"multiple_choice", "simulation"}:
        content = _shuffle_options(content, rng)
    content["variant_of_set"] = 1
    content["variant_generated"] = True
    if target_set == 4:
        content["reinforcement"] = True
    return content


async def backfill(target_sets: list[int], *, dry_run: bool) -> None:
    async with AsyncSessionLocal() as db:
        missions = (await db.execute(select(Mission).order_by(Mission.id))).scalars().all()
        created = 0
        touched_missions = 0

        for mission in missions:
            activities = (
                await db.execute(
                    select(Activity)
                    .where(
                        Activity.mission_id == mission.id,
                        Activity.is_active == True,
                    )
                    .order_by(Activity.order, Activity.question_set)
                )
            ).scalars().all()
            base = [activity for activity in activities if activity.question_set == 1]
            if not base:
                continue

            existing_sets = {activity.question_set for activity in activities}
            mission_created = 0
            for target_set in target_sets:
                if target_set in existing_sets:
                    continue
                for activity in base:
                    db.add(
                        Activity(
                            mission_id=mission.id,
                            order=activity.order,
                            activity_type=activity.activity_type,
                            content=_variant_content(activity, target_set),
                            points_value=activity.points_value,
                            is_active=activity.is_active,
                            question_set=target_set,
                        )
                    )
                    mission_created += 1
            if mission_created:
                touched_missions += 1
                created += mission_created
                print(
                    f"missão {mission.id} ({mission.number}): +{mission_created} atividades"
                )

        if dry_run:
            await db.rollback()
            print(
                f"[dry-run] {created} atividades seriam criadas em {touched_missions} missões."
            )
        else:
            await db.commit()
            print(
                f"{created} atividades criadas em {touched_missions} missões."
            )


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--sets",
        default="2,3",
        help="Conjuntos a criar (padrão: 2,3). Use 2,3,4 para incluir reforço.",
    )
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    target_sets = [int(item) for item in args.sets.split(",") if item.strip()]
    asyncio.run(backfill(target_sets, dry_run=args.dry_run))


if __name__ == "__main__":
    main()
