from tests.conftest import auth_headers, register_verified_user


async def test_mentor_placeholder_persists_messages_for_own_user(client, db_session):
    _, alice_tokens = await register_verified_user(client, db_session)
    _, bob_tokens = await register_verified_user(client, db_session)

    response = await client.post(
        "/api/v1/conversations/mentor",
        json={"content": "Como organizo meu primeiro salário?"},
        headers=auth_headers(alice_tokens),
    )
    alice_history = await client.get(
        "/api/v1/conversations/mentor/history",
        headers=auth_headers(alice_tokens),
    )
    bob_history = await client.get(
        "/api/v1/conversations/mentor/history",
        headers=auth_headers(bob_tokens),
    )

    assert response.status_code == 200
    assert response.json()["role"] == "assistant"
    assert alice_history.status_code == 200
    assert len(alice_history.json()) == 1
    assert [message["role"] for message in alice_history.json()[0]["messages"]] == [
        "user",
        "assistant",
    ]
    assert bob_history.json() == []
