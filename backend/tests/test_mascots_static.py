"""Os GLBs dos mascotes são servidos pelo backend existente em /static."""


async def test_mascot_manifest_is_served(client):
    response = await client.get("/static/mascotes/manifest.json")

    assert response.status_code == 200
    body = response.json()
    ids = {character["id"] for character in body["characters"]}
    assert {"catalisador", "mentor", "analista"} <= ids


async def test_mascot_glb_is_served_with_gltf_content_type(client):
    response = await client.get("/static/mascotes/mentor.glb")

    assert response.status_code == 200
    assert response.headers["content-type"] == "model/gltf-binary"
    assert len(response.content) > 1_000_000
