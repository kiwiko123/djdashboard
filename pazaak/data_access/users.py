from django.core.exceptions import ObjectDoesNotExist
from pazaak.models import User


def get_by_email(email_address: str) -> User:
    try:
        result = User.objects.get(email_address=email_address)
    except ObjectDoesNotExist:
        result = None

    return result