import requests
from bs4 import BeautifulSoup
import json

# URL главной страницы
url = "https://fsp-russia.com"
path = "region/regions"

# Получаем HTML-контент страницы
response = requests.get(f"{url}/{path}")
soup = BeautifulSoup(response.text, 'html.parser')

# Список для хранения ссылок на регионы
region_links_containers = []

# Найдем все элементы с классом 'white_region', обернутые ссылкой
region_containers = soup.find_all(class_='cont')

for container in region_containers:
    link = container.find('a', href=True)
    if link:
      print(link)
      region_links_containers.append(link['href'])

region_links_containers = list(set(region_links_containers))
region_links = []

# Печатаем все ссылки
print("Найденные ссылки на регионы:")
for link in region_links_containers:
    region_links.append(f"{url}{link}")
print(f"Всего регионов: {len(region_links)}")

regions = {}

for link in region_links:
    response = requests.get(link)
    soup = BeautifulSoup(response.text, 'html.parser')

    region = {}

    image = f"{url}{soup.find(class_='flag').find('img')['src']}"

    region_name = soup.find(class_='location').find('a', href=True).text

    agent_name = soup.find(class_='name').find('p').text

    contact = soup.find(class_='phone').find('a').text

    region['image'] = image
    region['agent_name'] = agent_name
    region['contact'] = contact

    print(region)
    regions[f"{region_name}"] = region


# Если нужно сохранить ссылки в JSON
with open('region_links.json', 'w', encoding='utf-8') as json_file:
    json.dump(region_links, json_file, ensure_ascii=False, indent=4)



print("Ссылки успешно сохранены в region_links.json")
