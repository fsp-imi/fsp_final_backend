from django.db import models
from contests.models import Contest
from contestant.models import Team

# Create your models here.

class Result(models.Model):
    contest = models.ForeignKey(Contest, verbose_name="Соревнование", db_index=True, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, verbose_name="Участник", db_index=True, on_delete=models.CASCADE)
    score = models.IntegerField("Очки")
    
    def __str__(self):
        return self.contest.name + ' ' + self.team.name + ' ' + str(self.score)

class ResultFile(models.Model):
    contest = models.ForeignKey(Contest, verbose_name="Соревнование", db_index=True, on_delete=models.CASCADE)
    file = models.CharField('Ссылка на файл', max_length=300, null=True, blank=True)
    results_protocol = models.BooleanField('Содержит результаты')