import pandas as pd
from sqlalchemy.orm import Session

from app.models.customer import Customer
from app.models.purchase import Purchase


def load_purchase_data(db: Session) -> pd.DataFrame:
    """
    Load customer purchase data from PostgreSQL
    into a Pandas DataFrame for ML processing.
    """

    rows = (
        db.query(
            Customer.id.label("customer_id"),
            Customer.first_name,
            Customer.last_name,
            Customer.gender,
            Customer.age,
            Customer.city,
            Customer.state,
            Customer.country,
            Purchase.id.label("purchase_id"),
            Purchase.product_name,
            Purchase.category,
            Purchase.quantity,
            Purchase.unit_price,
            Purchase.total_amount,
            Purchase.purchase_date,
        )
        .join(
            Purchase,
            Customer.id == Purchase.customer_id
        )
        .all()
    )

    data = [
        {
            "customer_id": row.customer_id,
            "first_name": row.first_name,
            "last_name": row.last_name,
            "gender": row.gender,
            "age": row.age,
            "city": row.city,
            "state": row.state,
            "country": row.country,
            "purchase_id": row.purchase_id,
            "product_name": row.product_name,
            "category": row.category,
            "quantity": row.quantity,
            "unit_price": row.unit_price,
            "total_amount": row.total_amount,
            "purchase_date": row.purchase_date,
        }
        for row in rows
    ]

    df = pd.DataFrame(data)

    if df.empty:
        return df

    # Ensure purchase date is a proper datetime column
    df["purchase_date"] = pd.to_datetime(
        df["purchase_date"],
        errors="coerce"
    )

    # Ensure numerical columns have correct types
    df["age"] = pd.to_numeric(
        df["age"],
        errors="coerce"
    )

    df["quantity"] = pd.to_numeric(
        df["quantity"],
        errors="coerce"
    )

    df["unit_price"] = pd.to_numeric(
        df["unit_price"],
        errors="coerce"
    )

    df["total_amount"] = pd.to_numeric(
        df["total_amount"],
        errors="coerce"
    )

    return df