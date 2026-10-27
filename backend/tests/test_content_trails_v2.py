"""Testes de contrato para os seeds das trilhas da reestruturação curricular.

Cobre:
  - trail_1_v2.py  — missões 2 e 3 da trilha 1 (holerite e 13º/férias)
  - trail_2_v1.py  — missões 3 e 4 da trilha 2 (gastos invisíveis e controle)
  - trail_3_v1.py  — missões 3 e 4 da trilha 3 (carteiras digitais e comparando)
  - trail_4_v1.py  — missões 2 e 3 da trilha 4 (fatura ciclo e pagamento mínimo)
  - trail_5_v1.py  — missões 2 e 4 da trilha 5 (calculando e usando a reserva)
  - trail_6_v1.py  — missões 2 e 3 da trilha 6 (separar no recebimento e adaptar)
  - trail_7_v1.py  — trilha 7 completa (juros e parcelas)
  - trail_8_v1.py  — trilha 8 completa (dívida que cresce)
  - trail_9_v1.py  — trilha 9 completa (inflação e poder de compra)
  - trail_10_v1.py — trilha 10 completa (onde o dinheiro rende)
  - trail_11_v1.py — trilha 11 completa (golpes e proteção de dados)
  - trail_12_v1.py — trilha 12 completa (desafio integrador)
"""
import pytest

from app.modules.content.activity_schema import validate_activity_content
from app.modules.content.seeds.trail_1_v2 import TRAIL_1_V2
from app.modules.content.seeds.trail_2_v1 import TRAIL_2_V1
from app.modules.content.seeds.trail_3_v1 import TRAIL_3_V1
from app.modules.content.seeds.trail_4_v1 import TRAIL_4_V1
from app.modules.content.seeds.trail_5_v1 import TRAIL_5_V1
from app.modules.content.seeds.trail_6_v1 import TRAIL_6_V1
from app.modules.content.seeds.trail_7_v1 import TRAIL_7_V1
from app.modules.content.seeds.trail_8_v1 import TRAIL_8_V1
from app.modules.content.seeds.trail_9_v1 import TRAIL_9_V1
from app.modules.content.seeds.trail_10_v1 import TRAIL_10_V1
from app.modules.content.seeds.trail_11_v1 import TRAIL_11_V1
from app.modules.content.seeds.trail_12_v1 import TRAIL_12_V1

ALL_SEEDS = [
    TRAIL_1_V2,
    TRAIL_2_V1,
    TRAIL_3_V1,
    TRAIL_4_V1,
    TRAIL_5_V1,
    TRAIL_6_V1,
    TRAIL_7_V1,
    TRAIL_8_V1,
    TRAIL_9_V1,
    TRAIL_10_V1,
    TRAIL_11_V1,
    TRAIL_12_V1,
]
SEED_IDS = [f"trail_{seed['phase_number']}" for seed in ALL_SEEDS]

# Seeds que são expansões (adicionam missões a phases já existentes)
EXPANSION_SEEDS = [TRAIL_1_V2, TRAIL_2_V1, TRAIL_3_V1, TRAIL_4_V1, TRAIL_5_V1, TRAIL_6_V1]
EXPANSION_IDS = [f"trail_{seed['phase_number']}_exp" for seed in EXPANSION_SEEDS]

# Seeds de trilhas novas (phases 7–12)
NEW_TRAIL_SEEDS = [TRAIL_7_V1, TRAIL_8_V1, TRAIL_9_V1, TRAIL_10_V1, TRAIL_11_V1, TRAIL_12_V1]
NEW_TRAIL_IDS = [f"trail_{seed['phase_number']}" for seed in NEW_TRAIL_SEEDS]

CONTENT_TYPES = ("explanation", "example", "tip")


@pytest.mark.parametrize("seed", ALL_SEEDS, ids=SEED_IDS)
def test_seed_has_phase_number_and_missions(seed):
    """Todo seed deve ter phase_number inteiro e lista de missões não vazia."""
    assert isinstance(seed["phase_number"], int)
    assert seed["missions"]


@pytest.mark.parametrize("seed", ALL_SEEDS, ids=SEED_IDS)
def test_every_activity_matches_the_formal_content_schema(seed):
    """Toda atividade deve passar na validação do schema Pydantic."""
    for mission in seed["missions"]:
        assert mission["activities"], f"Missão {mission['number']} sem atividades."
        for activity in mission["activities"]:
            validate_activity_content(activity["activity_type"], activity["content"])


@pytest.mark.parametrize("seed", ALL_SEEDS, ids=SEED_IDS)
def test_every_activity_competency_code_exists_in_its_mission(seed):
    """Toda atividade deve referenciar apenas competências definidas na missão."""
    for mission in seed["missions"]:
        known_codes = {comp["code"] for comp in mission["competencies"]}
        for activity in mission["activities"]:
            used_codes = set(activity["content"]["competency_codes"])
            assert used_codes <= known_codes, (
                f"Trilha {seed['phase_number']}, missão {mission['number']}, "
                f"atividade {activity['order']} usa códigos não cadastrados: "
                f"{used_codes - known_codes}."
            )


