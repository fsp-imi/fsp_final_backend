from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from country.models import City

from contests.models import Contest, ContestType, AgeGroup, Discipline, ContestDiscipline, ContestAgeGroup
from federations.models import Federation
from notifications.NotificationsFuncs import sendClaimNotification
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
    place = models.CharField(verbose_name="Город", max_length=300, blank=True, null=True)
    format = models.CharField(verbose_name="Формат соревнования", max_length=20, db_index=True, default=Contest.ContestFormat.ONL, choices=Contest.ContestFormat)
    status = models.CharField(verbose_name="Статус", max_length=25, db_index=True, default=Status.NEW, choices=Status)
    contest_char = models.CharField("Характер соревнования", max_length=11, db_index=True, default=Contest.ContestCharateristic.PERSONAL, choices=Contest.ContestCharateristic)
    contest_type = models.ForeignKey(ContestType, verbose_name="Уровень соревнования", db_index=True, null=True, on_delete=models.SET_NULL)
    contest_discipline = models.ManyToManyField(Discipline, verbose_name="Дисциплина соревнования")
    contest_age_group = models.ManyToManyField(AgeGroup, verbose_name="Возрастная группа")

    def save(self, *args, **kwargs):
        if self.status == self.Status.ACCEPTED:
            #create contest
            c = Contest()
            c.name = self.name
            c.organizer = self.sender_federation
            c.federation = self.receiver_federation
            c.start_time = self.start_time
            c.end_time = self.end_time
            c.place = self.place
            c.format = self.format
            c.contest_char = self.contest_char
            c.contest_type = c.contest_type
            c.save()
            for d in self.contest_discipline.all():
                cd = ContestDiscipline(contest=c, discipline=d)
                cd.save()
            for ag in self.contest_age_group.all():
                ca = ContestAgeGroup(contest=c, age_group=ag)
                ca.save()
            sendClaimNotification(self, f'Поздравляем! Ваша заявление \"{self.name}\" принята!', self.sender_federation.agent)
        elif self.status == self.Status.REJECTED:
            sendClaimNotification(self, f'К сожалению Ваша заявление \"{self.name}\" отклонена!', self.sender_federation.agent)
        elif self.status == self.Status.MODERATE:
            sendClaimNotification(self, f'Обратите внимание! Ваша заявление \"{self.name}\" отправлена на доработку!', self.sender_federation.agent)
        elif self.status == self.Status.NEW:
            sendClaimNotification(self, f'Обратите внимание! Ваша заявление поступило новое заявление!', User.objects.filter(is_staff=True).first())
        
        super(Claim, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


class ClaimFile(models.Model):
    claim = models.ForeignKey(Claim, verbose_name="Заявка", on_delete=models.CASCADE)
    file = models.FileField(verbose_name="Файл", upload_to='uploads/')
    description = models.CharField(verbose_name="Описание", max_length=300)
    
    def __str__(self):
        return self.claim.name
