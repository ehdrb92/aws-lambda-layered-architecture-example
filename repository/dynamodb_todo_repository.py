from repository.interfaces.todo_repository import TodoRepository


class DynamoDBTodoRepository(TodoRepository):

    def find_by_id(self, todo_id: str) -> dict | None:
        # TODO: implement DynamoDB logic
        raise NotImplementedError

    def save(self, todo: dict) -> dict:
        # TODO: implement DynamoDB logic
        raise NotImplementedError

    def update(self, todo_id: str, data: dict) -> dict | None:
        # TODO: implement DynamoDB logic
        raise NotImplementedError

    def delete(self, todo_id: str) -> bool:
        # TODO: implement DynamoDB logic
        raise NotImplementedError
