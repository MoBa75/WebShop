from fastapi import APIRouter, HTTPException, Depends
from app.postgres_data_manager import PostgresDataManager
from app.product.product_service import ProductService
from app.product.product_schemas import ProductCreate, ProductUpdate
from app.data_manager_interface import DataManagerInterface

router = APIRouter()

def get_data_manager():
    return PostgresDataManager()

@router.get("/", summary="Get all products")
def get_all_products(data_manager: DataManagerInterface = Depends(get_data_manager)):
    """
    Retrieve all available products.
    """
    product_service = ProductService(data_manager)
    result = product_service.get_all_products()
    if isinstance(result, tuple):
        raise HTTPException(status_code=result[1], detail=result[0]["error"])
    return result

@router.get("/{product_id}", summary="Get product by ID")
def get_product(product_id: int, data_manager: DataManagerInterface = Depends(get_data_manager)):
    """
    Retrieve a specific product by its ID.
    """
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
    """
    Create a new product using validated input data.
    """
    product_service = ProductService(data_manager)
    result = product_service.create_product(**product.model_dump())
    if isinstance(result, tuple) and result[1] != 200:
        raise HTTPException(status_code=result[1], detail=result[0]["error"])
    return {"message": "Product created successfully"}

@router.put("/{product_id}", summary="Update an existing product")
def update_product(
    product_id: int,
    product_data: ProductUpdate,
    data_manager: DataManagerInterface = Depends(get_data_manager)
):
    """
    Update an existing product by ID using partial or full input data.
    """
    product_service = ProductService(data_manager)
    result = product_service.update_product(product_id, **product_data.model_dump(exclude_unset=True))
    if isinstance(result, tuple) and result[1] != 200:
        raise HTTPException(status_code=result[1], detail=result[0]["error"])
    return {"message": "Product updated successfully"}

@router.delete("/{product_id}", summary="Delete a product")
def delete_product(product_id: int, data_manager: DataManagerInterface = Depends(get_data_manager)):
    """
    Delete a product by its ID.
    """
    product_service = ProductService(data_manager)
    result = product_service.delete_product(product_id)
    if isinstance(result, tuple) and result[1] != 200:
        raise HTTPException(status_code=result[1], detail=result[0]["error"])
    return {"message": "Product deleted successfully"}
