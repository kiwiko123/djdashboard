from django.contrib.auth import hashers
from pazaak.models import User
from pazaak import data_access
from pazaak.errors import DataError, InvalidCredentialsError


def create_user(email_address: str, password: str) -> User:
    if data_access.users.get_by_email(email_address):
        raise DataError('User with email address "{0}" already exists'.format(email_address))

    hashed_password = hashers.make_password(password)
    if not hashers.is_password_usable(hashed_password):
        raise InvalidCredentialsError('password is invalid')

    user = User(email_address=email_address, password=hashed_password)
    user.save()
    return user


def are_user_credentials_valid(email_address: str, password: str) -> bool:
    user = data_access.users.get_by_email(email_address)
    return user and hashers.check_password(password, user.password)