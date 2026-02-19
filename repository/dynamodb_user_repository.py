from repository.interfaces.user_repository import UserRepository


class DynamoDBUserRepository(UserRepository):

    def find_by_id(self, user_id: str) -> dict | None:
        # TODO: implement DynamoDB logic
        raise NotImplementedError
