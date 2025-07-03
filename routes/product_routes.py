from fastapi import APIRouter, HTTPException, Depends
from datamanager.postgres_data_manager import PostgresDataManager
from datamanager.product_service import ProductService
from datamanager.schemas import ProductCreate, ProductUpdate
from datamanager.data_manager_interface import DataManagerInterface

router = APIRouter()

def get_data_manager():
    return PostgresDataManager()

@router.get("/", summary="Get all products")
def get_all_products(data_manager: DataManagerInterface = Depends(get_data_manager)):
    product_service = ProductService(data_manager)
    result = product_service.get_all_products()
    if isinstance(result, tuple):
        raise HTTPException(status_code=result[1], detail=result[0]["error"])
    return result

@router.get("/{product_id}", summary="Get product by ID")
def get_product(product_id: int, data_manager: DataManagerInterface = Depends(get_data_manager)):
    product_service = ProductService(data_manager)
    result = product_service.get_product_by_id(product_id)
    if isinstance(result, tuple):
        raise HTTPException(status_code=result[1], detail=result[0]["error"])
    return result

@router.post("/", summary="Create a new product")
def create_product(
    product: ProductCreate,
    data_manager: DataManagerInterface = Depends(get_data_manager)
):
    product_service = ProductService(data_manager)
    result = product_service.create_product(**product.dict())
    if isinstance(result, tuple) and result[1] != 200:
        raise HTTPException(status_code=result[1], detail=result[0]["error"])
    return {"message": "Product created successfully"}

@router.put("/{product_id}", summary="Update an existing product")
def update_product(
    product_id: int,
    product_data: ProductUpdate,
    data_manager: DataManagerInterface = Depends(get_data_manager)
):
    product_service = ProductService(data_manager)
    result = product_service.update_product(product_id, **product_data.dict(exclude_unset=True))
    if isinstance(result, tuple) and result[1] != 200:
        raise HTTPException(status_code=result[1], detail=result[0]["error"])
    return {"message": "Product updated successfully"}

@router.delete("/{product_id}", summary="Delete a product")
def delete_product(product_id: int, data_manager: DataManagerInterface = Depends(get_data_manager)):
    product_service = ProductService(data_manager)
    result = product_service.delete_product(product_id)
    if isinstance(result, tuple) and result[1] != 200:
        raise HTTPException(status_code=result[1], detail=result[0]["error"])
    return {"message": "Product deleted successfully"}
