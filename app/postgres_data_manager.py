from sqlalchemy.exc import SQLAlchemyError
from app.database import SessionLocal
from typing import Union, Tuple
from app.models import User, Product, Order, OrderItem, Invoice, Reminder, Shipment
from app.data_manager_interface import DataManagerInterface


class PostgresDataManager(DataManagerInterface):
    """
    Concrete implementation of the DataManagerInterface for PostgreSQL using SQLAlchemy.
    Provides generic methods for committing transactions and performing CRUD operations.
    """

    def __init__(self):
        """
        Initializes the database session using SQLAlchemy's SessionLocal factory.
        """
        self.db = SessionLocal()

    def commit_only(self) -> Tuple[Union[str, dict], int]:
        """
        Commits the current database session.

        Returns:
            Tuple containing an empty string and 200 on success,
            or an error message and 500 on failure.
        """
        try:
            self.db.commit()
            return "", 200
        except SQLAlchemyError:
            self.db.rollback()
            return {'error': 'Sorry, something went wrong while processing your request. Please try again in a few moments.'}, 500

    def add_element(self, element: Union[User, Product, Order, OrderItem, Invoice, Reminder, Shipment]) -> Tuple[dict, int]:
        """
        Adds a new database object and commits the transaction.

        Args:
            element: A SQLAlchemy model instance to add to the database.

        Returns:
            Tuple containing an empty string and 200 on success,
            or an error message and 500 on failure.
        """
        try:
            self.db.add(element)
            return self.commit_only()
        except SQLAlchemyError:
            return {'error': 'Sorry, something went wrong while processing your request. Please try again in a few moments.'}, 500

    def get_by_id(self, model, element_id: int):
        """
        Retrieves a database record by its ID.

        Args:
            model: The SQLAlchemy model class.
            element_id: The ID of the element to retrieve.

        Returns:
            The found object on success,
            or an error dictionary and status code on failure.
        """
        try:
            return self.db.query(model).filter(model.id == element_id).first()
        except SQLAlchemyError:
            return {
                'error': 'Sorry, something went wrong while processing your request. Please try again in a few moments.'}, 500

    def get_all(self, model):
        """
        Retrieves all records for a given model.

        Args:
            model: The SQLAlchemy model class.

        Returns:
            A list of all model instances on success,
            or an error dictionary and status code on failure.
        """
        try:
            return self.db.query(model).all()
        except SQLAlchemyError:
            return {
                'error': 'Sorry, something went wrong while processing your request. Please try again in a few moments.'}, 500

    def delete_element(self, element) -> Tuple[Union[str, dict], int]:
        """
        Deletes a given object and commits the transaction.

        Args:
            element: The SQLAlchemy model instance to delete.

        Returns:
            Tuple containing an empty string and 200 on success,
            or an error message and 500 on failure.
        """
        try:
            self.db.delete(element)
            return self.commit_only()
        except SQLAlchemyError:
            return {
                'error': 'Sorry, something went wrong while processing your request. Please try again in a few moments.'}, 500
