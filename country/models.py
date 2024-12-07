from django.db import models

# Create your models here.
from django.db import models


class Country(models.Model):
    name = models.CharField(verbose_name="Наименование", max_length=250)

    def __str__(self):
        return self.name


class District(models.Model):
    name = models.CharField(verbose_name="Наименование", max_length=250)

    def __str__(self):
        return self.name


class Region(models.Model):
    district = models.ForeignKey(District, verbose_name="Федеральный округ", db_index=True, null=True, on_delete=models.CASCADE)
    name = models.CharField(verbose_name="Наименование", max_length=250)
    code = models.CharField(verbose_name="Код", max_length=10, null=True, blank=True, db_index=True)

    def __str__(self):
        return self.name


class City(models.Model):
    region = models.ForeignKey(Region, verbose_name="Населенный пункт", db_index=True, null=True, on_delete=models.CASCADE)
    name = models.CharField(verbose_name="Наименование", max_length=250)

    def __str__(self):
        return self.name