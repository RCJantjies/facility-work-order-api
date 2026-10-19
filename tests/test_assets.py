def test_create_asset(client):
    response = client.post(
        "/assets",
        json={
            "name": "Main Distribution Board",
            "location": "Building A - Electrical Room",
            "criticality": "HIGH",
        },
    )

    assert response.status_code == 201

    data = response.json()

    assert data["id"] == 1
    assert data["name"] == "Main Distribution Board"
    assert data["location"] == "Building A - Electrical Room"
    assert data["criticality"] == "HIGH"


def test_list_assets(client):
    client.post(
        "/assets",
        json={
            "name": "Chiller 01",
            "location": "Plant Room",
            "criticality": "HIGH",
        },
    )

    response = client.get("/assets")

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 1
    assert data[0]["name"] == "Chiller 01"


def test_create_asset_rejects_invalid_criticality(client):
    response = client.post(
        "/assets",
        json={
            "name": "Office Printer",
            "location": "Administration Office",
            "criticality": "CRITICAL",
        },
    )

    assert response.status_code == 422