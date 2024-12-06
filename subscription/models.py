from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class Subscription(models.Model):
    from contests.models import Contest
    user = models.ForeignKey(User, verbose_name="Пользователь", db_index=True, null=False, on_delete=models.CASCADE)
    contest = models.ForeignKey(Contest, verbose_name="Соревнование", db_index=True, null=False, on_delete=models.CASCADE)
