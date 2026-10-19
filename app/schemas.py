from datetime import datetime

from sqlmodel import SQLModel

from app.models import Criticality, Priority, WorkOrderStatus


class AssetCreate(SQLModel):
    name: str
    location: str
    criticality: Criticality


class AssetRead(SQLModel):
    id: int
    name: str
    location: str
    criticality: Criticality


class WorkOrderCreate(SQLModel):
    asset_id: int
    title: str
    priority: Priority


class WorkOrderRead(SQLModel):
    id: int
    asset_id: int
    title: str
    priority: Priority
    status: WorkOrderStatus
    created_at: datetime
    due_at: datetime
    completed_at: datetime | None


class WorkOrderStatusUpdate(SQLModel):
    status: WorkOrderStatus


class MetricsRead(SQLModel):
    total: int
    open: int
    in_progress: int
    completed: int
    overdue: int