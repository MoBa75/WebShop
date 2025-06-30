# datamanager/product_service.py

from datamanager.models import Product
from datamanager.services import create_product_image_folder
from typing import Tuple
from datamanager.data_manager_interface import DataManagerInterface

class ProductService:
    def __init__(self, data_manager: DataManagerInterface):
        self.data_manager = data_manager

    def create_product(self, name: str, unit: str, price: float, description: str, stock: int) -> Tuple[dict, int]:
        folder_path = create_product_image_folder(name)

        new_product = Product(
            name=name,
            unit=unit,
            price=price,
            description=description,
            stock=stock,
            image_path=folder_path
        )

        return self.data_manager.add_element(new_product)
