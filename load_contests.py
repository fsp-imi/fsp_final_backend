import datetime
from fsp.wsgi import application
from django.db import transaction
from contests.models import Contest, ContestType, Discipline, SportType, ContestDiscipline, ContestAgeGroup, AgeGroup, Gender
from load_fed import get_json_data

types = ContestType.objects.all()
regional = 1
interregional = 2
allrussia = 2
international = 4
sport_type = SportType.objects.filter(id=1).first()

def load_contests(file_name):
    data = get_json_data(file_name)
    i = 1
    with transaction.atomic():
        for contest in data:
            c = Contest()
            c.name = contest['name']
            if 'date' in contest and contest['date'] is not None and len(contest['date']) > 0:
                c.start_time = datetime.datetime.strptime(contest['date'], "%d.%m.%Y")
            else:
                c.start_time = datetime.datetime.now()
            c.place = contest['location']
            c.format = get_contest_type(contest['name'])
            c.save()
            if 'disciplines' in contest and\
                contest['disciplines'] is not None and\
                len(contest['disciplines']) > 0:
                add_disciplines(c, get_disciplines(contest['disciplines']))
            else:
                add_disciplines(c, Discipline.objects.all())
            
            if 'age_group' in contest and\
                contest['age_group'] is not None and\
                len(contest['age_group']) > 0:
                add_age_groups(c, get_age_groups(contest['age_group']))
            else:
                add_age_groups(c, AgeGroup.objects.all())
            i += 1
    print(i, 'contests loaded')


def get_disciplines(discipline_names):
    result = []
    for discipline in discipline_names:
        d = Discipline.objects.filter(name=discipline).first()
        if d is None:
            d = Discipline()
            d.sport_type = sport_type
            d.name = discipline
            d.save()
        result.append(d)
    return d
            
                
def add_disciplines(contest, disciplines):
    for discipline in disciplines:
        cd = ContestDiscipline()
        cd.contest = contest
        cd.discipline = discipline
        cd.save()


def get_age_groups(ages):
    result = []
    for age in ages:
        age = age.lower()
        if age == 'все':
            result.extend(AgeGroup.objects.all())
        elif age == 'студенты':
            result.extend(AgeGroup.objects.filter(start__gte=17, end__lte=25))
        elif age == 'мужчины':
            result.extend(AgeGroup.objects.filter(start__gte=18, gender=Gender.MALE))
        elif age == 'женщины':
            result.extend(AgeGroup.objects.filter(start__gte=18, gender=Gender.FEMALE))
        else:
            gender, g_age = age.split()
            if '(' in g_age:
                g_age = g_age[1:-1]
                start, end = map(int, g_age.split('-'))
                if gender == 'юниоры':
                    result.extend(AgeGroup.objects.filter(start__gte=start, end__lte=end, gender=Gender.MALE))
                elif gender == 'юниорки':
                    result.extend(AgeGroup.objects.filter(start__gte=start, end__lte=end, gender=Gender.FEMALE))
                else:
                    result.extend(AgeGroup.objects.filter(start__gte=start, end__lte=end))
            else:
                result.extend(AgeGroup.objects.filter(start__gte=start))



def add_age_groups(contest, ages):
    for age in ages:
        ca = ContestAgeGroup()
        ca.contest = contest
        ca.age_group = age
        ca.save()


def get_contest_type(contest_name):
    contest_name = contest_name.lower()
    if 'всерос' in contest_name or\
       'россии' in contest_name:
        return types[allrussia]
    if 'всемир' in contest_name or\
       'междунар' in contest_name or\
       'миров' in contest_name:
        return types[international]
    if 'межрегион' in contest_name or\
       'окруж' in contest_name:
        return types[interregional]
    return types[regional]


if __name__ == "__main__":
    load_contests('events.json')