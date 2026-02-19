from service.user_service import UserService


class UserController:

    def __init__(self, user_service: UserService) -> None:
        self._user_service = user_service

    def get_user(self, event: dict) -> dict:
        user_id = event["pathParameters"]["userId"]
        user = self._user_service.get_user(user_id)
        return {"statusCode": 200, "body": user}
