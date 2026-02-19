import json

from service.todo_service import TodoService


class TodoController:

    def __init__(self, todo_service: TodoService) -> None:
        self._todo_service = todo_service

    def create_todo(self, event: dict) -> dict:
        body = json.loads(event["body"])
        todo = self._todo_service.create_todo(
            title=body["title"],
            description=body.get("description", ""),
        )
        return {"statusCode": 201, "body": todo}

    def get_todo(self, event: dict) -> dict:
        todo_id = event["pathParameters"]["todoId"]
        todo = self._todo_service.get_todo(todo_id)
        return {"statusCode": 200, "body": todo}

    def update_todo(self, event: dict) -> dict:
        todo_id = event["pathParameters"]["todoId"]
        body = json.loads(event["body"])
        todo = self._todo_service.update_todo(
            todo_id=todo_id,
            title=body["title"],
            description=body.get("description", ""),
            completed=body.get("completed", False),
        )
        return {"statusCode": 200, "body": todo}

    def delete_todo(self, event: dict) -> dict:
        todo_id = event["pathParameters"]["todoId"]
        self._todo_service.delete_todo(todo_id)
        return {"statusCode": 204, "body": None}
