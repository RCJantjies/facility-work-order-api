from datetime import datetime, timedelta, timezone

from app.models import Priority, WorkOrder, WorkOrderStatus


def test_metrics_empty_database(client):
    response = client.get("/metrics")

    assert response.status_code == 200
    assert response.json() == {
        "total": 0,
        "open": 0,
        "in_progress": 0,
        "completed": 0,
        "overdue": 0,
    }


def test_metrics_count_work_order_statuses(client):
    asset = client.post(
        "/assets",
        json={
            "name": "Chiller 01",
            "location": "Plant Room",
            "criticality": "HIGH",
        },
    ).json()

    work_order = client.post(
        "/work-orders",
        json={
            "asset_id": asset["id"],
            "title": "Inspect chiller",
            "priority": "MEDIUM",
        },
    ).json()

    response = client.get("/metrics")

    assert response.status_code == 200
    assert response.json()["total"] == 1
    assert response.json()["open"] == 1

    client.patch(
        f"/work-orders/{work_order['id']}/status",
        json={"status": "IN_PROGRESS"},
    )

    response = client.get("/metrics")

    assert response.json()["open"] == 0
    assert response.json()["in_progress"] == 1

    client.patch(
        f"/work-orders/{work_order['id']}/status",
        json={"status": "COMPLETED"},
    )

    response = client.get("/metrics")

    assert response.json()["in_progress"] == 0
    assert response.json()["completed"] == 1


def test_overdue_incomplete_work_order_is_counted(client, session):
    now = datetime.now(timezone.utc)

    work_order = WorkOrder(
        asset_id=1,
        title="Overdue inspection",
        priority=Priority.HIGH,
        status=WorkOrderStatus.OPEN,
        created_at=now - timedelta(hours=6),
        due_at=now - timedelta(hours=2),
    )

    session.add(work_order)
    session.commit()

    response = client.get("/metrics")

    assert response.status_code == 200
    assert response.json()["overdue"] == 1


def test_completed_work_order_is_not_overdue(client, session):
    now = datetime.now(timezone.utc)

    work_order = WorkOrder(
        asset_id=1,
        title="Completed inspection",
        priority=Priority.HIGH,
        status=WorkOrderStatus.COMPLETED,
        created_at=now - timedelta(hours=10),
        due_at=now - timedelta(hours=6),
        completed_at=now - timedelta(hours=7),
    )

    session.add(work_order)
    session.commit()

    response = client.get("/metrics")

    assert response.status_code == 200
    assert response.json()["completed"] == 1
    assert response.json()["overdue"] == 0