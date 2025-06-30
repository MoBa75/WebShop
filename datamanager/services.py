import os
import re
from datamanager.models import Product
from sqlalchemy.orm import Session


def create_product_image_folder(product_name: str):
    safe_name = re.sub(r'\W+', '_', product_name.strip()).lower()
    folder_path = os.path.join("static", "product_images", safe_name)

    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    return folder_path


def product_exists_by_name(db: Session, name: str) -> bool:
    return db.query(Product).filter(Product.name == name).first() is not None


def product_exists_by_id(db: Session, product_id: int) -> bool:
    return db.query(Product).filter(Product.id == product_id).first() is not None
