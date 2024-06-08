# Выполнить скрейпинг данных в веб-сайта http://books.toscrape.com/ 
# и извлечь информацию о всех книгах на сайте
# во всех категориях: название, цену, количество товара в наличии 
# (In stock (19 available)) в формате integer, описание.

# Затем сохранить эту информацию в JSON-файле.

import requests
from bs4 import BeautifulSoup
import json
import re

url = "http://books.toscrape.com/"

headers = {
    "headers": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"
}

response = requests.get(url, headers=headers)

data_list = []

soup = BeautifulSoup(response.text, features="html.parser") # парсим сайт.
site_elements = soup.find_all("article", class_="product_pod")
# print(link.prettify()) # проверяем нахождения сведений о книге.

for elements in site_elements:
    href_element = elements.h3.a["href"] # ссылку на страницу товара.
    href_response = requests.get('http://books.toscrape.com/' + href_element) # создаём правильный url книги.
    
    url_book = BeautifulSoup(href_response.text, 'html.parser') # парсим страницу книги.
    book_elements = url_book.find_all("article", class_="product_page") # заходим в книгу.

    for book in book_elements:
        title = book.find("div", class_="col-sm-6 product_main").h1.text # получаем название.
        price = float(book.find("p", class_="price_color").text[1:].replace("£", "")) # получаем цену.
        stock_str = book.find("p", class_="instock availability").text.strip() # количество товара в наличии.
        stock = re.search(r"\d+", stock_str) # регулярное выражение для извлечения числа.
        number_str = stock.group() # извлекаем число как строку.
        number_int = int(number_str) # преобразуем строку в число.
        stock_int = re.sub(r"\d+", str(number_int), stock_str) # подменяем строковое число на интовое число.
        description = book.find_all('p')[3].text # получаем описание книги.
        # Добавляем в словарь.
        data_all = {
            'Title': title,
            'Price': price,
            'Stock_int': stock_int,
            'Description': description
        }
        data_list.append(data_all)
        print(data_list)
        
    

