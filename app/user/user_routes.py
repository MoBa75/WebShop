from fastapi import APIRouter, HTTPException
from app.user.user_schemas import UserUpdate, UserCreate
from app.user.user_service import UserService
from app.postgres_data_manager import PostgresDataManager

router = APIRouter()
user_service = UserService(PostgresDataManager())

@router.get("/", summary="Get all users")
def get_all_users():
    result = user_service.get_all_users()
    if isinstance(result, tuple):
        raise HTTPException(status_code=result[1], detail=result[0]["error"])
    return result

@router.get("/{user_id}", summary="Get user by ID")
def get_user(user_id: int):
    result = user_service.get_user_by_id(user_id)
    if isinstance(result, tuple):
        raise HTTPException(status_code=result[1], detail=result[0]["error"])
    return result

@router.post("/", summary="Create a new user")
def create_user(user: UserCreate):
    result = user_service.create_user(**user.dict())
    if isinstance(result, tuple) and result[1] != 200:
        raise HTTPException(status_code=result[1], detail=result[0]["error"])
    return {"message": "User created successfully"}

@router.put("/{user_id}", summary="Update a user")
def update_user(user_id: int, update_data: UserUpdate):
    result = user_service.update_user(user_id, **update_data.dict(exclude_unset=True))
    if isinstance(result, tuple) and result[1] != 200:
        raise HTTPException(status_code=result[1], detail=result[0]["error"])
    return result

@router.delete("/{user_id}", summary="Delete a user")
def delete_user(user_id: int):
    result = user_service.delete_user(user_id)
    if isinstance(result, tuple) and result[1] != 200:
        raise HTTPException(status_code=result[1], detail=result[0]["error"])
    return {"message": "User deleted successfully"}
