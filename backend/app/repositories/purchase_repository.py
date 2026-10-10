from sqlalchemy.orm import Session

from app.models.purchase import Purchase
from app.schemas.purchase import PurchaseCreate, PurchaseUpdate


class PurchaseRepository:

    @staticmethod
    def create(
        db: Session,
        purchase: PurchaseCreate
    ) -> Purchase:
        """
        Create a new purchase.
        """

        db_purchase = Purchase(
            customer_id=purchase.customer_id,
            product_name=purchase.product_name,
            category=purchase.category,
            quantity=purchase.quantity,
            unit_price=purchase.unit_price,
            total_amount=purchase.total_amount,
            purchase_date=purchase.purchase_date,
        )

        db.add(db_purchase)
        db.commit()
        db.refresh(db_purchase)

        return db_purchase

    @staticmethod
    def get_by_id(
        db: Session,
        purchase_id: int
    ) -> Purchase | None:
        """
        Get a purchase by ID.
        """

        return (
            db.query(Purchase)
            .filter(Purchase.id == purchase_id)
            .first()
        )

    @staticmethod
    def get_by_customer(
        db: Session,
        customer_id: int
    ) -> list[Purchase]:
        """
        Get all purchases for a customer.
        """

        return (
            db.query(Purchase)
            .filter(Purchase.customer_id == customer_id)
            .order_by(Purchase.id)
            .all()
        )

    @staticmethod
    def get_all(
        db: Session
    ) -> list[Purchase]:
        """
        Get all purchases.
        """

        return (
            db.query(Purchase)
            .order_by(Purchase.id)
            .all()
        )

    @staticmethod
    def update(
        db: Session,
        db_purchase: Purchase,
        purchase: PurchaseUpdate
    ) -> Purchase:
        """
        Update an existing purchase.
        """

        update_data = purchase.model_dump(
            exclude_unset=True
        )

        for key, value in update_data.items():
            setattr(
                db_purchase,
                key,
                value
            )

        db.commit()
        db.refresh(db_purchase)

        return db_purchase

    @staticmethod
    def delete(
        db: Session,
        db_purchase: Purchase
    ) -> None:
        """
        Delete a purchase.
        """

        db.delete(db_purchase)
        db.commit()