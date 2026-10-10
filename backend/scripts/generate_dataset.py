import sys
import os

sys.path.insert(
    0,
    os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            ".."
        )
    )
)

import random
from datetime import datetime, timedelta

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import settings
from app.models.customer import Customer
from app.models.purchase import Purchase


# --------------------------------------------------
# Configuration
# --------------------------------------------------

NUM_CUSTOMERS = 100
MIN_PURCHASES = 3
MAX_PURCHASES = 10

random.seed(42)


# --------------------------------------------------
# Sample data
# --------------------------------------------------

FIRST_NAMES = [
    "John",
    "Jane",
    "Michael",
    "Sarah",
    "David",
    "Emily",
    "Robert",
    "Priya",
    "Amit",
    "Sneha",
    "Rahul",
    "Ananya",
    "Arjun",
    "Neha",
    "Rohan",
    "Pooja",
    "Vikram",
    "Kavya",
    "Daniel",
    "Olivia",
]

LAST_NAMES = [
    "Smith",
    "Johnson",
    "Williams",
    "Brown",
    "Davis",
    "Miller",
    "Patel",
    "Sharma",
    "Singh",
    "Das",
    "Sahoo",
    "Mishra",
    "Roy",
    "Gupta",
    "Mehta",
]

LOCATIONS = [
    ("Bhubaneswar", "Odisha", "India"),
    ("Kolkata", "West Bengal", "India"),
    ("Mumbai", "Maharashtra", "India"),
    ("Delhi", "Delhi", "India"),
    ("Bengaluru", "Karnataka", "India"),
    ("Hyderabad", "Telangana", "India"),
    ("Chennai", "Tamil Nadu", "India"),
    ("Pune", "Maharashtra", "India"),
    ("New York", "New York", "USA"),
    ("London", "England", "UK"),
]

PRODUCTS = {
    "Electronics": [
        ("Laptop", 60000),
        ("Smartphone", 30000),
        ("Headphones", 5000),
        ("Smart Watch", 8000),
        ("Tablet", 25000),
    ],
    "Clothing": [
        ("T-Shirt", 1200),
        ("Jeans", 2500),
        ("Jacket", 4500),
        ("Shoes", 3500),
        ("Dress", 3000),
    ],
    "Grocery": [
        ("Rice", 1200),
        ("Cooking Oil", 800),
        ("Coffee", 600),
        ("Snacks", 500),
        ("Cereal", 450),
    ],
    "Home": [
        ("Chair", 3000),
        ("Table", 7000),
        ("Lamp", 1800),
        ("Bedsheet", 1500),
        ("Cookware", 3500),
    ],
    "Beauty": [
        ("Face Wash", 500),
        ("Shampoo", 700),
        ("Perfume", 2500),
        ("Moisturizer", 900),
        ("Makeup Kit", 3000),
    ],
    "Sports": [
        ("Running Shoes", 4000),
        ("Yoga Mat", 1200),
        ("Cricket Bat", 3500),
        ("Football", 1500),
        ("Dumbbells", 2500),
    ],
}


# --------------------------------------------------
# Database
# --------------------------------------------------

engine = create_engine(settings.DATABASE_URL)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)


# --------------------------------------------------
# Customer generation
# --------------------------------------------------

def generate_customers(db):

    customers = []

    for _ in range(NUM_CUSTOMERS):

        first_name = random.choice(FIRST_NAMES)
        last_name = random.choice(LAST_NAMES)

        email = (
            f"{first_name.lower()}."
            f"{last_name.lower()}."
            f"{random.randint(1000, 99999)}"
            "@example.com"
        )

        phone = str(
            random.randint(
                6000000000,
                9999999999
            )
        )

        gender = random.choice(
            ["Male", "Female"]
        )

        age = random.randint(18, 65)

        city, state, country = random.choice(
            LOCATIONS
        )

        customer = Customer(
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone=phone,
            gender=gender,
            age=age,
            city=city,
            state=state,
            country=country,
            is_active=True,
        )

        db.add(customer)
        customers.append(customer)

    db.commit()

    for customer in customers:
        db.refresh(customer)

    return customers


# --------------------------------------------------
# Purchase generation
# --------------------------------------------------

def generate_purchases(db, customers):

    purchases = []

    end_date = datetime.now()
    start_date = end_date - timedelta(days=365)

    categories = list(PRODUCTS.keys())

    for customer in customers:

        number_of_purchases = random.randint(
            MIN_PURCHASES,
            MAX_PURCHASES
        )

        for _ in range(number_of_purchases):

            category = random.choice(
                categories
            )

            product_name, base_price = random.choice(
                PRODUCTS[category]
            )

            quantity = random.randint(1, 4)

            # Add some realistic price variation
            variation = random.uniform(
                0.90,
                1.10
            )

            unit_price = round(
                base_price * variation,
                2
            )

            total_amount = round(
                unit_price * quantity,
                2
            )

            purchase_date = (
                start_date
                + timedelta(
                    seconds=random.randint(
                        0,
                        int(
                            (
                                end_date - start_date
                            ).total_seconds()
                        )
                    )
                )
            )

            purchase = Purchase(
                customer_id=customer.id,
                product_name=product_name,
                category=category,
                quantity=quantity,
                unit_price=unit_price,
                total_amount=total_amount,
                purchase_date=purchase_date,
            )

            db.add(purchase)
            purchases.append(purchase)

    db.commit()

    return purchases


# --------------------------------------------------
# Main
# --------------------------------------------------

def main():

    db = SessionLocal()

    try:

        print("Generating customers...")

        customers = generate_customers(db)

        print(
            f"Created {len(customers)} customers."
        )

        print("Generating purchases...")

        purchases = generate_purchases(
            db,
            customers
        )

        print(
            f"Created {len(purchases)} purchases."
        )

        print(
            "Development dataset generated successfully."
        )

    except Exception as e:

        db.rollback()

        print(
            f"Dataset generation failed: {e}"
        )

        raise

    finally:

        db.close()


if __name__ == "__main__":
    main()