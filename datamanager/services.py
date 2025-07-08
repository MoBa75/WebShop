import os
import re
import shutil
import logging
from fastapi import HTTPException
from sqlalchemy.orm import Session
from datamanager.models import Product, User, OrderItem, Order

logger = logging.getLogger(__name__)

def create_product_image_folder(product_name: str) -> str:
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
    return db.query(Product).filter(Product.name == name).first() is not None

def product_exists_by_id(db: Session, product_id: int) -> bool:
    return db.query(Product).filter(Product.id == product_id).first() is not None

def user_exists_by_id(db: Session, user_id: int) -> bool:
    return db.query(User).filter(User.id == user_id).first() is not None

def user_exists_by_email(db: Session, email: str) -> bool:
    return db.query(User).filter(User.email == email).first() is not None

def validate_quantity(quantity: int):
    if quantity <= 0:
        raise HTTPException(status_code=400, detail="Quantity must be greater than 0")

def reduce_stock_on_checkout(db: Session, order: Order):
    """
    Reduces stock levels for all items in a given order instance.

    Args:
        db (Session): SQLAlchemy session.
        order (Order): Order object to reduce stock for.

    Raises:
        HTTPException: If stock is insufficient for any item.
    """
    for item in order.items:
        product = db.query(Product).filter(Product.id == item.product_id).first()

        if not product:
            raise HTTPException(status_code=404, detail=f"Product with ID {item.product_id} not found.")

        if product.stock < item.quantity:
            raise HTTPException(
                status_code=409,
                detail=f"Not enough stock for product '{product.name}'. Available: {product.stock}, Required: {item.quantity}"
            )

        product.stock -= item.quantity

    db.commit()
    logger.info(f"Stock reduced for order {order.id}")