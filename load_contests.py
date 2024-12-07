from contests.models import Contest
from load_fed import get_json_data

def load_contests(file_name):
    data = get_json_data(file_name)

    for contest in data:
        c = Contest()
        c.name = contest['name']


if __name__ == "__main__":
    load_contests('events.json')