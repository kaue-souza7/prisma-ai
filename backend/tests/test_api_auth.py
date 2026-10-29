from tests.conftest import auth_headers, register_verified_user


async def test_register_verify_login_and_me(client, db_session):
    user, tokens = await register_verified_user(client, db_session)

    response = await client.get("/api/v1/users/me", headers=auth_headers(tokens))
    assert response.status_code == 200
    body = response.json()
    assert body["user"]["id"] == user.id
    assert body["user"]["email"] == user.email
    assert body["user"]["role"] == "student"
    assert body["user"]["is_verified"] is True
    assert body["profile"]["onboarding_completed"] is False
    assert "access_token" not in response.text


async def test_login_requires_verified_email_when_flag_is_enabled(
    client, db_session, monkeypatch
):
    from uuid import uuid4

    from app.core.config import settings

    monkeypatch.setattr(settings, "require_email_verification", True)

    email = f"nao-verificado.{uuid4().hex}@example.com"
    register = await client.post(
        "/api/v1/auth/register",
        json={"email": email, "password": "Senha123"},
    )
    assert register.status_code == 201

    login = await client.post(
        "/api/v1/auth/login",
        json={"email": email, "password": "Senha123"},
    )
    assert login.status_code == 403
    assert login.json()["error"]["message"] == "E-mail não verificado. Verifique sua caixa de entrada."


async def test_register_creates_verified_user_and_allows_login(client, db_session):
    from uuid import uuid4

    email = f"acesso-direto.{uuid4().hex}@example.com"
    register = await client.post(
        "/api/v1/auth/register",
        json={"email": email, "password": "Senha123"},
    )
    assert register.status_code == 201

    login = await client.post(
        "/api/v1/auth/login",
        json={"email": email, "password": "Senha123"},
    )
    assert login.status_code == 200
    assert login.json()["access_token"]

    me = await client.get(
        "/api/v1/users/me",
        headers={"Authorization": f"Bearer {login.json()['access_token']}"},
    )
    assert me.status_code == 200
    assert me.json()["user"]["is_verified"] is True


async def test_duplicate_registration_is_rejected(client, db_session):
    from uuid import uuid4

    email = f"duplicado.{uuid4().hex}@example.com"
    payload = {"email": email, "password": "Senha123"}

    first = await client.post("/api/v1/auth/register", json=payload)
    second = await client.post("/api/v1/auth/register", json=payload)

    assert first.status_code == 201
    assert second.status_code == 409
    assert second.json()["error"]["message"] == "E-mail já cadastrado."


async def test_weak_password_returns_structured_error(client):
    response = await client.post(
        "/api/v1/auth/register",
        json={"email": "fraca@example.com", "password": "abc"},
    )
    assert response.status_code == 422
    assert response.json()["error"]["message"] == "Dados inválidos."
    assert response.json()["error"]["detail"]


async def test_onboarding_is_idempotent_and_grants_bonus_once(client, db_session):
    _, tokens = await register_verified_user(client, db_session)
    headers = auth_headers(tokens)
    payload = {
        "personal_goal": "Organizar meu primeiro salário",
        "knowledge_level": "beginner",
        "consent_version": "v1",
        "preferences": {"theme": "light"},
    }

    first = await client.post("/api/v1/users/me/onboarding", json=payload, headers=headers)
    second = await client.post("/api/v1/users/me/onboarding", json=payload, headers=headers)
    summary = await client.get("/api/v1/progress/summary", headers=headers)

    assert first.status_code == 200
    assert second.status_code == 200
    assert summary.status_code == 200
    assert summary.json()["total_points"] == 50
    assert summary.json()["coins"] == 20
    assert [item["key"] for item in summary.json()["achievements"]] == ["primeiro_passo"]


async def test_onboarding_repairs_missing_profile_for_legacy_user(client, db_session):
    from sqlalchemy import select

    from app.shared.models import Profile

    user, tokens = await register_verified_user(client, db_session)
    profile_result = await db_session.execute(
        select(Profile).where(Profile.user_id == user.id)
    )
    profile = profile_result.scalar_one()
    await db_session.delete(profile)
    await db_session.flush()

    response = await client.post(
        "/api/v1/users/me/onboarding",
        json={
            "personal_goal": "Organizar meu primeiro salário",
            "knowledge_level": "beginner",
            "consent_version": "v1",
        },
        headers=auth_headers(tokens),
    )

    assert response.status_code == 200
    assert response.json()["trail"]["phase_order"] == [
        1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12
    ]

    repaired = await db_session.execute(
        select(Profile).where(Profile.user_id == user.id)
    )
    assert repaired.scalar_one().onboarding_completed is True


async def test_password_reset_flow_changes_password(client, db_session):
    from sqlalchemy import select

    from app.shared.models import User

    user, _ = await register_verified_user(client, db_session)
    request = await client.post(
        "/api/v1/auth/password-reset/request",
        json={"email": user.email},
    )
    assert request.status_code == 200

    await db_session.refresh(user)
    assert user.password_reset_token

    confirm = await client.post(
        "/api/v1/auth/password-reset/confirm",
        json={"token": user.password_reset_token, "new_password": "NovaSenha456"},
    )
    old_login = await client.post(
        "/api/v1/auth/login",
        json={"email": user.email, "password": "Senha123"},
    )
    new_login = await client.post(
        "/api/v1/auth/login",
        json={"email": user.email, "password": "NovaSenha456"},
    )

    assert confirm.status_code == 200
    assert old_login.status_code == 401
    assert new_login.status_code == 200


async def test_password_reset_request_does_not_reveal_account_existence(client):
    response = await client.post(
        "/api/v1/auth/password-reset/request",
        json={"email": "nao-existe@example.com"},
    )

    assert response.status_code == 200
    assert response.json()["message"] == (
        "Se o e-mail estiver cadastrado, você receberá as instruções em breve."
    )


async def test_refresh_token_returns_new_pair(client, db_session):
    _, tokens = await register_verified_user(client, db_session)

    response = await client.post(
        "/api/v1/auth/refresh",
        json={"refresh_token": tokens["refresh_token"]},
    )

    assert response.status_code == 200
    assert response.json()["access_token"]
    assert response.json()["refresh_token"]
    assert response.json()["token_type"] == "bearer"
