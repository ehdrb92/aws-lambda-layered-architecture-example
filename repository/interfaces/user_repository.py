from abc import ABC, abstractmethod


class UserRepository(ABC):

    @abstractmethod
    def find_by_id(self, user_id: str) -> dict | None:
        raise NotImplementedError
