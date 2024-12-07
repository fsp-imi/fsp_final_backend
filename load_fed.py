import json
import datetime
from fsp.wsgi import application
from django.db import transaction
from django.contrib.auth.models import User
from federations.models import Federation
from country.models import Region


def get_json_data(file_name):
    with open(file_name, encoding='utf-8') as f:
        data = json.load(f)
    return data

def upload_regions(file_name):
    data = get_json_data(file_name)

    with transaction.atomic():
        i = 1
        for region_name, value in data.items():
            region = Region.objects.filter(name=region_name).first()
            if region is None:
                region = Region(name=region_name)
                region.save()
            
            u = None
            if len(data[region_name]['agent_name']) > 0:
                u = User()
                u.username = 'user' + str(i)
                u.first_name = data[region_name]['agent_name']
                u.email = data[region_name]['contact']
                u.set_password('123456')
                u.save()
            
            f = Federation()
            f.name = "ФСП" + ''.join([x[0] for x in region_name.split()])
            f.region = region
            f.email = data[region_name]['contact']
            f.logo = data[region_name]['image']
            f.agent = u
            f.save()
            i += 1
        print('loaded', i, 'federations')

if __name__ == '__main__':
    upload_regions('./regions.json')