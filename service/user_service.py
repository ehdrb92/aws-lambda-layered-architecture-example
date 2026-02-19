from repository.interfaces.user_repository import UserRepository


class UserService:

    def __init__(self, user_repository: UserRepository) -> None:
        self._user_repository = user_repository

    def get_user(self, user_id: str) -> dict:
        user = self._user_repository.find_by_id(user_id)
        if user is None:
            raise ValueError(f"User not found: {user_id}")
        return user
