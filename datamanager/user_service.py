from datamanager.models import User
from datamanager.services import user_exists_by_id, user_exists_by_email
from typing import Tuple, Optional, List, Union
from datamanager.data_manager_interface import DataManagerInterface


class UserService:
    """
    Service class for managing users.
    Handles all business logic related to user creation, retrieval, updating, and deletion.
    """

    def __init__(self, data_manager: DataManagerInterface):
        """
        Initializes the UserService with a data manager.

        Args:
            data_manager (DataManagerInterface): The interface used for database operations.
        """
        self.data_manager = data_manager

    def create_user(self, first_name: str, last_name: str, email: str, phone_number: str,
                    address: str, zip_code: int, city: str, is_admin: bool = False,
                    company: Optional[str] = None, birth_date: Optional[str] = None) -> Tuple[dict, int]:
        """
        Creates a new user if the email address is not already taken.

        Args:
            first_name (str): User's first name.
            last_name (str): User's last name.
            email (str): User's email address.
            phone_number (str): User's phone number.
            address (str): Street and house number.
            zip_code (int): Postal code.
            city (str): City of residence.
            is_admin (bool, optional): Whether the user is an admin.
            company (str, optional): Company name, if applicable.
            birth_date (str, optional): Birth date of the user (ISO format: YYYY-MM-DD).

        Returns:
            Tuple[dict, int]: A success or error message with an HTTP status code.
        """
        if user_exists_by_email(self.data_manager.db, email):
            return {"error": "A user with this email already exists."}, 409

        new_user = User(
            first_name=first_name,
            last_name=last_name,
            company=company,
            email=email,
            phone_number=phone_number,
            address=address,
            zip_code=zip_code,
            city=city,
            is_admin=is_admin,
            birth_date=birth_date
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
