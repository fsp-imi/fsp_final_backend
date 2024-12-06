from django.db import models
from country.models import City, Country
#from notifications.models import Notification
#from subscription.models import Subscrip
from notifications.NotificationsFuncs import sendNotification

# Create your models here.

class SportType(models.Model):
    name = models.CharField(verbose_name="Вид спорта", max_length=250)
    #code = models.CharField(verbose_name="Вид спорта", max_length=250)

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
    contest = models.ForeignKey('Contest', verbose_name="Cоревнование", db_index=True, null=False, on_delete=models.CASCADE)
    gender = models.IntegerField('Пол', default=Gender.MALE, choices=Gender.choices)
    start = models.IntegerField(verbose_name="Нижний порог")
    end = models.IntegerField(verbose_name="Верхний порог")

    def __str__(self):
        return self.contest.program + ' ' + ("Мужчина" if self.gender == 1 else "Женщина") + ' ' + str(self.start) + '-' + str(self.end)


class Contest(models.Model):
    program = models.CharField(verbose_name="Программа", max_length=250)
    code = models.CharField(verbose_name="Код", max_length=250)
    start = models.DateField(verbose_name="Дата начала")
    end = models.DateField(verbose_name="Дата окончания")
    place = models.ForeignKey(City, verbose_name="Город проведения", db_index=True, null=True, on_delete=models.SET_NULL)
    country = models.ForeignKey(Country, verbose_name="Страна проведения", db_index=True, null=True, on_delete=models.SET_NULL)
    contestants = models.IntegerField(verbose_name="Количество участников")
    contest_type = models.ForeignKey(ContestType, verbose_name="Уровень соревнования", db_index=True, null=True, on_delete=models.SET_NULL)
    male = models.BooleanField("Мужчины")
    female = models.BooleanField("Женщины")

    def save(self, *args, **kwargs):
        if self.pk is not None:
            # Создание нового объекта
            sendNotification(self)
        super(Contest, self).save(*args, **kwargs)

    def __str__(self):
        return self.program


class ContestDiscipline(models.Model):
    contest = models.ForeignKey(Contest, verbose_name="Cоревнование", db_index=True, null=True, on_delete=models.SET_NULL)
    discipline = models.ForeignKey(Discipline, verbose_name="Дисциплина", db_index=True, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return f'{self.contest} {self.discipline}'
