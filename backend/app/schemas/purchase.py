from datetime import datetime

from pydantic import BaseModel, Field


class PurchaseBase(BaseModel):

    customer_id: int

    product_name: str = Field(
        ...,
        min_length=1,
        max_length=255
    )

    category: str = Field(
        ...,
        min_length=1,
        max_length=100
    )

    quantity: int = Field(
        ...,
        gt=0
    )

    unit_price: float = Field(
        ...,
        gt=0
    )

    total_amount: float = Field(
        ...,
        gt=0
    )

    purchase_date: datetime


class PurchaseCreate(PurchaseBase):
    pass


class PurchaseUpdate(BaseModel):

    product_name: str | None = Field(
        default=None,
        min_length=1,
        max_length=255
    )

    category: str | None = Field(
        default=None,
        min_length=1,
        max_length=100
    )

    quantity: int | None = Field(
        default=None,
        gt=0
    )

    unit_price: float | None = Field(
        default=None,
        gt=0
    )

    total_amount: float | None = Field(
        default=None,
        gt=0
    )

    purchase_date: datetime | None = None


class PurchaseResponse(PurchaseBase):

    id: int

    class Config:
        from_attributes = True


class PurchaseListResponse(BaseModel):

    total: int
    purchases: list[PurchaseResponse]