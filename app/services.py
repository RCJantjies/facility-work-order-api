from datetime import datetime, timedelta, timezone

from sqlmodel import Session, select

from app.models import Priority, WorkOrder, WorkOrderStatus


SLA_HOURS = {
    Priority.HIGH: 4,
    Priority.MEDIUM: 24,
    Priority.LOW: 72,
}


def utc_now() -> datetime:
    """Return the current time as a timezone-aware UTC datetime."""
    return datetime.now(timezone.utc)


def calculate_due_at(priority: Priority, created_at: datetime) -> datetime:
    """Calculate the SLA deadline for a work order."""
    return created_at + timedelta(hours=SLA_HOURS[priority])


def create_work_order(
    session: Session,
    asset_id: int,
    title: str,
    priority: Priority,
    now: datetime | None = None,
) -> WorkOrder:
    """Create and persist a new work order."""
    created_at = now or utc_now()

    work_order = WorkOrder(
        asset_id=asset_id,
        title=title,
        priority=priority,
        status=WorkOrderStatus.OPEN,
        created_at=created_at,
        due_at=calculate_due_at(priority, created_at),
    )

    session.add(work_order)
    session.commit()
    session.refresh(work_order)

    return work_order


def update_work_order_status(
    session: Session,
    work_order: WorkOrder,
    new_status: WorkOrderStatus,
    now: datetime | None = None,
) -> WorkOrder:
    """Apply an allowed work-order status transition."""
    allowed_transitions = {
        WorkOrderStatus.OPEN: WorkOrderStatus.IN_PROGRESS,
        WorkOrderStatus.IN_PROGRESS: WorkOrderStatus.COMPLETED,
    }

    expected_status = allowed_transitions.get(work_order.status)

    if new_status != expected_status:
        raise ValueError(
            f"Invalid status transition: "
            f"{work_order.status.value} -> {new_status.value}"
        )

    work_order.status = new_status

    if new_status == WorkOrderStatus.COMPLETED:
        work_order.completed_at = now or utc_now()

    session.add(work_order)
    session.commit()
    session.refresh(work_order)

    return work_order


def calculate_metrics(
    session: Session,
    now: datetime | None = None,
) -> dict[str, int]:
    """Calculate management metrics for all work orders."""
    current_time = now or utc_now()
    work_orders = session.exec(select(WorkOrder)).all()

    metrics = {
        "total": len(work_orders),
        "open": 0,
        "in_progress": 0,
        "completed": 0,
        "overdue": 0,
    }

    for work_order in work_orders:
        if work_order.status == WorkOrderStatus.OPEN:
            metrics["open"] += 1
        elif work_order.status == WorkOrderStatus.IN_PROGRESS:
            metrics["in_progress"] += 1
        elif work_order.status == WorkOrderStatus.COMPLETED:
            metrics["completed"] += 1

        if (
            work_order.status != WorkOrderStatus.COMPLETED
            and work_order.due_at < current_time
        ):
            metrics["overdue"] += 1

    return metrics