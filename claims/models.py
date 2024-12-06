from datetime import datetime
from django.db import models
from django.contrib.auth.models import User
from ..country.models import City
# Create your models here.

class ClaimFile(models.FileField):
    pass

class Claim(models.Model):
    name = models.CharField(verbose_name="Название заявки", max_length=250)
    start_time = models.DateField(verbose_name="Дата заполнения", max_length=50)
    end_time =  models.DateField(verbose_name="Дата заполнения", max_length=50)
    place = models.ForeignKey(City, verbose_name="Город", db_index=True, null=False, )
    format = 0
    claim_file = models.ForeignKey(ClaimFile, verbose_name="Файл", db_index=True, null=True, on_delete=models.CASCADE)
