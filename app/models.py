from datetime import datetime
from enum import Enum

from sqlmodel import Field, SQLModel


class Criticality(str, Enum):
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"


class Priority(str, Enum):
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"


class WorkOrderStatus(str, Enum):
    OPEN = "OPEN"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"


class Asset(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    location: str
    criticality: Criticality


class WorkOrder(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    asset_id: int = Field(foreign_key="asset.id")
    title: str
    priority: Priority
    status: WorkOrderStatus = Field(default=WorkOrderStatus.OPEN)

    created_at: datetime
    due_at: datetime
    completed_at: datetime | None = None