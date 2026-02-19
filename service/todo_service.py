import uuid
from datetime import datetime, timezone

from repository.interfaces.todo_repository import TodoRepository


class TodoService:

    def __init__(self, todo_repository: TodoRepository) -> None:
        self._todo_repository = todo_repository

    def create_todo(self, title: str, description: str) -> dict:
        now = datetime.now(timezone.utc).isoformat()
        todo = {
            "todoId": str(uuid.uuid4()),
            "title": title,
            "description": description,
            "completed": False,
            "createdAt": now,
            "updatedAt": now,
        }
        return self._todo_repository.save(todo)

    def get_todo(self, todo_id: str) -> dict:
        todo = self._todo_repository.find_by_id(todo_id)
        if todo is None:
            raise ValueError(f"Todo not found: {todo_id}")
        return todo

    def update_todo(self, todo_id: str, title: str, description: str, completed: bool) -> dict:
        self.get_todo(todo_id)  # 존재 여부 확인
        data = {
            "title": title,
            "description": description,
            "completed": completed,
            "updatedAt": datetime.now(timezone.utc).isoformat(),
        }
        updated = self._todo_repository.update(todo_id, data)
        if updated is None:
            raise ValueError(f"Todo not found: {todo_id}")
        return updated

    def delete_todo(self, todo_id: str) -> None:
        self.get_todo(todo_id)  # 존재 여부 확인
        deleted = self._todo_repository.delete(todo_id)
        if not deleted:
            raise ValueError(f"Todo not found: {todo_id}")
