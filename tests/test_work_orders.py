from datetime import datetime


def create_asset(client):
    response = client.post(
        "/assets",
        json={
            "name": "Main Distribution Board",
            "location": "Building A - Electrical Room",
            "criticality": "HIGH",
        },
    )
    return response.json()["id"]


def test_create_high_priority_work_order(client):
    asset_id = create_asset(client)

    response = client.post(
        "/work-orders",
        json={
            "asset_id": asset_id,
            "title": "Investigate abnormal heat",
            "priority": "HIGH",
        },
    )

    assert response.status_code == 201

    data = response.json()

    assert data["asset_id"] == asset_id
    assert data["priority"] == "HIGH"
    assert data["status"] == "OPEN"
    assert data["completed_at"] is None

    created_at = datetime.fromisoformat(
        data["created_at"].replace("Z", "+00:00")
    )
    due_at = datetime.fromisoformat(
        data["due_at"].replace("Z", "+00:00")
    )

    assert (due_at - created_at).total_seconds() == 4 * 60 * 60


def test_create_medium_priority_work_order_has_24_hour_sla(client):
    asset_id = create_asset(client)

    response = client.post(
        "/work-orders",
        json={
            "asset_id": asset_id,
            "title": "Inspect air handling unit",
            "priority": "MEDIUM",
        },
    )

    assert response.status_code == 201

    data = response.json()

    created_at = datetime.fromisoformat(
        data["created_at"].replace("Z", "+00:00")
    )
    due_at = datetime.fromisoformat(
        data["due_at"].replace("Z", "+00:00")
    )

    assert (due_at - created_at).total_seconds() == 24 * 60 * 60


def test_create_low_priority_work_order_has_72_hour_sla(client):
    asset_id = create_asset(client)

    response = client.post(
        "/work-orders",
        json={
            "asset_id": asset_id,
            "title": "Replace damaged room label",
            "priority": "LOW",
        },
    )

    assert response.status_code == 201

    data = response.json()

    created_at = datetime.fromisoformat(
        data["created_at"].replace("Z", "+00:00")
    )
    due_at = datetime.fromisoformat(
        data["due_at"].replace("Z", "+00:00")
    )

    assert (due_at - created_at).total_seconds() == 72 * 60 * 60


def test_create_work_order_for_missing_asset_returns_404(client):
    response = client.post(
        "/work-orders",
        json={
            "asset_id": 999,
            "title": "Inspect nonexistent asset",
            "priority": "HIGH",
        },
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Asset not found"


def test_work_order_status_progression(client):
    asset_id = create_asset(client)

    created = client.post(
        "/work-orders",
        json={
            "asset_id": asset_id,
            "title": "Investigate electrical fault",
            "priority": "HIGH",
        },
    )

    work_order_id = created.json()["id"]

    in_progress = client.patch(
        f"/work-orders/{work_order_id}/status",
        json={"status": "IN_PROGRESS"},
    )

    assert in_progress.status_code == 200
    assert in_progress.json()["status"] == "IN_PROGRESS"
    assert in_progress.json()["completed_at"] is None

    completed = client.patch(
        f"/work-orders/{work_order_id}/status",
        json={"status": "COMPLETED"},
    )

    assert completed.status_code == 200
    assert completed.json()["status"] == "COMPLETED"
    assert completed.json()["completed_at"] is not None


def test_completed_work_order_cannot_be_reopened(client):
    asset_id = create_asset(client)

    created = client.post(
        "/work-orders",
        json={
            "asset_id": asset_id,
            "title": "Repair pump",
            "priority": "HIGH",
        },
    )

    work_order_id = created.json()["id"]

    client.patch(
        f"/work-orders/{work_order_id}/status",
        json={"status": "IN_PROGRESS"},
    )
    client.patch(
        f"/work-orders/{work_order_id}/status",
        json={"status": "COMPLETED"},
    )

    response = client.patch(
        f"/work-orders/{work_order_id}/status",
        json={"status": "OPEN"},
    )

    assert response.status_code == 409
    assert (
        response.json()["detail"]
        == "Invalid status transition: COMPLETED -> OPEN"
    )


def test_missing_work_order_returns_404(client):
    response = client.patch(
        "/work-orders/999/status",
        json={"status": "IN_PROGRESS"},
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Work order not found"


def test_invalid_priority_returns_422(client):
    asset_id = create_asset(client)

    response = client.post(
        "/work-orders",
        json={
            "asset_id": asset_id,
            "title": "Invalid priority test",
            "priority": "URGENT",
        },
    )

    assert response.status_code == 422