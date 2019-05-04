from django.core.exceptions import ObjectDoesNotExist
from pazaak.models import User


def get_by_email(email_address: str, raise_exception_on_fail=False) -> User:
    try:
        result = User.objects.get(email_address=email_address)
    except ObjectDoesNotExist as e:
        if raise_exception_on_fail:
            message = e.args[0] if e.args else ''
            message = 'User with email address "{0}" does not exist.\n{1}'.format(email_address, message)
            remaining_args = e.args[1:] if e.args else ()
            e.args = (message, *remaining_args)
            raise e
        else:
            result = None

    return result