@pytest.mark.parametrize("seed", ALL_SEEDS, ids=SEED_IDS)
def test_essential_competencies_have_objective_evidence(seed):
    """Competências essenciais devem ter ao menos uma atividade objetiva (não open_text)."""
    for mission in seed["missions"]:
        objective_codes = {
            code
            for activity in mission["activities"]
            if activity["activity_type"] != "open_text"
            for code in activity["content"]["competency_codes"]
        }
        for comp in mission["competencies"]:
            if comp["is_essential"]:
                assert comp["code"] in objective_codes, (
                    f"Competência essencial {comp['code']} da trilha "
                    f"{seed['phase_number']}, missão {mission['number']}, "
                    "sem evidência objetiva."
                )


@pytest.mark.parametrize("seed", NEW_TRAIL_SEEDS, ids=NEW_TRAIL_IDS)
def test_new_trail_missions_are_all_required_with_passing_score(seed):
    """Todas as missões de trilhas novas devem ser obrigatórias com passing_score=70."""
    for mission in seed["missions"]:
        assert mission["is_required"], (
            f"Trilha {seed['phase_number']}, missão {mission['number']} não é obrigatória."
        )
        assert mission["passing_score"] == 70, (
            f"Trilha {seed['phase_number']}, missão {mission['number']} "
            f"tem passing_score inesperado: {mission['passing_score']}."
        )


@pytest.mark.parametrize("seed", NEW_TRAIL_SEEDS, ids=NEW_TRAIL_IDS)
def test_new_trail_missions_have_content_items(seed):
    """Missões de trilhas novas devem ter content_items com títulos e corpos não-vazios."""
    for mission in seed["missions"]:
        items = mission.get("content_items", [])
        # Trilha 12 (Desafio integrador) pode não ter content_items convencionais.
        if seed["phase_number"] == 12:
            continue
        assert items, (
            f"Trilha {seed['phase_number']}, missão {mission['number']} sem content_items."
        )
        for item in items:
            assert item.get("title"), (
                f"Trilha {seed['phase_number']}, missão {mission['number']}: "
                "content_item sem título."
            )
            assert item.get("body", "").strip(), (
                f"Trilha {seed['phase_number']}, missão {mission['number']}: "
                "content_item com corpo vazio."
            )


def _flow_key(seed, mission):
    return (seed["phase_number"], mission["number"])


@pytest.mark.parametrize("seed", ALL_SEEDS, ids=SEED_IDS)
def test_lesson_flows_cover_all_new_missions(seed):
    """Toda missão dos novos seeds deve ter um roteiro no LESSON_FLOWS_TRAILS."""
    from app.modules.content.lesson_flows_trails import LESSON_FLOWS_TRAILS

    for mission in seed["missions"]:
        key = _flow_key(seed, mission)
        assert key in LESSON_FLOWS_TRAILS, (
            f"Missão {key} não tem roteiro em LESSON_FLOWS_TRAILS."
        )


@pytest.mark.parametrize("seed", ALL_SEEDS, ids=SEED_IDS)
def test_lesson_flow_structure_for_new_missions(seed):
    """Cada flow deve começar com intro, terminar com summary e cobrir todas as atividades."""
    from app.modules.content.lesson_flows_trails import LESSON_FLOWS_TRAILS

    for mission in seed["missions"]:
        key = _flow_key(seed, mission)
        flow = LESSON_FLOWS_TRAILS[key]

        step_types = [step["type"] for step in flow]
        assert flow[0]["type"] == "intro", f"{key}: flow não começa com intro."
        assert flow[-1]["type"] == "summary", f"{key}: flow não termina com summary."

        activities_by_order = {a["order"]: a for a in mission["activities"]}
        content_by_key = {
            (item["content_type"], item["order"])
            for item in mission.get("content_items", [])
        }
        covered = []

        for step in flow:
            if step["type"] == "reading":
                assert (step["content_type"], step["content_order"]) in content_by_key, (
                    f"{key}: step {step} referencia content_item inexistente."
                )
            elif step["type"] in {"question", "scenario"}:
                activity = activities_by_order.get(step["activity_order"])
                assert activity is not None, (
                    f"{key}: step {step} referencia atividade inexistente."
                )
                expected = (
                    "scenario" if activity["activity_type"] == "simulation" else "question"
                )
                assert step["type"] == expected, (
                    f"{key}: step {step} tem tipo errado para atividade {activity['activity_type']}."
                )
                covered.append(step["activity_order"])

        assert sorted(covered) == sorted(activities_by_order), (
            f"{key}: nem todas as atividades estão cobertas no flow. "
            f"Cobertas: {sorted(covered)}, Esperadas: {sorted(activities_by_order)}."
        )
