from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Notification(models.Model):
    user = models.ForeignKey(User, verbose_name="Пользователь", db_index=True, null=False, on_delete=models.CASCADE)
    text = models.CharField(verbose_name="Текст уведомления", max_length=300)
