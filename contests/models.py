from django.db import models
from country.models import City, Country
from notifications.models import Notification
from django.utils.translation import gettext_lazy as _
#from subscription.models import Subscrip
from notifications.NotificationsFuncs import sendNotification

# Create your models here.

class SportType(models.Model):
    name = models.CharField(verbose_name="Вид спорта", max_length=250)

    def __str__(self):
        return self.name


class Discipline(models.Model):
    sport_type = models.ForeignKey(SportType, verbose_name="Вид спорта", db_index=True, null=False, on_delete=models.CASCADE)
    name = models.CharField(verbose_name="Вид спорта", max_length=250)

    def __str__(self):
        return self.name


class ContestType(models.Model):
    name = models.CharField(verbose_name="Уровень соревнования", max_length=250)

    def __str__(self):
        return self.name


class Gender(models.IntegerChoices):
    FEMALE = 0, "Женщина"
    MALE = 1, "Мужчина"


class AgeGroup(models.Model):
    gender = models.IntegerField('Пол', default=Gender.MALE, choices=Gender.choices)
    start = models.IntegerField(verbose_name="Нижний порог")
    end = models.IntegerField(verbose_name="Верхний порог", null=True, blank=True)

    def __str__(self):
        return ("Мужчина" if self.gender == 1 else "Женщина") + ' ' + str(self.start) + '-' + str(self.end)


class Contest(models.Model):
    
    class ContestFormat(models.TextChoices):
        ONL = "ONLINE", _("Онлайн")
        OFL = "OFFLINE", _("Оффлайн")
        ONFL = "ONLINE/OFFLINE", _("Онлайн/Оффлайн")

    class Status(models.TextChoices):
        ACTIVE = "ACTIVE", _("Активный")
        CLOSED = "CLOSED", _("Закрыт")
        CANCLED = "CANCLED", _("Отменен")

    name = models.CharField(verbose_name="Наименование", max_length=300)
    start_time = models.DateTimeField(verbose_name="Дата начала")
    end_time = models.DateTimeField(verbose_name="Дата окончания")
    place = models.ForeignKey(City, verbose_name="Город проведения", db_index=True, null=True, on_delete=models.SET_NULL)
    contest_type = models.ForeignKey(ContestType, verbose_name="Уровень соревнования", db_index=True, null=True, on_delete=models.SET_NULL)
    format = models.CharField("Формат соревнования", max_length=20, default=ContestFormat.ONL, choices=ContestFormat)
    status = models.CharField("Статус", max_length=10, default=Status.ACTIVE, choices=Status)

    def save(self, *args, **kwargs):
        if self.pk is not None:
            # Создание нового объекта
            sendNotification(self)
        super(Contest, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


class ContestDiscipline(models.Model):
    contest = models.ForeignKey(Contest, verbose_name="Cоревнование", db_index=True, null=True, on_delete=models.SET_NULL)
    discipline = models.ForeignKey(Discipline, verbose_name="Дисциплина", db_index=True, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return f'{self.contest} {self.discipline}'

class ContestAgeGroup(models.Model):
    contest = models.ForeignKey(Contest, verbose_name="Cоревнование", db_index=True, null=True, on_delete=models.SET_NULL)
    age_group = models.ForeignKey(AgeGroup, verbose_name="Возрастная группа", db_index=True, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return f'{self.contest} {self.age_group}'