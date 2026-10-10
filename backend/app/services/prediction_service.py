import os
import joblib
import pandas as pd

from sqlalchemy.orm import Session

from app.models.customer import Customer
from app.models.purchase import Purchase
from datetime import datetime


MODEL_PATH = "/app/models/customer_spending_model.joblib"


class PredictionService:

    @staticmethod
    def load_model():
        if not os.path.exists(MODEL_PATH):
            raise FileNotFoundError(
                "Trained model not found. Please train the model first."
            )

        return joblib.load(MODEL_PATH)

    @staticmethod
    def get_customer_features(
        db: Session,
        customer_id: int
    ) -> pd.DataFrame:

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

        # reference_date = max(purchase_dates)

        # recency_days = (
        #     reference_date - latest_purchase
        # ).days
        reference_date = datetime.now()

        recency_days = (
            reference_date - latest_purchase
        ).days

        return pd.DataFrame([{
            "purchase_frequency": purchase_frequency,
            "average_order_value": average_order_value,
            "total_quantity": total_quantity,
            "category_count": category_count,
            "unique_product_count": unique_product_count,
            "recency_days": recency_days,
            "age": customer.age,
            "gender": customer.gender,
            "city": customer.city,
            "state": customer.state,
            "country": customer.country,
        }])

    @staticmethod
    def predict_customer_spending(
        db: Session,
        customer_id: int
    ):

        model = PredictionService.load_model()

        features = PredictionService.get_customer_features(
            db,
            customer_id
        )

        prediction = model.predict(features)

        predicted_spend = float(
            prediction[0]
        )

        return {
            "customer_id": customer_id,
            "predicted_spend": round(
                predicted_spend,
                2
            )
        }