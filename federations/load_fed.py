from fsp.wsgi import application
import json
import datetime
from django.db import transaction
from federations.models import Federation


def get_json_data(file_name):
    with open(file_name, encoding='utf-8') as f:
        data = json.load(f)
    return data

