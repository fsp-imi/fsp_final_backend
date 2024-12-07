from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from country.models import City

from contests.models import Contest, ContestType, AgeGroup, Discipline
from federations.models import Federation
# Create your models here.

#new to onprogress
#moderate to onprogress

#na rasmot to moderate
#raassmot to otlk


class Claim(models.Model):
    class Status(models.TextChoices):
        
        NEW = "NEW", _("Новый")
        ONPROGRESS = "ONPROGRESS", _("На рассмотрении")
        MODERATE = "MODERATE", _("Отправлен на модерацию")
        REJECTED = "REJECTED", _("Отклонен")
        ACCEPTED = 'ACCEPTED', _("Принят")
        
    name = models.CharField(verbose_name="Название заявки", max_length=300, null=True)
    sender_federation = models.ForeignKey(Federation, related_name="Отправитель",null=True, on_delete=models.CASCADE)
    receiver_federation = models.ForeignKey(Federation, related_name="Приниматель",null=True, on_delete=models.CASCADE)
    start_time = models.DateTimeField(verbose_name="Дата начала", db_index=True, null=True)
    end_time =  models.DateTimeField(verbose_name="Дата окончания", db_index=True, null=True)
    place = models.CharField(verbose_name="Город", blank=True, null=True)
    format = models.CharField(verbose_name="Формат соревнования", max_length=20, db_index=True, default=Contest.ContestFormat.ONL, choices=Contest.ContestFormat)
    status = models.CharField(verbose_name="Статус", max_length=25, db_index=True, default=Status.NEW, choices=Status)
    contest_char = models.CharField("Характер соревнования", max_length=11, db_index=True, default=Contest.ContestCharateristic.PERSONAL, choices=Contest.ContestCharateristic)
    contest_type = models.ForeignKey(ContestType, verbose_name="Уровень соревнования", db_index=True, null=True, on_delete=models.SET_NULL)
    contest_discipline = models.ManyToManyField(Discipline, verbose_name="Дисциплина соревнования")
    contest_age_group = models.ManyToManyField(AgeGroup, verbose_name="Возрастная группа")


class ClaimFile(models.Model):
    claim = models.ForeignKey(Claim, verbose_name="Заявка", on_delete=models.CASCADE)
    file = models.FileField(verbose_name="Файл", upload_to='uploads/')
    description = models.CharField(verbose_name="Описание", max_length=300)
    
    def __str__(self):
        return self.claim.name
