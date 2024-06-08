# Выполнить скрейпинг данных в веб-сайта http://books.toscrape.com/ 
# и извлечь информацию о всех книгах на сайте
# во всех категориях: название, цену, количество товара в наличии 
# (In stock (19 available)) в формате integer, описание.

# Затем сохранить эту информацию в JSON-файле.

import requests
from bs4 import BeautifulSoup
import json

url = "http://books.toscrape.com/"

headers = {
    "headers": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"
}

response = requests.get(url, headers=headers)

soup = BeautifulSoup(response.text, features="html.parser")

data_list = []

for link in soup.find_all("article", class_="product_pod"):
    print(link.prettify()) # проверяем
