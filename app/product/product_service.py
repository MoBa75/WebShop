from app.models import Product
from typing import Tuple, Optional, List, Union
from app.data_manager_interface import DataManagerInterface
from fastapi import HTTPException
import os
import re
import shutil
import logging
from sqlalchemy.orm import Session


def create_product_image_folder(product_name: str) -> str:
    """
    Creates a sanitized folder for storing product images.

    This function takes a product name, sanitizes it by replacing non-word characters
    with underscores, and uses it to create a folder path under 'static/product_images/'.
    If the folder does not already exist, it will be created.

    Args:
        product_name (str): The name of the product used to generate the folder name.

    Returns:
        str: The full path to the created (or existing) image folder.

    Raises:
        Exception: If an error occurs while creating the folder.
    """
    safe_name = re.sub(r'\W+', '_', product_name.strip()).lower()
    folder_path = os.path.join("static", "product_images", safe_name)

    try:
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
            logger.info(f"Created folder for product images: {folder_path}")
        else:
            logger.debug(f"Folder already exists: {folder_path}")
    except Exception as e:
        logger.error(f"Failed to create folder '{folder_path}': {e}")
        raise

    return folder_path


def delete_product_image_folder(product_name: str):
    """
    Deletes the image folder associated with a given product name.
    This function constructs a sanitized folder name based on the product name
    and attempts to remove the corresponding directory from the filesystem.

    Args:
        product_name (str): The name of the product whose image folder should be deleted.

    Logs:
        - Info log if the folder was successfully deleted.
        - Warning log if the folder does not exist.
        - Error log if an exception occurs during deletion.
    """
    safe_name = re.sub(r'\W+', '_', product_name.strip()).lower()
    folder_path = os.path.join("static", "product_images", safe_name)

    try:
        if os.path.exists(folder_path):
            shutil.rmtree(folder_path)
            logger.info(f"Deleted image folder: {folder_path}")
        else:
            logger.warning(f"Image folder not found: {folder_path}")
    except Exception as error:
        logger.error(f"Error deleting image folder {folder_path}: {error}")


def product_exists_by_name(db: Session, name: str) -> bool:
    """
    Checks whether a product with the given name exists in the database.

    Args:
        db (Session): The active SQLAlchemy database session.
        name (str): The name of the product to check.

    Returns:
        bool: True if a product with the specified name exists, False otherwise.
    """
    return db.query(Product).filter(Product.name == name).first() is not None


def product_exists_by_id(db: Session, product_id: int) -> bool:
    """
    Checks whether a product with the given ID exists in the database.

    Args:
        db (Session): The active SQLAlchemy database session.
        product_id (int): The ID of the product to check.

    Returns:
        bool: True if a product with the specified ID exists, False otherwise.
    """
    return db.query(Product).filter(Product.id == product_id).first() is not None


class ProductService:
    """
    Service class responsible for managing product-related operations.
    Includes creation, retrieval, updating, deletion, and stock control.
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
            if hasattr(product, key) and value is not None:
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
        delete_product_image_folder(product.name)
        return self.data_manager.delete_element(product)

    def check_product_stock(self, product_id, requested_quantity: int):
        """
        Validates whether the product has sufficient stock for the requested quantity.

        Args:
            product (Product): The product instance to check.
            requested_quantity (int): The quantity the user wants to purchase.

        Raises:
            HTTPException: If the product is out of stock or not enough is available.
        """
        product = self.data_manager.get_by_id(Product, product_id)
        if product.stock == 0:
            raise HTTPException(status_code=400, detail=f"Product '{product.name}' is currently out of stock.")

        if product.stock < requested_quantity:
            raise HTTPException(
                status_code=409,
                detail=f"Only {product.stock} units of '{product.name}' are available. Do you want to proceed with that amount?"
            )

    def reduce_product_stock(self, product_id, quantity: int):
        """
        Reduces the product's stock by the given quantity.

        Args:
            product (Product): The product to update.
            quantity (int): The quantity to subtract from stock.
        """
        product = self.data_manager.get_by_id(Product, product_id)
        product.stock -= quantity

    def increase_product_stock(self, product: Product, quantity: int):
        """
        Increases the product's stock by the given quantity.

        Args:
            product (Product): The product to update.
            quantity (int): The quantity to add to stock.
        """
        product.stock += quantity

    def reset_product_stock(self, product: Product, previous_quantity: int):
        """
        Resets the product's stock to a previous value (e.g., after a failed transaction).

        Args:
            product (Product): The product to update.
            previous_quantity (int): The stock value to restore.
        """
        product.stock = previous_quantity
