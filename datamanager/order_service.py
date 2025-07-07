from sqlalchemy.orm import Session
from datetime import datetime
from fastapi import HTTPException
from datamanager.models import Order, OrderItem, User, Product
from datamanager.schemas import OrderCreate
from datamanager.product_service import ProductService
from datamanager.postgres_data_manager import PostgresDataManager


def create_order(db: Session, order_data: OrderCreate):
    """
    Creates a new order for a user, deducts the stock for each ordered product,
    and ensures rollback with stock restoration in case of failure.

    Args:
        db (Session): The SQLAlchemy session object.
        order_data (OrderCreate): Contains user_id and a list of order items.

    Returns:
        Order: The newly created Order object.

    Raises:
        HTTPException: If the user does not exist, a product is not found,
                       or stock is insufficient.
    """
    user = db.query(User).filter(User.id == order_data.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Initialize product service with the current DB session
    product_service = ProductService(PostgresDataManager())
    product_service.data_manager.db = db

    new_order = Order(
        user_id=order_data.user_id,
        date=datetime.utcnow(),
        status="neu"
    )
    db.add(new_order)
    db.flush()  # ensures order.id is available

    stock_changes = []  # to track what needs to be rolled back if something fails

    try:
        for item in order_data.items:
            # Check and deduct stock using product service
            product_service.check_product_stock(item.product_id, item.quantity)
            product_service.reduce_product_stock(item.product_id, item.quantity)
            stock_changes.append((item.product_id, item.quantity))

            product = db.query(Product).filter(Product.id == item.product_id).first()

            order_item = OrderItem(
                order_id=new_order.id,
                product_id=item.product_id,
                quantity=item.quantity,
                unit_price=product.price
            )
            db.add(order_item)

        db.commit()
        db.refresh(new_order)
        return new_order

    except Exception as error:
        db.rollback()
        # Restore any stock that was already deducted
        for pid, qty in stock_changes:
            product_service.restore_product_stock(pid, qty)
        db.commit()
        raise HTTPException(status_code=500, detail=f"Order failed: {str(error)}")
