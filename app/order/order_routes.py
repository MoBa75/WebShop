from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.order.order_service import (
    add_to_cart,
    get_cart,
    update_cart_item,
    remove_from_cart,
    checkout_cart,
    get_user_orders,
)
from app.order.order_schemas import (
    CartAddItem,
    CartUpdateItem,
    CartRemoveItem,
    CartCheckout,
)

router = APIRouter(prefix="/orders", tags=["orders"])


@router.get("/cart/{user_id}")
def view_cart(user_id: int, db: Session = Depends(get_db)):
    """
    Retrieves the current cart for a user.
    """
    try:
        return get_cart(db, user_id)
    except Exception as error:
        raise HTTPException(status_code=500, detail=str(error))


@router.post("/cart/add")
def add_product_to_cart(payload: CartAddItem, db: Session = Depends(get_db)):
    """
    Adds a product to the user's cart using Pydantic schema.
    """
    try:
        return add_to_cart(db, payload.user_id, payload.product_id, payload.quantity)
    except HTTPException as http_error:
        raise http_error
    except Exception as error:
        raise HTTPException(status_code=500, detail=str(error))


@router.put("/cart/update")
def update_product_in_cart(payload: CartUpdateItem, db: Session = Depends(get_db)):
    """
    Updates the quantity of a product in the user's cart using Pydantic schema.
    """
    try:
        return update_cart_item(db, payload.user_id, payload.product_id, payload.quantity)
    except HTTPException as http_error:
        raise http_error
    except Exception as error:
        raise HTTPException(status_code=500, detail=str(error))


@router.delete("/cart/remove")
def remove_product_from_cart(payload: CartRemoveItem, db: Session = Depends(get_db)):
    """
    Removes a product from the user's cart using Pydantic schema.
    """
    try:
        return remove_from_cart(db, payload.user_id, payload.product_id)
    except HTTPException as http_error:
        raise http_error
    except Exception as error:
        raise HTTPException(status_code=500, detail=str(error))


@router.post("/cart/checkout")
def checkout_user_cart(payload: CartCheckout, db: Session = Depends(get_db)):
    """
    Finalizes the cart by changing its status to 'abgeschlossen' and deducting stock.
    """
    try:
        return checkout_cart(db, payload.user_id)
    except HTTPException as http_error:
        raise http_error
    except Exception as error:
        raise HTTPException(status_code=500, detail=str(error))


@router.get("/user/{user_id}")
def get_user_completed_orders(user_id: int, db: Session = Depends(get_db)):
    """
    Retrieves all completed orders for a given user.
    """
    try:
        return get_user_orders(db, user_id)
    except HTTPException as http_error:
        raise http_error
    except Exception as error:
        raise HTTPException(status_code=500, detail=str(error))
