from sqlalchemy.orm import Session
from datetime import datetime
from fastapi import HTTPException
from datamanager.models import Order, OrderItem, User, Product
from datamanager.services import user_exists_by_id, product_exists_by_id, validate_quantity, reduce_stock_on_checkout
import logging

logger = logging.getLogger(__name__)

def get_or_create_cart_order(db: Session, user_id: int) -> Order:
    """
    Retrieves an existing cart order or creates a new one for the user.

    Args:
        db (Session): SQLAlchemy session.
        user_id (int): ID of the user.

    Returns:
        Order: Existing or newly created cart order.
    """
    try:
        cart_order = db.query(Order).filter(Order.user_id == user_id, Order.status == "im_warenkorb").first()
        if cart_order:
            return cart_order
        new_order = Order(user_id=user_id, date=datetime.utcnow(), status="im_warenkorb")
        db.add(new_order)
        db.flush()
        return new_order
    except Exception as error:
        logger.error(f"Error getting or creating cart order: {error}")
        raise HTTPException(status_code=500, detail="Error processing cart order")

def add_to_cart(db: Session, user_id: int, product_id: int, quantity: int):
    """
    Adds a product to the user's cart. Updates quantity if already present.

    Args:
        db (Session): SQLAlchemy session.
        user_id (int): ID of the user.
        product_id (int): ID of the product.
        quantity (int): Quantity to add.

    Returns:
        dict: Confirmation message.
    """
    try:
        if not user_exists_by_id(db, user_id):
            raise HTTPException(status_code=404, detail="User not found")
        if not product_exists_by_id(db, product_id):
            raise HTTPException(status_code=404, detail="Product not found")

        validate_quantity(quantity)

        order = get_or_create_cart_order(db, user_id)
        existing_item = db.query(OrderItem).filter(OrderItem.order_id == order.id, OrderItem.product_id == product_id).first()
        product = db.query(Product).filter(Product.id == product_id).first()

        if existing_item:
            existing_item.quantity += quantity
        else:
            new_item = OrderItem(
                order_id=order.id,
                product_id=product_id,
                quantity=quantity,
                unit_price=product.price
            )
            db.add(new_item)

        db.commit()
        return {"message": "Product added to cart."}
    except HTTPException:
        raise
    except Exception as error:
        logger.error(f"Error adding to cart: {error}")
        raise HTTPException(status_code=500, detail="Error adding to cart")

def update_cart_item(db: Session, user_id: int, product_id: int, quantity: int):
    """
    Updates the quantity of a product in the user's cart.

    Args:
        db (Session): SQLAlchemy session.
        user_id (int): ID of the user.
        product_id (int): ID of the product.
        quantity (int): New quantity value.

    Returns:
        dict: Confirmation message.
    """
    try:
        validate_quantity(quantity)

        order = get_or_create_cart_order(db, user_id)
        item = db.query(OrderItem).filter(OrderItem.order_id == order.id, OrderItem.product_id == product_id).first()
        if not item:
            raise HTTPException(status_code=404, detail="Product not in cart")
        item.quantity = quantity
        db.commit()
        return {"message": "Cart item updated."}
    except HTTPException:
        raise
    except Exception as error:
        logger.error(f"Error updating cart item: {error}")
        raise HTTPException(status_code=500, detail="Error updating cart item")

def remove_from_cart(db: Session, user_id: int, product_id: int):
    """
    Removes a product from the user's cart.

    Args:
        db (Session): SQLAlchemy session.
        user_id (int): ID of the user.
        product_id (int): ID of the product.

    Returns:
        dict: Confirmation message.
    """
    try:
        order = get_or_create_cart_order(db, user_id)
        item = db.query(OrderItem).filter(OrderItem.order_id == order.id, OrderItem.product_id == product_id).first()
        if not item:
            raise HTTPException(status_code=404, detail="Product not in cart")
        db.delete(item)
        db.commit()
        return {"message": "Product removed from cart."}
    except HTTPException:
        raise
    except Exception as error:
        logger.error(f"Error removing product from cart: {error}")
        raise HTTPException(status_code=500, detail="Error removing product from cart")

def get_cart(db: Session, user_id: int):
    """
    Retrieves the current cart for the user.

    Args:
        db (Session): SQLAlchemy session.
        user_id (int): ID of the user.

    Returns:
        dict: Cart contents.
    """
    try:
        order = db.query(Order).filter(Order.user_id == user_id, Order.status == "im_warenkorb").first()
        if not order:
            return {"message": "Cart is empty", "items": []}
        items = db.query(OrderItem).filter(OrderItem.order_id == order.id).all()
        return {"order_id": order.id, "items": items}
    except Exception as error:
        logger.error(f"Error retrieving cart: {error}")
        raise HTTPException(status_code=500, detail="Error retrieving cart")

def checkout_cart(db: Session, user_id: int):
    """
    Finalizes the user's cart by reducing product stock and marking the order as completed.

    Args:
        db (Session): SQLAlchemy session.
        user_id (int): ID of the user.

    Returns:
        dict: Confirmation message.
    """
    try:
        order = db.query(Order).filter(Order.user_id == user_id, Order.status == "im_warenkorb").first()
        if not order:
            raise HTTPException(status_code=404, detail="No cart to checkout")

        # Reduce stock for all items in the order
        reduce_stock_on_checkout(db, order)

        # Finalize order
        order.status = "abgeschlossen"
        order.date = datetime.utcnow()
        db.commit()
        return {"message": "Order checked out successfully"}
    except HTTPException:
        raise
    except Exception as error:
        logger.error(f"Error during checkout: {error}")
        raise HTTPException(status_code=500, detail="Error during checkout")


def get_user_orders(db: Session, user_id: int):
    """
    Retrieves all completed orders for a user.

    Args:
        db (Session): SQLAlchemy session.
        user_id (int): ID of the user.

    Returns:
        list: List of completed orders.
    """
    try:
        if not user_exists_by_id(db, user_id):
            raise HTTPException(status_code=404, detail="User not found")
        return db.query(Order).filter(Order.user_id == user_id, Order.status == "abgeschlossen").all()
    except HTTPException:
        raise
    except Exception as error:
        logger.error(f"Error retrieving user orders: {error}")
        raise HTTPException(status_code=500, detail="Error retrieving user orders")
