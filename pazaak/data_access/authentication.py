from pazaak.models import AuthenticationRecord, User


def get_most_recent_record_for_user(user: User) -> AuthenticationRecord:
    records = AuthenticationRecord.objects.filter(user=user).order_by('-created_time')
    return records[0] if records else None