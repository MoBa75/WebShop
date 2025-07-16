from abc import ABC, abstractmethod
from typing import Union, Tuple
from app.models import User, Product, Order, OrderItem, Invoice, Reminder, Shipment

class DataManagerInterface(ABC):
    @abstractmethod
    def add_element(self, element: Union[User, Product, Order, OrderItem, Invoice, Reminder, Shipment]) -> Tuple[dict, int]:
        """Adds an element to the database and commits the transaction."""
        pass

    @abstractmethod
    def commit_only(self) -> Tuple[Union[str, dict], int]:
        """Commits the current database session."""
        pass

    @abstractmethod
    def get_by_id(self, model, element_id: int):
        """Retrieves a single element by its ID."""
        pass

    @abstractmethod
    def get_all(self, model):
        """Retrieves all elements of a model."""
        pass

    @abstractmethod
    def delete_element(self, element) -> Tuple[Union[str, dict], int]:
        """Deletes an element and commits the transaction."""
        pass
