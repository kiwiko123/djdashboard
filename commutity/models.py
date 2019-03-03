from django.db import models
from .utilities import tools

class User(models.Model):
    class Meta:
        db_table = 'Users'

    username = models.CharField(max_length=20, unique=True, db_index=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    phone = models.CharField(max_length=10)

    def __str__(self) -> str:
        return tools.generic_obj_str(self, 'username', 'first_name', 'last_name', 'phone')


class Credentials(models.Model):
    class Meta:
        db_table = 'Credentials'

    user = models.ForeignKey(User, on_delete=models.CASCADE, to_field='username')
    password = models.BinaryField(max_length=128)
    key = models.CharField(max_length=16)
    iv = models.BinaryField(max_length=128)
    
    def __str__(self) -> str:
        return '{0}(username={1}, password={2}, key={3}, iv={4})'.format(type(self).__name__, self.user.username, self.password, self.key, self.iv)