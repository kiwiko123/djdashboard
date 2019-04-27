from django.db import models

# Create your models here.
class User(models.Model):
    email_address = models.EmailField(unique=True)
    password = models.CharField(max_length=256)
    is_active = models.BooleanField(default=True)