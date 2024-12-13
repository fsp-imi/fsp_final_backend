import datetime
import random
from fsp.wsgi import application
from django.db import transaction
from contests.models import Contest, ContestType, Discipline, SportType, ContestDiscipline, ContestAgeGroup, AgeGroup, Gender
from federations.models import Federation
from load_fed import get_json_data

def set_date(contest):
    if contest.end_time is None:
        contest.end_time = contest.start_time + datetime.timedelta(days=5)

def set_orgs(contest, federations):
    if contest.organizer is None:
        f = random.choice(federations)
        contest.organizer = f


def fix_contests_data(contests):
    federations = Federation.objects.all()
    for contest in contests:
        set_date(contest)
        set_orgs(contest, federations)
        contest.save()


if __name__ == '__main__':
    contests = Contest.objects.all()
    fix_contests_data(contests)
