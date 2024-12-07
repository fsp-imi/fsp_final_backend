from django.db import models
from country.models import Region
from contests.models import AgeGroup

# Create your models here.

class Contestant(models.Model):
    fio = models.CharField(verbose_name="ФИО", max_length=300)
    age_group = models.ForeignKey(AgeGroup, verbose_name="Возрастная группа", db_index=True, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.fio


class Team(models.Model):
    name = models.CharField(verbose_name="Наименование", max_length=300)
    region = models.ForeignKey(Region, verbose_name="Регион", db_index=True, null=True, on_delete=models.SET_NULL)
    members = models.ManyToManyField(Contestant, verbose_name="Члены команды")

    def __str__(self):
        return self.name