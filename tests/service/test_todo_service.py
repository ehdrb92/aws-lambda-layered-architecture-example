from unittest.mock import MagicMock, patch

import pytest

from service.todo_service import TodoService


@pytest.fixture
def mock_repository():
    return MagicMock()


@pytest.fixture
def service(mock_repository):
    return TodoService(todo_repository=mock_repository)


class TestCreateTodo:

    def test_returns_repository_save_result(self, service, mock_repository):
        saved = {"todoId": "1", "title": "Buy milk", "completed": False}
        mock_repository.save.return_value = saved

        result = service.create_todo(title="Buy milk", description="2 liters")

        assert result == saved

    def test_saves_todo_with_completed_false(self, service, mock_repository):
        mock_repository.save.return_value = {}

        service.create_todo(title="Buy milk", description="")

        saved_todo = mock_repository.save.call_args[0][0]
        assert saved_todo["completed"] is False

    def test_saves_todo_with_given_title_and_description(self, service, mock_repository):
        mock_repository.save.return_value = {}

        service.create_todo(title="Buy milk", description="2 liters")

        saved_todo = mock_repository.save.call_args[0][0]
        assert saved_todo["title"] == "Buy milk"
        assert saved_todo["description"] == "2 liters"

    def test_saves_todo_with_uuid(self, service, mock_repository):
        mock_repository.save.return_value = {}

        service.create_todo(title="Buy milk", description="")

        saved_todo = mock_repository.save.call_args[0][0]
        assert "todoId" in saved_todo
        assert len(saved_todo["todoId"]) > 0

    def test_saves_todo_with_timestamps(self, service, mock_repository):
        mock_repository.save.return_value = {}

        service.create_todo(title="Buy milk", description="")

        saved_todo = mock_repository.save.call_args[0][0]
        assert "createdAt" in saved_todo
        assert "updatedAt" in saved_todo
        assert saved_todo["createdAt"] == saved_todo["updatedAt"]

    def test_each_call_generates_unique_todo_id(self, service, mock_repository):
        mock_repository.save.return_value = {}

        service.create_todo(title="A", description="")
        first_id = mock_repository.save.call_args[0][0]["todoId"]

        service.create_todo(title="B", description="")
        second_id = mock_repository.save.call_args[0][0]["todoId"]

        assert first_id != second_id


class TestGetTodo:

    def test_returns_todo_when_found(self, service, mock_repository):
        todo = {"todoId": "1", "title": "Buy milk"}
        mock_repository.find_by_id.return_value = todo

        result = service.get_todo("1")

        assert result == todo

    def test_raises_value_error_when_not_found(self, service, mock_repository):
        mock_repository.find_by_id.return_value = None

        with pytest.raises(ValueError, match="Todo not found: not-exist"):
            service.get_todo("not-exist")

    def test_passes_todo_id_to_repository(self, service, mock_repository):
        mock_repository.find_by_id.return_value = {"todoId": "abc"}

        service.get_todo("abc")

        mock_repository.find_by_id.assert_called_once_with("abc")


class TestUpdateTodo:

    def test_returns_updated_todo(self, service, mock_repository):
        existing = {"todoId": "1", "title": "Buy milk"}
        updated = {"todoId": "1", "title": "Buy oat milk", "completed": True}
        mock_repository.find_by_id.return_value = existing
        mock_repository.update.return_value = updated

        result = service.update_todo("1", title="Buy oat milk", description="", completed=True)

        assert result == updated

    def test_raises_value_error_when_todo_not_found(self, service, mock_repository):
        mock_repository.find_by_id.return_value = None

        with pytest.raises(ValueError, match="Todo not found: 1"):
            service.update_todo("1", title="Buy oat milk", description="", completed=False)

    def test_raises_value_error_when_repository_update_returns_none(self, service, mock_repository):
        mock_repository.find_by_id.return_value = {"todoId": "1"}
        mock_repository.update.return_value = None

        with pytest.raises(ValueError, match="Todo not found: 1"):
            service.update_todo("1", title="Buy oat milk", description="", completed=False)

    def test_passes_correct_data_to_repository(self, service, mock_repository):
        mock_repository.find_by_id.return_value = {"todoId": "1"}
        mock_repository.update.return_value = {"todoId": "1"}

        service.update_todo("1", title="Buy oat milk", description="1 liter", completed=True)

        todo_id, data = mock_repository.update.call_args[0]
        assert todo_id == "1"
        assert data["title"] == "Buy oat milk"
        assert data["description"] == "1 liter"
        assert data["completed"] is True
        assert "updatedAt" in data


class TestDeleteTodo:

    def test_succeeds_when_todo_exists(self, service, mock_repository):
        mock_repository.find_by_id.return_value = {"todoId": "1"}
        mock_repository.delete.return_value = True

        service.delete_todo("1")  # 예외 없이 통과

    def test_raises_value_error_when_todo_not_found(self, service, mock_repository):
        mock_repository.find_by_id.return_value = None

        with pytest.raises(ValueError, match="Todo not found: 1"):
            service.delete_todo("1")

    def test_raises_value_error_when_repository_delete_returns_false(self, service, mock_repository):
        mock_repository.find_by_id.return_value = {"todoId": "1"}
        mock_repository.delete.return_value = False

        with pytest.raises(ValueError, match="Todo not found: 1"):
            service.delete_todo("1")

    def test_passes_todo_id_to_repository(self, service, mock_repository):
        mock_repository.find_by_id.return_value = {"todoId": "abc"}
        mock_repository.delete.return_value = True

        service.delete_todo("abc")

        mock_repository.delete.assert_called_once_with("abc")
