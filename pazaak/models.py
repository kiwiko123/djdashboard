from django.db import models


# Create your models here.
class AuditableModel(models.Model):
    created_time = models.DateTimeField(auto_now_add=True)
    last_updated_time = models.DateTimeField(auto_now=True)

    def auditable_fields_str(self) -> str:
        date_format = '%m/%d/%Y'
        return 'created_time={0}, last_updated_time={1}'.format(
            self.created_time.strftime(date_format),
            self.last_updated_time.strftime(date_format)
        )

    class Meta:
        abstract = True


class User(AuditableModel):
    email_address = models.EmailField(unique=True)
    password = models.CharField(max_length=256)
    is_active = models.BooleanField(default=True)
    first_name = models.CharField(max_length=64, null=True)
    last_name = models.CharField(max_length=64, null=True)

    def __str__(self) -> str:
        return "User(email_address='{0}', first_name={1}, last_name={3}, is_active={4}, {5})".format(
            self.email_address,
            self.first_name,
            self.last_name,
            self.is_active,
            self.auditable_fields_str()
        )


class AuthenticationRecord(AuditableModel):
    user = models.ForeignKey(User, models.PROTECT)
    context_type_id = models.IntegerField()

    def __str__(self) -> str:
        return "AuthenticationRecord(user='{0}', context_type_id={1}, {2})".format(
            self.user.email_address,
            self.context_type_id,
            self.auditable_fields_str()
        )