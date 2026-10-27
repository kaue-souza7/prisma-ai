import pytest

from app.modules.content.activity_schema import validate_activity_content
# Os seeds originais das phases 3–6 são validados contra _BASE_FLOWS
# (flows das missões originais antes da expansão). O LESSON_FLOWS mesclado
# inclui os flows das missões novas, que substituem as entradas antigas.
from app.modules.content.lesson_flows import _BASE_FLOWS as LESSON_FLOWS
from app.modules.content.seeds.phase_3_v1 import PHASE_3_V1
from app.modules.content.seeds.phase_4_v1 import PHASE_4_V1
from app.modules.content.seeds.phase_5_v1 import PHASE_5_V1
from app.modules.content.seeds.phase_6_v1 import PHASE_6_V1


PHASES = [PHASE_3_V1, PHASE_4_V1, PHASE_5_V1, PHASE_6_V1]
PHASE_IDS = [f"fase_{phase['phase_number']}" for phase in PHASES]
CONTENT_TYPES = ("explanation", "example", "tip")


@pytest.mark.parametrize("phase", PHASES, ids=PHASE_IDS)
def test_phase_has_expected_required_missions(phase):
    missions = phase["missions"]

    expected_numbers = [1, 2, 3, 4] if phase["phase_number"] == 6 else [1, 2, 3]
    assert [mission["number"] for mission in missions] == expected_numbers
    assert all(mission["is_required"] for mission in missions)
    assert all(mission["passing_score"] == 70 for mission in missions)
    assert all(mission["competencies"] for mission in missions)
    assert all(mission["activities"] for mission in missions)


@pytest.mark.parametrize("phase", PHASES, ids=PHASE_IDS)
def test_every_activity_matches_the_formal_content_schema(phase):
    for mission in phase["missions"]:
        for activity in mission["activities"]:
            validate_activity_content(activity["activity_type"], activity["content"])


@pytest.mark.parametrize("phase", PHASES, ids=PHASE_IDS)
def test_every_activity_competency_code_exists_in_its_mission(phase):
    for mission in phase["missions"]:
        known_codes = {competency["code"] for competency in mission["competencies"]}

        for activity in mission["activities"]:
            used_codes = set(activity["content"]["competency_codes"])
            assert used_codes <= known_codes, (
                f"Atividade {activity['order']} da missão {mission['number']} usa "
                f"códigos sem competência cadastrada: {used_codes - known_codes}."
            )


@pytest.mark.parametrize("phase", PHASES, ids=PHASE_IDS)
def test_essential_competencies_have_objective_evidence(phase):
    for mission in phase["missions"]:
        objective_codes = {
            code
            for activity in mission["activities"]
            if activity["activity_type"] != "open_text"
            for code in activity["content"]["competency_codes"]
        }

        for competency in mission["competencies"]:
            if competency["is_essential"]:
                assert competency["code"] in objective_codes, (
                    f"Competência essencial {competency['code']} da missão "
                    f"{mission['number']} não possui evidência objetiva."
                )


@pytest.mark.parametrize("phase", PHASES, ids=PHASE_IDS)
def test_content_items_are_ready_to_publish(phase):
    for mission in phase["missions"]:
        items = mission["content_items"]

        if not items:
            # O desafio integrador é conduzido pelo roteiro, com intro e
            # síntese próprias, e não precisa de itens de leitura.
            assert mission["name"] == "Desafio integrador"
            continue

        assert len(items) == 3
        assert [item["content_type"] for item in items] == list(CONTENT_TYPES)
        assert all(item["body"].strip() for item in items)
        assert all(item["title"] for item in items)


def test_lesson_flows_cover_all_phases_and_missions():
    for phase in PHASES:
        for mission in phase["missions"]:
            key = (phase["phase_number"], mission["number"])
            assert key in LESSON_FLOWS, f"Minicurso {key} sem roteiro."


@pytest.mark.parametrize(
    "key",
    sorted(
        (phase["phase_number"], mission["number"])
        for phase in PHASES
        for mission in phase["missions"]
    ),
)
def test_lesson_flow_references_existing_content_and_activities(key):
    phase = next(item for item in PHASES if item["phase_number"] == key[0])
    mission = next(item for item in phase["missions"] if item["number"] == key[1])
    flow = LESSON_FLOWS[key]

    assert flow[0]["type"] == "intro"
    assert flow[-1]["type"] == "summary"

    content_by_key = {
        (item["content_type"], item["order"]) for item in mission["content_items"]
    }
    activities_by_order = {
        activity["order"]: activity for activity in mission["activities"]
    }
    covered_activities = []

    for step in flow:
        if step["type"] == "reading":
            assert (step["content_type"], step["content_order"]) in content_by_key
        elif step["type"] in {"question", "scenario"}:
            activity = activities_by_order.get(step["activity_order"])
            assert activity is not None, (
                f"Etapa {step} referencia uma atividade inexistente em {key}."
            )
            expected_type = (
                "scenario" if activity["activity_type"] == "simulation" else "question"
            )
            assert step["type"] == expected_type
            covered_activities.append(step["activity_order"])

    assert sorted(covered_activities) == sorted(activities_by_order)


@pytest.mark.parametrize(
    "key",
    sorted(
        (phase["phase_number"], mission["number"])
        for phase in PHASES
        for mission in phase["missions"]
    ),
)
def test_lesson_flow_has_intro_reading_activities_and_summary(key):
    flow = LESSON_FLOWS[key]
    step_types = [step["type"] for step in flow]

    assert step_types.count("intro") == 1
    assert step_types.count("summary") == 1
    assert step_types.count("question") + step_types.count("scenario") >= 4
    assert step_types.count("reading") >= 3 or key == (6, 4)
