from django.contrib.auth import hashers
from pazaak.models import AuthenticationRecord, User
from pazaak import data_access
from pazaak.enums import AuthenticationContextType
from pazaak.errors import DataError, InvalidCredentialsError


def create_user(email_address: str, password: str, **kwargs) -> User:
    if data_access.users.get_by_email(email_address):
        raise DataError('User with email address "{0}" already exists'.format(email_address))

    hashed_password = hashers.make_password(password)
    if not hashers.is_password_usable(hashed_password):
        raise InvalidCredentialsError('password is invalid')

    user = User(email_address=email_address, password=hashed_password, **kwargs)
    user.save()
    return user


def are_user_credentials_valid(user: User, plaintext_password: str) -> bool:
    return user and hashers.check_password(plaintext_password, user.password)


def authenticate_user(email_address: str, authentication_context_type: AuthenticationContextType) -> None:
    user = data_access.users.get_by_email(email_address, raise_exception_on_fail=True)
    record = AuthenticationRecord(user=user, context_type_id=authentication_context_type.value)
    record.save()


def is_user_logged_in(email_address: str) -> bool:
    user = data_access.users.get_by_email(email_address, raise_exception_on_fail=True)
    most_recent_auth_record = data_access.authentication.get_most_recent_record_for_user(user)
    return most_recent_auth_record and most_recent_auth_record.context_type_id == AuthenticationContextType.LOGIN.value


if __name__ == '__main__':
    pass