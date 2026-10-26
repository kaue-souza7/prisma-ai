from app.modules.content.activity_schema import validate_activity_content
from app.modules.content.seeds.phase_1_v1 import PHASE_1_V1


def test_phase_1_has_three_mandatory_missions():
    missions = PHASE_1_V1["missions"]

    assert [mission["number"] for mission in missions] == [1, 2, 3]
    assert all(mission["is_required"] for mission in missions)
    assert all(mission["passing_score"] == 70 for mission in missions)


def test_every_activity_matches_the_formal_content_schema():
    for mission in PHASE_1_V1["missions"]:
        assert mission["activities"], f"Missão {mission['number']} sem atividades."

        for activity in mission["activities"]:
            validate_activity_content(activity["activity_type"], activity["content"])


def test_every_activity_competency_code_exists_in_its_mission():
    for mission in PHASE_1_V1["missions"]:
        known_codes = {competency["code"] for competency in mission["competencies"]}

        for activity in mission["activities"]:
            used_codes = set(activity["content"]["competency_codes"])
            assert used_codes <= known_codes, (
                f"Atividade {activity['order']} da missão {mission['number']} usa "
                f"códigos sem competência cadastrada: {used_codes - known_codes}."
            )


def test_all_phase_1_competencies_have_objective_evidence():
    for mission in PHASE_1_V1["missions"]:
        objective_codes = {
            code
            for activity in mission["activities"]
            if activity["activity_type"] != "open_text"
            for code in activity["content"]["competency_codes"]
        }

        for competency in mission["competencies"]:
            assert competency["code"] in objective_codes, (
                f"Competência {competency['code']} não possui evidência objetiva."
            )


def test_content_items_are_ready_to_publish():
    for mission in PHASE_1_V1["missions"]:
        items = mission["content_items"]

        assert len(items) >= 3
        assert all(item["body"].strip() for item in items)
        assert all(item["title"] for item in items)
        assert all(item["content_type"] in {"explanation", "example", "tip"} for item in items)
