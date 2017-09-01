from django.db import models


class User(models.Model):
    class Meta:
        db_table = 'Users'

    username = models.CharField(max_length=20, unique=True, db_index=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    phone = models.CharField(max_length=10)

    def __str__(self) -> str:
        return '{0}(username={1}, first_name={2}, last_name={3}, phone={4})'.format(type(self).__name__, self.username, self.first_name, self.last_name, self.phone)


class Credentials(models.Model):
    class Meta:
        db_table = 'Credentials'

    username = models.ForeignKey(User, on_delete=models.CASCADE, to_field='username')
    password = models.CharField(max_length=64)
    key = models.CharField(max_length=16)
