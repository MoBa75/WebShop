from datamanager.models import Product
from datamanager.services import create_product_image_folder, product_exists_by_name, product_exists_by_id
from typing import Tuple, Optional, List, Union
from datamanager.data_manager_interface import DataManagerInterface


class ProductService:
    """
    Service class responsible for managing product-related operations.
    Includes creation, retrieval, updating, and deletion of products.
    """

    def __init__(self, data_manager: DataManagerInterface):
        """
        Initializes the ProductService with a data manager.

        Args:
            data_manager (DataManagerInterface): Interface used for interacting with the database.
        """
        self.data_manager = data_manager

    def create_product(self, name: str, unit: str, price: float, description: str, stock: int) -> Tuple[dict, int]:
        """
        Creates a new product and its corresponding image folder if the product does not already exist.

        Args:
            name (str): The product name.
            unit (str): Unit of measurement (e.g., "piece", "box").
            price (float): Price of the product.
            description (str): Product description.
            stock (int): Available stock quantity.

        Returns:
            Tuple[dict, int]: A success or error message with an HTTP status code.
        """
        try:
            if product_exists_by_name(self.data_manager.db, name):
                return {"error": "A product with this name already exists."}, 409

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
        """
        Retrieves a product by its ID.

        Args:
            product_id (int): ID of the product.

        Returns:
            Union[Product, Tuple[dict, int]]: The product object or an error message with status code.
        """
        product = self.data_manager.get_by_id(Product, product_id)
        if not product:
            return {"error": "Product not found"}, 404
        return product

    def get_all_products(self) -> Union[List[Product], Tuple[dict, int]]:
        """
        Retrieves all products.

        Returns:
            Union[List[Product], Tuple[dict, int]]: A list of product objects or an error message with status code.
        """
        return self.data_manager.get_all(Product)

    def update_product(self, product_id: int, **kwargs) -> Tuple[Union[str, dict], int]:
        """
        Updates an existing product's attributes.

        Args:
            product_id (int): ID of the product to update.
            **kwargs: Attributes to update as key-value pairs.

        Returns:
            Tuple[Union[str, dict], int]: A success or error message with an HTTP status code.
        """
        if not product_exists_by_id(self.data_manager.db, product_id):
            return {"error": "Product not found."}, 404

        product = self.data_manager.get_by_id(Product, product_id)
        for key, value in kwargs.items():
            if hasattr(product, key):
                setattr(product, key, value)
        return self.data_manager.commit_only()

    def delete_product(self, product_id: int) -> Tuple[Union[str, dict], int]:
        """
        Deletes a product by its ID.

        Args:
            product_id (int): ID of the product to delete.

        Returns:
            Tuple[Union[str, dict], int]: A success or error message with an HTTP status code.
        """
        if not product_exists_by_id(self.data_manager.db, product_id):
            return {"error": "Product not found."}, 404

        product = self.data_manager.get_by_id(Product, product_id)
        return self.data_manager.delete_element(product)
