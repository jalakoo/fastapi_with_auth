from abc import ABC, abstractmethod


class BaseAuthModule(ABC):

    @abstractmethod
    async def get_current_user(self, credentials: dict):
        pass

    @abstractmethod
    async def sign_in(self, user_data: dict):
        # Takes an email + password and returns a token if valid
        pass

    @abstractmethod
    async def sign_up(self, user_data: dict) -> bool:
        pass

    @abstractmethod
    async def delete_user(self, user_id: str) -> bool:
        pass

    @abstractmethod
    async def forgot_password(self, email: str) -> bool:
        pass
