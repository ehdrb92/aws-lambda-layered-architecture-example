import pytest

from repository.dynamodb_todo_repository import DynamoDBTodoRepository
from repository.interfaces.todo_repository import TodoRepository


@pytest.fixture
def repository():
    return DynamoDBTodoRepository()


class TestDynamoDBTodoRepository:

    def test_is_instance_of_todo_repository(self, repository):
        assert isinstance(repository, TodoRepository)

    def test_find_by_id_raises_not_implemented(self, repository):
        with pytest.raises(NotImplementedError):
            repository.find_by_id("1")

    def test_save_raises_not_implemented(self, repository):
        with pytest.raises(NotImplementedError):
            repository.save({"todoId": "1", "title": "Buy milk"})

    def test_update_raises_not_implemented(self, repository):
        with pytest.raises(NotImplementedError):
            repository.update("1", {"title": "Buy oat milk"})

    def test_delete_raises_not_implemented(self, repository):
        with pytest.raises(NotImplementedError):
            repository.delete("1")
