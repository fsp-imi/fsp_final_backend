from datetime import datetime, timedelta
import requests
from bs4 import BeautifulSoup
import json

def events_parse(start_month=10, start_year=2024, end_month=11, end_year=2024):
    url = "https://fsp-russia.com"
    path = "calendar"

    start_date = datetime(start_year, start_month, 1)
    end_date = datetime(end_year, end_month, 1)

    events = []
    # Создаем последовательность месяцев
    current_date = start_date
    while current_date <= end_date:
        year = current_date.year
        month = current_date.month
        
        print(f"year: {year}, month: {month}")

        # Здесь можно отправлять запросы к сайту, например:
        response = requests.get(f"{url}/{path}", params={'month': month, 'year': year})
        # Парсим страницу, если нужно
        soup = BeautifulSoup(response.text, 'html.parser')
        # Добавьте логику обработки soup
        calendar_items = soup.find_all(class_='calendar-table__item')

        for item in calendar_items:
          event_data = item.find(class_='event-item-hover')
          if event_data:
            event = {}
            # Извлечение имени
            name = event_data.find(class_='name').find('p').text if event_data.find(class_='name') else None

            # Извлечение даты
            date = event_data.find(class_='date').find('p').text if event_data.find(class_='date') else None

            # Извлечение формата (с проверкой на наличие)
            format_element = event_data.find(class_='online')
            format = format_element.find('p').text if format_element else None

            # Извлечение локации
            location = event_data.find(class_='location').find('p').text if event_data.find(class_='location') else None

            # Извлечение дисциплин
            disciplines_element = event_data.find_all(class_='dis')
            if disciplines_element:
                disciplines = [dis.find(class_='info').find('p').text for dis in disciplines_element if dis.find(class_='info') and dis.find(class_='name').find('p').text == 'Дисциплина']
                age_group = [dis.find(class_='info').find('p').text for dis in disciplines_element if dis.find(class_='info') and dis.find(class_='name').find('p').text == 'Участники']
            else:
                disciplines = None
                age_group = None

            event['name'] = name
            event['date'] = date
            event['format'] = format
            event['location'] = location
            event['disciplines'] = disciplines
            event['age_group'] = age_group
            events.append(event)

        # Переходим к следующему месяцу
        if month == 12:
            current_date = datetime(year + 1, 1, 1)
        else:
            current_date = datetime(year, month + 1, 1)

    # Если нужно сохранить ссылки в JSON
    with open('events.json', 'w', encoding='utf-8') as json_file:
        json.dump(events, json_file, ensure_ascii=False, indent=4)

    print("Данные успешно сохранены в events.json")

