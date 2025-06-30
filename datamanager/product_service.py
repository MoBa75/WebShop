from datamanager.models import Product
from datamanager.services import create_product_image_folder, product_exists_by_name, product_exists_by_id
from typing import Tuple, Optional, List, Union
from datamanager.data_manager_interface import DataManagerInterface
from sqlalchemy.exc import SQLAlchemyError


class ProductService:
    def __init__(self, data_manager: DataManagerInterface):
        self.data_manager = data_manager
        self.db = self.data_manager.db


    def create_product(self, name: str, unit: str, price: float, description: str, stock: int) -> \
    Tuple[dict, int]:
        try:
            if product_exists_by_name(self.db, name):
                return {"error": "A product with this name already exists."}, 409  # Conflict

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

        except OSError as e:
            return {"error": f"Could not create folder for product image: {e}"}, 500
        except Exception:
            return {"error": "Unexpected error while creating product."}, 500

    def get_product_by_id(self, product_id: int) -> Union[Product, Tuple[dict, int]]:
        try:
            product = self.db.query(Product).filter(Product.id == product_id).first()
            if not product:
                return {"error": "Product not found"}, 404
            return product
        except SQLAlchemyError:
            return {"error": "Database error occurred while fetching product."}, 500

    def get_all_products(self) -> Union[List[Product], Tuple[dict, int]]:
        try:
            return self.db.query(Product).all()
        except SQLAlchemyError:
            return {"error": "Database error occurred while fetching products."}, 500

    def update_product(self, product_id: int, **kwargs) -> Tuple[Union[str, dict], int]:
        if not product_exists_by_id(self.db, product_id):
            return {"error": "Product not found."}, 404

        try:
            product = self.db.query(Product).filter(Product.id == product_id).first()
            for key, value in kwargs.items():
                if hasattr(product, key):
                    setattr(product, key, value)
            return self.data_manager.commit_only()
        except SQLAlchemyError:
            return {"error": "Database error occurred while updating product."}, 500
        except Exception:
            return {"error": "Unexpected error while updating product."}, 500

    def delete_product(self, product_id: int) -> Tuple[Union[str, dict], int]:
        if not product_exists_by_id(self.db, product_id):
            return {"error": "Product not found."}, 404

        try:
            product = self.db.query(Product).filter(Product.id == product_id).first()
            self.db.delete(product)
            return self.data_manager.commit_only()
        except SQLAlchemyError:
            return {"error": "Database error occurred while deleting product."}, 500
        except Exception:
            return {"error": "Unexpected error while deleting product."}, 500