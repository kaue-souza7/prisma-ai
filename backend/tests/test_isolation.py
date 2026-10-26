from tests.conftest import auth_headers, register_verified_user


async def test_student_cannot_access_admin_content_endpoint(client, db_session):
    _, tokens = await register_verified_user(client, db_session)

    response = await client.post(
        "/api/v1/content/",
        json={"content_type": "tip", "body": "Conteúdo de teste"},
        headers=auth_headers(tokens),
    )

    assert response.status_code == 403
    assert response.json()["error"]["message"] == "Acesso restrito a administradores."


async def test_user_progress_is_isolated_between_accounts(client, db_session):
    alice_user, alice_tokens = await register_verified_user(client, db_session)
    _, bob_tokens = await register_verified_user(client, db_session)

    onboarding = await client.post(
        "/api/v1/users/me/onboarding",
        json={
            "personal_goal": "Meta da Alice",
            "knowledge_level": "beginner",
            "consent_version": "v1",
        },
        headers=auth_headers(alice_tokens),
    )
    assert onboarding.status_code == 200

    alice_me = await client.get("/api/v1/users/me", headers=auth_headers(alice_tokens))
    bob_me = await client.get("/api/v1/users/me", headers=auth_headers(bob_tokens))
    alice_summary = await client.get("/api/v1/progress/summary", headers=auth_headers(alice_tokens))
    bob_summary = await client.get("/api/v1/progress/summary", headers=auth_headers(bob_tokens))

    assert alice_me.json()["user"]["id"] != bob_me.json()["user"]["id"]
    assert alice_me.json()["profile"]["personal_goal"] == "Meta da Alice"
    assert bob_me.json()["profile"]["personal_goal"] is None
    assert bob_me.json()["profile"]["onboarding_completed"] is False
    assert alice_summary.json()["total_points"] == 50
    assert bob_summary.json()["total_points"] == 0
    assert alice_me.json()["user"]["id"] == alice_user.id


async def test_protected_route_without_token_is_rejected(client):
    response = await client.get("/api/v1/progress/summary")
    assert response.status_code in (401, 403)


async def test_invalid_token_is_rejected(client):
    response = await client.get(
        "/api/v1/progress/summary",
        headers={"Authorization": "Bearer token-invalido"},
    )
    assert response.status_code == 401
    assert response.json()["error"]["message"] == "Token inválido ou expirado."
