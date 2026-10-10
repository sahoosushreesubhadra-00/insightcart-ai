import os
import sys

# Add /app to Python path so the app package can be imported
sys.path.insert(
    0,
    os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            ".."
        )
    )
)

from app.database.database import SessionLocal
from app.ml.train import train_customer_spending_model


def main():

    db = SessionLocal()

    try:
        model, metrics = train_customer_spending_model(db)

        print("\nTraining completed successfully.")

        print("\nMetrics:")

        for name, value in metrics.items():
            print(f"{name}: {value}")

    finally:
        db.close()


if __name__ == "__main__":
    main()