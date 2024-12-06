from django.db import models
from django.contrib.auth.models import User
from country.models import City
from contests.models import Contest
from django.utils.translation import gettext_lazy as _
# Create your models here.


class Claim(models.Model):
    class Status(models.TextChoices):
        
        NEW = "NEW", _("Новый")
        ONPROGRESS = "ONPROGRESS", _("На рассмотрении")
        MODERATE = "MODERATE", _("Отправлен на модерацию")
        REJECTED = "REJECTED", _("Отклонен")
        ACCEPTED = 'ACCEPTED', _("Принят")
        
    name = models.CharField(verbose_name="Название заявки", max_length=250, null=True)
    start_time = models.DateTimeField(verbose_name="Дата начала", null=True)
    end_time =  models.DateTimeField(verbose_name="Дата окончания", null=True)
    place = models.ForeignKey(City, verbose_name="Город", db_index=True, null=True, on_delete=models.SET_NULL)
    format = models.CharField(verbose_name="Формат соревнования", max_length=20, default=Contest.ContestFormat.ONL, choices=Contest.ContestFormat)
    status = models.CharField(verbose_name="Статус", max_length=25, default=Status.NEW, choices=Status)
    
    
class ClaimFile(models.Model):
    claim = models.ForeignKey(Claim, verbose_name="Заявка", on_delete=models.CASCADE)
    file = models.FileField(verbose_name="Файл", upload_to='uploads/')
    description = models.CharField(verbose_name="Описание", max_length=300)
    
    def __str__(self):
        return self.claim.name
