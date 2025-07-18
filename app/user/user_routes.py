from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.user.user_schemas import UserUpdate
from app.user.user_service import UserService
from app.auth.auth_utils import get_current_user_data
from app.postgres_data_manager import PostgresDataManager

router = APIRouter()
user_service = UserService(PostgresDataManager())
auth_scheme = HTTPBearer()

@router.post("/register", summary="Create user from Auth0 token")
def register_user(token: HTTPAuthorizationCredentials = Depends(auth_scheme)):
    """
    Register a new user using data from Auth0 access token.
    """
    try:
        user_info_auth = get_current_user_data(token.credentials)
    except Exception as e:
        raise HTTPException(status_code=401, detail=str(e))

    result = user_service.create_user(**user_info_auth)
    if isinstance(result, tuple) and result[1] != 200:
        raise HTTPException(status_code=result[1], detail=result[0]["error"])
    return {"message": "User created successfully"}

@router.get("/", summary="Get all users")
def get_all_users(token: HTTPAuthorizationCredentials = Depends(auth_scheme)):
    """
    Retrieve a list of all users. (Requires valid token)
    """
    user_info_auth = get_current_user_data(token.credentials)  # Validates token
    result = user_service.get_all_users()
    if isinstance(result, tuple):
        raise HTTPException(status_code=result[1], detail=result[0]["error"])
    return result

@router.get("/{user_id}", summary="Get user by ID")
def get_user(user_id: int, token: HTTPAuthorizationCredentials = Depends(auth_scheme)):
    """
    Retrieve a single user by their ID. (Requires valid token)
    """
    user_info_auth = get_current_user_data(token.credentials)
    result = user_service.get_user_by_id(user_id)
    if isinstance(result, tuple):
        raise HTTPException(status_code=result[1], detail=result[0]["error"])
    return result

@router.put("/{user_id}", summary="Update a user")
def update_user(user_id: int, update_data: UserUpdate, token: HTTPAuthorizationCredentials = Depends(auth_scheme)):
    """
    Update an existing user's information. (Requires valid token)
    """
    user_info_auth = get_current_user_data(token.credentials)
    result = user_service.update_user(user_id, **update_data.model_dump(exclude_unset=True))
    if isinstance(result, tuple) and result[1] != 200:
        raise HTTPException(status_code=result[1], detail=result[0]["error"])
    return result

@router.delete("/{user_id}", summary="Delete a user")
def delete_user(user_id: int, token: HTTPAuthorizationCredentials = Depends(auth_scheme)):
    """
    Delete a user by their ID. (Requires valid token)
    """
    user_info_auth = get_current_user_data(token.credentials)
    result = user_service.delete_user(user_id)
    if isinstance(result, tuple) and result[1] != 200:
        raise HTTPException(status_code=result[1], detail=result[0]["error"])
    return {"message": "User deleted successfully"}
