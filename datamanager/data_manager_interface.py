from abc import ABC, abstractmethod
from typing import Union, Tuple
from datamanager.models import User, Product, Order, OrderItem, Invoice, Reminder, Shipment

class DataManagerInterface(ABC):
    @abstractmethod
    def add_element(self, element: Union[User, Product, Order, OrderItem, Invoice, Reminder, Shipment]) -> Tuple[dict, int]:
        pass

    @abstractmethod
    def commit_only(self) -> Tuple[Union[str, dict], int]:
        pass
