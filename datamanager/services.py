import os
import re
from datamanager.models import Product, User
from sqlalchemy.orm import Session


def create_product_image_folder(product_name: str) -> str:
    """
    Creates a folder for storing images of a specific product.
    The folder name is sanitized by replacing non-alphanumeric characters with underscores.

    Args:
        product_name (str): The name of the product.

    Returns:
        str: The path to the created (or existing) folder.
    """
    safe_name = re.sub(r'\W+', '_', product_name.strip()).lower()
    folder_path = os.path.join("static", "product_images", safe_name)

    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    return folder_path


def product_exists_by_name(db: Session, name: str) -> bool:
    """
    Checks whether a product with the given name already exists.

    Args:
        db (Session): SQLAlchemy session.
        name (str): The name of the product to check.

    Returns:
        bool: True if the product exists, False otherwise.
    """
    return db.query(Product).filter(Product.name == name).first() is not None


def product_exists_by_id(db: Session, product_id: int) -> bool:
    """
    Checks whether a product with the given ID exists.

    Args:
        db (Session): SQLAlchemy session.
        product_id (int): ID of the product to check.

    Returns:
        bool: True if the product exists, False otherwise.
    """
    return db.query(Product).filter(Product.id == product_id).first() is not None


def user_exists_by_id(db: Session, user_id: int) -> bool:
    """
    Checks whether a user with the given ID exists.

    Args:
        db (Session): SQLAlchemy session.
        user_id (int): ID of the user to check.

    Returns:
        bool: True if the user exists, False otherwise.
    """
    return db.query(User).filter(User.id == user_id).first() is not None


def user_exists_by_email(db: Session, email: str) -> bool:
    """
    Checks whether a user with the given email address already exists.

    Args:
        db (Session): SQLAlchemy session.
        email (str): Email address to check.

    Returns:
        bool: True if the user exists, False otherwise.
    """
    return db.query(User).filter(User.email == email).first() is not None

