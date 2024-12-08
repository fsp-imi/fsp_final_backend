from django.db import models
from country.models import City, Country
from notifications.models import Notification
from django.utils.translation import gettext_lazy as _
#from subscription.models import Subscrip
from notifications.NotificationsFuncs import sendNotification
from federations.models import Federation

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
        return ("Мужчина" if self.gender == 1 else "Женщина") + ' (от ' + str(self.start) + (' до ' + str(self.end) if self.end is not None else '') + ')'


class Contest(models.Model):

    class ContestCharateristic(models.TextChoices):
        PERSONAL = "Личная", _("Личная")
        TEAM = "Командная", _("Командная")
    
    class ContestFormat(models.TextChoices):
        ONL = "ONLINE", _("Онлайн")
        OFL = "OFFLINE", _("Оффлайн")
        ONFL = "ONLINE/OFFLINE", _("Онлайн/Оффлайн")

    class Status(models.TextChoices):
        ACTIVE = "ACTIVE", _("Активный")
        CLOSED = "CLOSED", _("Закрыт")
        CANCLED = "CANCLED", _("Отменен")

    name = models.CharField(verbose_name="Наименование", max_length=300)
    start_time = models.DateTimeField(verbose_name="Дата начала", db_index=True)
    end_time = models.DateTimeField(verbose_name="Дата окончания", null=True, db_index=True)
    place = models.CharField(verbose_name="Город", max_length=300, blank=True, null=True)
    file = models.FileField(verbose_name="Файл", upload_to='uploads/', null=True)
    contest_char = models.CharField("Характер соревнования", max_length=11, db_index=True, default=ContestCharateristic.PERSONAL, choices=ContestCharateristic)
    contest_type = models.ForeignKey(ContestType, verbose_name="Уровень соревнования", db_index=True, null=True, on_delete=models.SET_NULL)
    format = models.CharField("Формат соревнования", max_length=20, db_index=True, default=ContestFormat.ONL, choices=ContestFormat)
    status = models.CharField("Статус", max_length=10, db_index=True, default=Status.ACTIVE, choices=Status)
    organizer = models.ForeignKey(Federation, verbose_name="Организатор",null=True, on_delete=models.CASCADE, related_name='organizer_set')
    federation = models.ForeignKey(Federation, verbose_name="Федерация",null=True, on_delete=models.CASCADE, related_name='fedration_set')
    file = models.CharField('Ссылка на файл', max_length=300, null=True, blank=True)


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