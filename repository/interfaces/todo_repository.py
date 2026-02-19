from abc import ABC, abstractmethod


class TodoRepository(ABC):

    @abstractmethod
    def find_by_id(self, todo_id: str) -> dict | None:
        raise NotImplementedError

    @abstractmethod
    def save(self, todo: dict) -> dict:
        raise NotImplementedError

    @abstractmethod
    def update(self, todo_id: str, data: dict) -> dict | None:
        raise NotImplementedError

    @abstractmethod
    def delete(self, todo_id: str) -> bool:
        raise NotImplementedError
