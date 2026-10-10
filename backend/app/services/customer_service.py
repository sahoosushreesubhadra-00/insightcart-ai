from sqlalchemy.orm import Session

from app.repositories.customer_repository import CustomerRepository
from app.schemas.customer import CustomerCreate, CustomerUpdate


class CustomerService:

    @staticmethod
    def create_customer(
        db: Session,
        customer: CustomerCreate
    ):

        # Check whether email already exists
        existing_customer = CustomerRepository.get_by_email(
            db,
            customer.email
        )

        if existing_customer:
            raise ValueError(
                "Customer with this email already exists."
            )

        return CustomerRepository.create(
            db,
            customer
        )

    @staticmethod
    def get_customer(
        db: Session,
        customer_id: int
    ):

        customer = CustomerRepository.get_by_id(
            db,
            customer_id
        )

        if not customer:
            raise ValueError(
                "Customer not found."
            )

        return customer

    @staticmethod
    def get_all_customers(
        db: Session
    ):

        return CustomerRepository.get_all(db)

    @staticmethod
    def update_customer(
        db: Session,
        customer_id: int,
        customer_data: CustomerUpdate
    ):

        # Check whether customer exists
        db_customer = CustomerRepository.get_by_id(
            db,
            customer_id
        )

        if not db_customer:
            raise ValueError(
                "Customer not found."
            )

        # If email is being changed,
        # make sure another customer isn't using it.
        if customer_data.email:

            existing_customer = (
                CustomerRepository.get_by_email(
                    db,
                    customer_data.email
                )
            )

            if (
                existing_customer
                and existing_customer.id != customer_id
            ):
                raise ValueError(
                    "Customer with this email already exists."
                )

        return CustomerRepository.update(
            db,
            db_customer,
            customer_data
        )

    @staticmethod
    def delete_customer(
        db: Session,
        customer_id: int
    ):

        db_customer = CustomerRepository.get_by_id(
            db,
            customer_id
        )

        if not db_customer:
            raise ValueError(
                "Customer not found."
            )

        CustomerRepository.delete(
            db,
            db_customer
        )

        return {
            "message": "Customer deleted successfully."
        }