from functools import cached_property

from presentation.todo_controller import TodoController
from repository.dynamodb_todo_repository import DynamoDBTodoRepository
from service.todo_service import TodoService


class Container:

    @cached_property
    def _todo_repository(self) -> DynamoDBTodoRepository:
        return DynamoDBTodoRepository()

    @cached_property
    def _todo_service(self) -> TodoService:
        return TodoService(todo_repository=self._todo_repository)

    @cached_property
    def todo_controller(self) -> TodoController:
        return TodoController(todo_service=self._todo_service)


container = Container()
