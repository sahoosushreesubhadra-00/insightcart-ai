from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.api.dependencies import get_current_user

from app.schemas.purchase import (
    PurchaseCreate,
    PurchaseUpdate,
    PurchaseResponse,
    PurchaseListResponse,
)

from app.services.purchase_service import PurchaseService


router = APIRouter(
    prefix="/purchases",
    tags=["Purchases"]
)


@router.post(
    "",
    response_model=PurchaseResponse,
    status_code=status.HTTP_201_CREATED
)
def create_purchase(
    purchase: PurchaseCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    try:

        return PurchaseService.create_purchase(
            db,
            purchase
        )

    except ValueError as e:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )


@router.get(
    "",
    response_model=PurchaseListResponse
)
def get_purchases(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):

    purchases = PurchaseService.get_all_purchases(
        db
    )

    return {
        "total": len(purchases),
        "purchases": purchases
    }


@router.get(
    "/{purchase_id}",
    response_model=PurchaseResponse
)
def get_purchase(
    purchase_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):

    try:

        return PurchaseService.get_purchase(
            db,
            purchase_id
        )

    except ValueError as e:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )


@router.get(
    "/customer/{customer_id}",
    response_model=PurchaseListResponse
)
def get_customer_purchases(
    customer_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):

    try:

        purchases = PurchaseService.get_customer_purchases(
            db,
            customer_id
        )

        return {
            "total": len(purchases),
            "purchases": purchases
        }

    except ValueError as e:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )


@router.put(
    "/{purchase_id}",
    response_model=PurchaseResponse
)
def update_purchase(
    purchase_id: int,
    purchase: PurchaseUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):

    try:

        return PurchaseService.update_purchase(
            db,
            purchase_id,
            purchase
        )

    except ValueError as e:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )


@router.delete(
    "/{purchase_id}"
)
def delete_purchase(
    purchase_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):

    try:

        return PurchaseService.delete_purchase(
            db,
            purchase_id
        )

    except ValueError as e:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )