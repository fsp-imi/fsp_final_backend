import requests
from bs4 import BeautifulSoup
import json

def regions_parse(count=None):
    # URL главной страницы
    url = "https://fsp-russia.com"
    path = "region/regions"

    # Получаем HTML-контент страницы
    response = requests.get(f"{url}/{path}")
    soup = BeautifulSoup(response.text, 'html.parser')

    # Список для хранения ссылок на регионы
    region_links_containers = []

    # Найдем все элементы с классом 'cont', обернутые ссылкой
    region_containers = soup.find_all(class_='cont')

    for container in region_containers:
        link = container.find('a', href=True)
        if link:
            region_links_containers.append(link['href'])

    # Удаляем дубликаты ссылок
    region_links_containers = list(set(region_links_containers))
    region_links = [f"{url}{link}" for link in region_links_containers]

    print(f"Найденные ссылки на регионы (всего {len(region_links)}):")
    for link in region_links:
        print(link)

    # Словарь для хранения информации о регионах
    regions = {}

    n = 0  # Счетчик для ограничения количества регионов

    for link in region_links:
        if count and n >= count:
            break

        # Получаем HTML-контент страницы региона
        response = requests.get(link)
        soup = BeautifulSoup(response.text, 'html.parser')

        region = {}

        # Извлечение данных о регионе
        image_container = soup.find(class_='flag')
        image = f"{url}{image_container.find('img')['src']}" if image_container else None

        region_container = soup.find(class_='location')
        region_name = region_container.find('a', href=True).text if region_container else None

        agent_name_container = soup.find(class_='name')
        agent_name = agent_name_container.find('p').text if agent_name_container else None

        contact_container = soup.find(class_='name_phone').find(class_='phone')
        contact = contact_container.find('a').text if contact_container else None

        # Сохраняем данные в словарь
        if image:
            region['image'] = image
        region['agent_name'] = agent_name
        region['contact'] = contact

        regions[region_name] = region
        print(f"Собраны данные для региона: {region_name}")
        n += 1

    # Сохранение данных в JSON
    with open('regions.json', 'w', encoding='utf-8') as json_file:
        json.dump(regions, json_file, ensure_ascii=False, indent=4)

    print("Данные успешно сохранены в regions.json")

