from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from app.database import get_session
from app.models import Asset, WorkOrder
from app.schemas import (
    AssetCreate,
    AssetRead,
    MetricsRead,
    WorkOrderCreate,
    WorkOrderRead,
    WorkOrderStatusUpdate,
)
from app.services import (
    calculate_metrics,
    create_work_order,
    update_work_order_status,
)


router = APIRouter()


@router.post("/assets", response_model=AssetRead, status_code=201)
def create_asset(
    asset_data: AssetCreate,
    session: Session = Depends(get_session),
):
    asset = Asset(
        name=asset_data.name,
        location=asset_data.location,
        criticality=asset_data.criticality,
    )

    session.add(asset)
    session.commit()
    session.refresh(asset)

    return asset


@router.get("/assets", response_model=list[AssetRead])
def list_assets(session: Session = Depends(get_session)):
    return session.exec(select(Asset)).all()


@router.post("/work-orders", response_model=WorkOrderRead, status_code=201)
def create_work_order_route(
    work_order_data: WorkOrderCreate,
    session: Session = Depends(get_session),
):
    asset = session.get(Asset, work_order_data.asset_id)

    if asset is None:
        raise HTTPException(status_code=404, detail="Asset not found")

    return create_work_order(
        session=session,
        asset_id=work_order_data.asset_id,
        title=work_order_data.title,
        priority=work_order_data.priority,
    )


@router.get("/work-orders", response_model=list[WorkOrderRead])
def list_work_orders(session: Session = Depends(get_session)):
    return session.exec(select(WorkOrder)).all()


@router.patch(
    "/work-orders/{work_order_id}/status",
    response_model=WorkOrderRead,
)
def change_work_order_status(
    work_order_id: int,
    status_data: WorkOrderStatusUpdate,
    session: Session = Depends(get_session),
):
    work_order = session.get(WorkOrder, work_order_id)

    if work_order is None:
        raise HTTPException(status_code=404, detail="Work order not found")

    try:
        return update_work_order_status(
            session=session,
            work_order=work_order,
            new_status=status_data.status,
        )
    except ValueError as exc:
        raise HTTPException(status_code=409, detail=str(exc)) from exc


@router.get("/metrics", response_model=MetricsRead)
def get_metrics(session: Session = Depends(get_session)):
    return calculate_metrics(session)