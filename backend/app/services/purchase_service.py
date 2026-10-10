from sqlalchemy.orm import Session

from app.repositories.purchase_repository import PurchaseRepository
from app.repositories.customer_repository import CustomerRepository
from app.schemas.purchase import (
    PurchaseCreate,
    PurchaseUpdate,
)


class PurchaseService:

    @staticmethod
    def create_purchase(
        db: Session,
        purchase: PurchaseCreate
    ):

        # Verify that the customer exists
        customer = CustomerRepository.get_by_id(
            db,
            purchase.customer_id
        )

        if not customer:
            raise ValueError(
                "Customer not found."
            )

        return PurchaseRepository.create(
            db,
            purchase
        )

    @staticmethod
    def get_purchase(
        db: Session,
        purchase_id: int
    ):

        purchase = PurchaseRepository.get_by_id(
            db,
            purchase_id
        )

        if not purchase:
            raise ValueError(
                "Purchase not found."
            )

        return purchase

    @staticmethod
    def get_all_purchases(
        db: Session
    ):

        return PurchaseRepository.get_all(db)

    @staticmethod
    def get_customer_purchases(
        db: Session,
        customer_id: int
    ):

        # Verify customer exists
        customer = CustomerRepository.get_by_id(
            db,
            customer_id
        )

        if not customer:
            raise ValueError(
                "Customer not found."
            )

        return PurchaseRepository.get_by_customer(
            db,
            customer_id
        )

    @staticmethod
    def update_purchase(
        db: Session,
        purchase_id: int,
        purchase_data: PurchaseUpdate
    ):

        purchase = PurchaseRepository.get_by_id(
            db,
            purchase_id
        )

        if not purchase:
            raise ValueError(
                "Purchase not found."
            )

        return PurchaseRepository.update(
            db,
            purchase,
            purchase_data
        )

    @staticmethod
    def delete_purchase(
        db: Session,
        purchase_id: int
    ):

        purchase = PurchaseRepository.get_by_id(
            db,
            purchase_id
        )

        if not purchase:
            raise ValueError(
                "Purchase not found."
            )

        PurchaseRepository.delete(
            db,
            purchase
        )

        return {
            "message": "Purchase deleted successfully."
        }