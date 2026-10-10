from sqlalchemy.orm import Session

from app.models.customer import Customer
from app.schemas.customer import CustomerCreate, CustomerUpdate


class CustomerRepository:

    @staticmethod
    def create(db: Session, customer: CustomerCreate) -> Customer:
        """
        Create a new customer.
        """

        db_customer = Customer(
            first_name=customer.first_name,
            last_name=customer.last_name,
            email=customer.email,
            phone=customer.phone,
            gender=customer.gender,
            age=customer.age,
            city=customer.city,
            state=customer.state,
            country=customer.country,
            is_active=True,
        )

        db.add(db_customer)
        db.commit()
        db.refresh(db_customer)

        return db_customer

    @staticmethod
    def get_by_id(db: Session, customer_id: int) -> Customer | None:
        """
        Get customer by ID.
        """

        return (
            db.query(Customer)
            .filter(Customer.id == customer_id)
            .first()
        )

    @staticmethod
    def get_by_email(db: Session, email: str) -> Customer | None:
        """
        Get customer by email.
        """

        return (
            db.query(Customer)
            .filter(Customer.email == email)
            .first()
        )

    @staticmethod
    def get_all(db: Session) -> list[Customer]:
        """
        Get all customers.
        """

        return (
            db.query(Customer)
            .order_by(Customer.id)
            .all()
        )

    @staticmethod
    def update(
        db: Session,
        db_customer: Customer,
        customer: CustomerUpdate,
    ) -> Customer:
        """
        Update customer.
        """

        update_data = customer.model_dump(exclude_unset=True)

        for key, value in update_data.items():
            setattr(db_customer, key, value)

        db.commit()
        db.refresh(db_customer)

        return db_customer

    @staticmethod
    def delete(
        db: Session,
        db_customer: Customer,
    ) -> None:
        """
        Delete customer.
        """

        db.delete(db_customer)
        db.commit()