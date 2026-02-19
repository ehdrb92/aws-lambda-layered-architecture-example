import json
from unittest.mock import MagicMock

import pytest

from presentation.todo_controller import TodoController


@pytest.fixture
def mock_service():
    return MagicMock()


@pytest.fixture
def controller(mock_service):
    return TodoController(todo_service=mock_service)


class TestCreateTodo:

    def test_returns_201(self, controller, mock_service):
        mock_service.create_todo.return_value = {"todoId": "1", "title": "Buy milk"}
        event = {"body": json.dumps({"title": "Buy milk", "description": "2 liters"})}

        response = controller.create_todo(event)

        assert response["statusCode"] == 201

    def test_passes_title_and_description_to_service(self, controller, mock_service):
        mock_service.create_todo.return_value = {}
        event = {"body": json.dumps({"title": "Buy milk", "description": "2 liters"})}

        controller.create_todo(event)

        mock_service.create_todo.assert_called_once_with(title="Buy milk", description="2 liters")

    def test_description_defaults_to_empty_string_when_omitted(self, controller, mock_service):
        mock_service.create_todo.return_value = {}
        event = {"body": json.dumps({"title": "Buy milk"})}

        controller.create_todo(event)

        mock_service.create_todo.assert_called_once_with(title="Buy milk", description="")

    def test_body_contains_service_return_value(self, controller, mock_service):
        created = {"todoId": "1", "title": "Buy milk"}
        mock_service.create_todo.return_value = created
        event = {"body": json.dumps({"title": "Buy milk"})}

        response = controller.create_todo(event)

        assert response["body"] == created


class TestGetTodo:

    def test_returns_200(self, controller, mock_service):
        mock_service.get_todo.return_value = {"todoId": "1", "title": "Buy milk"}
        event = {"pathParameters": {"todoId": "1"}}

        response = controller.get_todo(event)

        assert response["statusCode"] == 200

    def test_passes_todo_id_to_service(self, controller, mock_service):
        mock_service.get_todo.return_value = {}
        event = {"pathParameters": {"todoId": "abc-123"}}

        controller.get_todo(event)

        mock_service.get_todo.assert_called_once_with("abc-123")

    def test_body_contains_service_return_value(self, controller, mock_service):
        todo = {"todoId": "1", "title": "Buy milk"}
        mock_service.get_todo.return_value = todo
        event = {"pathParameters": {"todoId": "1"}}

        response = controller.get_todo(event)

        assert response["body"] == todo


class TestUpdateTodo:

    def test_returns_200(self, controller, mock_service):
        mock_service.update_todo.return_value = {"todoId": "1", "title": "Buy oat milk"}
        event = {
            "pathParameters": {"todoId": "1"},
            "body": json.dumps({"title": "Buy oat milk", "description": "", "completed": True}),
        }

        response = controller.update_todo(event)

        assert response["statusCode"] == 200

    def test_passes_all_fields_to_service(self, controller, mock_service):
        mock_service.update_todo.return_value = {}
        event = {
            "pathParameters": {"todoId": "1"},
            "body": json.dumps({"title": "Buy oat milk", "description": "1 liter", "completed": True}),
        }

        controller.update_todo(event)

        mock_service.update_todo.assert_called_once_with(
            todo_id="1",
            title="Buy oat milk",
            description="1 liter",
            completed=True,
        )

    def test_completed_defaults_to_false_when_omitted(self, controller, mock_service):
        mock_service.update_todo.return_value = {}
        event = {
            "pathParameters": {"todoId": "1"},
            "body": json.dumps({"title": "Buy oat milk"}),
        }

        controller.update_todo(event)

        _, kwargs = mock_service.update_todo.call_args
        assert kwargs["completed"] is False


class TestDeleteTodo:

    def test_returns_204(self, controller, mock_service):
        event = {"pathParameters": {"todoId": "1"}}

        response = controller.delete_todo(event)

        assert response["statusCode"] == 204

    def test_body_is_none(self, controller, mock_service):
        event = {"pathParameters": {"todoId": "1"}}

        response = controller.delete_todo(event)

        assert response["body"] is None

    def test_passes_todo_id_to_service(self, controller, mock_service):
        event = {"pathParameters": {"todoId": "abc-123"}}

        controller.delete_todo(event)

        mock_service.delete_todo.assert_called_once_with("abc-123")
