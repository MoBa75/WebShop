from app.models import User
from typing import Tuple, Optional, List, Union
from app.data_manager_interface import DataManagerInterface
from sqlalchemy.orm import Session

def user_exists_by_id(db: Session, user_id: int) -> bool:
    """
    Checks whether a user with the given ID exists in the database.

    Args:
        db (Session): The active SQLAlchemy database session.
        user_id (int): The ID of the user to check.

    Returns:
        bool: True if the user exists, False otherwise.
    """
    return db.query(User).filter(User.id == user_id).first() is not None

def user_exists_by_email(db: Session, email: str) -> bool:
    """
    Checks whether a user with the given email address exists in the database.

    Args:
        db (Session): The active SQLAlchemy database session.
        email (str): The email address of the user to check.

    Returns:
        bool: True if a user with the given email exists, False otherwise.
    """
    return db.query(User).filter(User.email == email).first() is not None

class UserService:
    """
    Service class for managing users.
    Handles creation, retrieval, updating, and deletion of users.
    """

    def __init__(self, data_manager: DataManagerInterface):
        """
        Initializes the UserService with a data manager.

        Args:
            data_manager (DataManagerInterface): The interface used for database operations.
        """
        self.data_manager = data_manager

    def create_user(self, sub: str, email: str, first_name: Optional[str] = None,
                    last_name: Optional[str] = None, company: Optional[str] = None,
                    birth_date: Optional[str] = None, is_admin: bool = False) -> Tuple[dict, int]:
        """
        Creates a new user record based on Auth0 information.

        Args:
            sub (str): Auth0 unique user identifier.
            email (str): User email.
            first_name (str, optional): User's first name.
            last_name (str, optional): User's last name.
            company (str, optional): User's company.
            birth_date (str, optional): User's birth date.
            is_admin (bool): Whether user has admin privileges.

        Returns:
            Tuple[dict, int]: A success or error message with an HTTP status code.
        """
        if user_exists_by_email(self.data_manager.db, email):
            return {"error": "A user with this email already exists."}, 409

        new_user = User(
            email=email,
            first_name=first_name,
            last_name=last_name,
            company=company,
            birth_date=birth_date,
            is_admin=is_admin
        )
        return self.data_manager.add_element(new_user)

    def get_user_by_id(self, user_id: int) -> Union[User, Tuple[dict, int]]:
        """
        Retrieves a user by their ID.

        Args:
            user_id (int): The ID of the user.

        Returns:
            Union[User, Tuple[dict, int]]: The user object or an error message with status code.
        """
        user = self.data_manager.get_by_id(User, user_id)
        if not user:
            return {"error": "User not found"}, 404
        return user

    def get_all_users(self) -> Union[List[User], Tuple[dict, int]]:
        """
        Retrieves all users.

        Returns:
            Union[List[User], Tuple[dict, int]]: A list of users or an error message with status code.
        """
        return self.data_manager.get_all(User)

    def update_user(self, user_id: int, **kwargs) -> Tuple[Union[str, dict], int]:
        """
        Updates user attributes by ID.

        Args:
            user_id (int): The ID of the user to update.
            **kwargs: Dictionary of attributes to update.

        Returns:
            Tuple[Union[str, dict], int]: A success or error message with status code.
        """
        if not user_exists_by_id(self.data_manager.db, user_id):
            return {"error": "User not found."}, 404

        user = self.data_manager.get_by_id(User, user_id)
        for key, value in kwargs.items():
            if hasattr(user, key) and value is not None:
                setattr(user, key, value)

        result, status = self.data_manager.commit_only()
        if status != 200:
            return result, status

        return {"message": "User updated successfully"}, 200

    def delete_user(self, user_id: int) -> Tuple[Union[str, dict], int]:
        """
        Deletes a user by ID.

        Args:
            user_id (int): The ID of the user to delete.

        Returns:
            Tuple[Union[str, dict], int]: A success or error message with status code.
        """
        if not user_exists_by_id(self.data_manager.db, user_id):
            return {"error": "User not found."}, 404

        user = self.data_manager.get_by_id(User, user_id)
        return self.data_manager.delete_element(user)
