from pazaak.models import User
from pazaak.utilities.serialize import Serializable


class UserDTO(Serializable):

    def __init__(self, user: User):
        self._email_address = user.email_address
        self._is_active = user.is_active

    def context(self) -> dict:
        return {
            'emailAddress': self._email_address,
            'isActive': self._is_active
        }