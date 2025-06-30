from sqlalchemy.exc import SQLAlchemyError
from datamanager.database import SessionLocal
from typing import Union, Tuple
from datamanager.models import User, Product, Order, OrderItem, Invoice, Reminder, Shipment
from datamanager.data_manager_interface import DataManagerInterface

class PostgresDataManager(DataManagerInterface):
    def __init__(self):
        self.db = SessionLocal()

    def commit_only(self) -> Tuple[Union[str, dict], int]:
        try:
            self.db.commit()
            return "", 200
        except SQLAlchemyError:
            self.db.rollback()
            return {'error': 'Sorry, something went wrong while processing your request. Please try again in a few moments.'}, 500

    def add_element(self, element: Union[User, Product, Order, OrderItem, Invoice, Reminder, Shipment]) -> Tuple[dict, int]:
        try:
            self.db.add(element)
            return self.commit_only()
        except SQLAlchemyError:
            return {'error': 'Sorry, something went wrong while processing your request. Please try again in a few moments.'}, 500
