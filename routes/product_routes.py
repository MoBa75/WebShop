from fastapi import APIRouter, HTTPException
from datamanager.postgres_data_manager import PostgresDataManager
from datamanager.product_service import ProductService

router = APIRouter()
product_service = ProductService(PostgresDataManager())

@router.get("/", summary="Get all products")
def get_all_products():
    result = product_service.get_all_products()
    if isinstance(result, tuple):
        raise HTTPException(status_code=result[1], detail=result[0]["error"])
    return result

@router.get("/{product_id}", summary="Get product by ID")
def get_product(product_id: int):
    result = product_service.get_product_by_id(product_id)
    if isinstance(result, tuple):
        raise HTTPException(status_code=result[1], detail=result[0]["error"])
    return result

@router.post("/", summary="Create a new product")
def create_product(
    name: str,
    unit: str,
    price: float,
    description: str,
    stock: int
):
    result = product_service.create_product(
        name=name,
        unit=unit,
        price=price,
        description=description,
        stock=stock
    )
    if isinstance(result, tuple) and result[1] != 200:
        raise HTTPException(status_code=result[1], detail=result[0]["error"])
    return {"message": "Product created successfully"}

@router.put("/{product_id}", summary="Update an existing product")
def update_product(product_id: int, **kwargs):
    result = product_service.update_product(product_id, **kwargs)
    if isinstance(result, tuple) and result[1] != 200:
        raise HTTPException(status_code=result[1], detail=result[0]["error"])
    return {"message": "Product updated successfully"}

@router.delete("/{product_id}", summary="Delete a product")
def delete_product(product_id: int):
    result = product_service.delete_product(product_id)
    if isinstance(result, tuple) and result[1] != 200:
        raise HTTPException(status_code=result[1], detail=result[0]["error"])
    return {"message": "Product deleted successfully"}
