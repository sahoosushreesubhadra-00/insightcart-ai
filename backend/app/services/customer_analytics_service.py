from sqlalchemy.orm import Session

from app.models.customer import Customer
from app.models.purchase import Purchase
from app.services.prediction_service import PredictionService


class CustomerAnalyticsService:

    @staticmethod
    def get_customer_analytics(
        db: Session,
        customer_id: int
    ):

        customer = (
            db.query(Customer)
            .filter(Customer.id == customer_id)
            .first()
        )

        if not customer:
            raise ValueError("Customer not found.")

        purchases = (
            db.query(Purchase)
            .filter(Purchase.customer_id == customer_id)
            .all()
        )

        if not purchases:
            raise ValueError(
                "Customer has no purchase history."
            )

        purchase_frequency = len(purchases)

        total_spend = sum(
            purchase.total_amount
            for purchase in purchases
        )

        average_order_value = (
            total_spend / purchase_frequency
        )

        total_quantity = sum(
            purchase.quantity
            for purchase in purchases
        )

        category_count = len(
            set(
                purchase.category
                for purchase in purchases
            )
        )

        unique_product_count = len(
            set(
                purchase.product_name
                for purchase in purchases
            )
        )

        purchase_dates = [
            purchase.purchase_date
            for purchase in purchases
        ]

        latest_purchase = max(purchase_dates)

        from datetime import datetime

        recency_days = (
            datetime.now() - latest_purchase
        ).days

        prediction = (
            PredictionService.predict_customer_spending(
                db,
                customer_id
            )
        )

        return {
            "customer": {
                "id": customer.id,
                "name": (
                    f"{customer.first_name} "
                    f"{customer.last_name}"
                ),
                "age": customer.age,
                "gender": customer.gender,
                "city": customer.city,
                "state": customer.state,
                "country": customer.country,
            },
            "purchase_summary": {
                "purchase_frequency": purchase_frequency,
                "total_spend": round(
                    float(total_spend),
                    2
                ),
                "average_order_value": round(
                    float(average_order_value),
                    2
                ),
                "total_quantity": total_quantity,
                "category_count": category_count,
                "unique_product_count": (
                    unique_product_count
                ),
                "recency_days": recency_days,
            },
            "prediction": prediction,
        }