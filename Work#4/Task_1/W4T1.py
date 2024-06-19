### Урок 4. Парсинг HTML. XPath
# 1. Выберите веб-сайт с табличными данными, который вас интересует.
# 2. Напишите код Python, использующий библиотеку requests для отправки HTTP GET-запроса на сайт и получения HTML-содержимого страницы.
# 3. Выполните парсинг содержимого HTML с помощью библиотеки lxml, чтобы извлечь данные из таблицы.
# 4. Сохраните извлеченные данные в CSV-файл с помощью модуля csv.

# Ваш код должен включать следующее:
# - Строку агента пользователя в заголовке HTTP-запроса, чтобы имитировать веб-браузер и избежать блокировки сервером.
# - Выражения XPath для выбора элементов данных таблицы и извлечения их содержимого.
# - Обработка ошибок для случаев, когда данные не имеют ожидаемого формата.
# - Комментарии для объяснения цели и логики кода.

# Примечание: Пожалуйста, не забывайте соблюдать этические и юридические нормы при веб-скреппинге.


import requests
from lxml import html
import csv
import pandas as pd

# URL для запроса данных
url = 'https://en.wikipedia.org/wiki/List_of_countries_and_dependencies_and_their_capitals_in_native_languages'

headers={
    'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36'
    }

response = requests.get(url, headers=headers)

response.raise_for_status()
# print(response)

tree = html.fromstring(response.content)

table_rows = tree.xpath("//table[@class='wikitable']/tbody/tr")

data_list =[]

for rows in table_rows:
    data = {}

    data["Country (exonym)"] = rows.xpath(".//td/b/a/text()|.//td/i/a/text()|.//td/i/a/b/text()")
    data["Capital (exonym)"] = rows.xpath(".//td[2]//text()")
    data["Country (endonym)"] = rows.xpath(".//td[3]//text()")
    data["Capital (endonym)"] = rows.xpath(".//td[4]//text()")
    data["Official or native language"] = rows.xpath(".//td[5]//text()")

    data_list.append(data)

df = pd.DataFrame(data_list)
df.to_csv('countries_and_capitals.csv', index=False, encoding='utf-8-sig')
