from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datamanager.database import get_db
from datamanager.schemas import OrderCreate, OrderResponse
from datamanager.order_service import create_order

router = APIRouter(prefix="/orders", tags=["orders"])

@router.post("/", response_model=OrderResponse)
def create_new_order(order_data: OrderCreate, db: Session = Depends(get_db)):
    try:
        return create_order(db, order_data)
    except HTTPException as http_error:
        raise http_error
    except Exception as unexpected_error:
        raise HTTPException(status_code=500, detail=str(unexpected_error))
