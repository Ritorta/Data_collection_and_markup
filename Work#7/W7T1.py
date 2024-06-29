# 1. Выберите веб-сайт, который содержит информацию, представляющую интерес для извлечения данных. 
# Это может быть новостной сайт, платформа для электронной коммерции или любой другой сайт, 
# который позволяет осуществлять скрейпинг (убедитесь в соблюдении условий обслуживания сайта).
# 2. Используя Selenium, напишите сценарий для автоматизации процесса перехода на нужную страницу сайта.
# 3. Определите элементы HTML, содержащие информацию, которую вы хотите извлечь (например, заголовки статей, названия продуктов, цены и т.д.).
# 4. Используйте BeautifulSoup для парсинга содержимого HTML и извлечения нужной информации из идентифицированных элементов.
# 4. Обработайте любые ошибки или исключения, которые могут возникнуть в процессе скрейпинга.
# 5. Протестируйте свой скрипт на различных сценариях, чтобы убедиться, что он точно извлекает нужные данные.
# 6. Предоставьте ваш Python-скрипт вместе с кратким отчетом (не более 1 страницы), который включает следующее: 
# - URL сайта. Укажите URL сайта, который вы выбрали для анализа. 
# - Описание. Предоставьте краткое описание информации, которую вы хотели извлечь из сайта. 
# - Подход. Объясните подход, который вы использовали для навигации по сайту, определения соответствующих элементов и извлечения нужных данных. 
# - Трудности. Опишите все проблемы и препятствия, с которыми вы столкнулись в ходе реализации проекта, и как вы их преодолели. 
# - Результаты. Включите образец извлеченных данных в выбранном вами структурированном формате (например, CSV или JSON). 
# - Примечание: Обязательно соблюдайте условия обслуживания сайта и избегайте чрезмерного скрейпинга, который может нарушить нормальную работу сайта.

from selenium import webdriver # Основной модуль веб-драйвера
from selenium.webdriver.firefox.options import Options # Модуль для браузера используем FIrefox
from selenium.webdriver.support.ui import WebDriverWait # Модуль для ожидания условия
from selenium.webdriver.support import expected_conditions as EC # Модуль набора присетов для WebDriverWait
from selenium.webdriver.common.keys import Keys # Модуль симуляции клавиатуры
from selenium.webdriver.common.by import By # Определение местоположения элементов
from selenium.webdriver.support import expected_conditions as Error # Персональный try exept
import time # Модуль для работы с временем
import re # Модуль для работы с регулярными выражениями
import pandas as pd # Модуль для работы с базами данных

# Модуль работы браузера
options = Options()
options.add_argument('-start-maximized')  # Запуск браузера в полном окне
options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:126.0) Gecko/20100101 Firefox/126.0') # User-Agent
driver = webdriver.Firefox(options=options)  # Драйвер который запускает экземпляр браузера
driver.get('https://www.wildberries.ru/') # открытие вебсайта
time.sleep(4) # Таймер задержки

# Поиск строки поиска и ввод запроса в строку
wait = WebDriverWait(driver, 10) # Ожидание прогрузки страницы
input = wait.until(EC.presence_of_element_located((By.ID, "searchInput"))) # Ищем строку поиска
# Вводим фразу поиска и нажимаем Enter
input.send_keys('процессоры амд 9') # Имитируем ввод запроса в строку поиска
input.send_keys(Keys.ENTER) # Имитируем нажание кнопки ввода

# Модуль создания списка, прокручивания сайта и подсчёта карточек товара, парсинга и перехода на следующию страницу
product_list = [] # Список процессоров
# Прокручиваем сайт до конца
while True:
    count = None # Для подсчёта количества карточек товара
    while True:
        time.sleep(4) # Таймер задержки
        cards = wait.until(EC.presence_of_all_elements_located((By.XPATH, '//article[@id]'))) # Ищем карточку товара
        
        if len(cards) == count: # Выходим из цикла, если при прокрутке страницы, количество товаров не меняется
            break

        count = len(cards) # Посчитываем количество карточек товара на странице
        
        driver.execute_script('window.scrollBy(0, 1800)') # Прокручиваем страницу выполняя JAVA Script
        time.sleep(2) # Таймер задержки
    # Проходимся по карточкам, извлекаем ссылку на товар и добавляем в product_list    
    for card in cards:
        url = card.find_element(By.XPATH, './div/a').get_attribute('href')
        product_list.append(url)

    try: # Доработать проверку на ошибки!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        next = driver.find_element(By.XPATH,  "//a[@class='pagination-next pagination__next j-next-page']") # Ищем кнопку перехода на следующию страницу
        next.click()
    except Exception: 
        break

print(f'Всего получено: {len(product_list)} ссылок на процессоры AMD R9')

# Модуль парсинга данных с страницы товара
driver2 = webdriver.Firefox(options=options)  # Ещё один экземпляр браузера FireFox
wait2 = WebDriverWait(driver2, 10) # Таймер ожидания действий driver2
data_list = [] # Лист данных о процессорах

# Парсинг данных
for url_item in data_list:
    data_parsing = {} # Словарь для парсинга

    driver2.get(url_item) # Переход по страницам
    data_parsing['name'] = wait2.until(EC.presence_of_element_located((By.XPATH, "//h1"))).text # Парсим название процессора

    # Блок парсинга цены, с скидкой, без, старой ценой, новой ценой и тд
    price = wait2.until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'price-block__wallet-price'))) # парсим цену процессора, WB кошелёк распродажа
    try: # Доработать проверку на ошибки!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        data_parsing['price_WB_wallet_sales'] = float(re.sub(r'[^\d.]+', '', price[1].text))
    except Exception:
        data_parsing['price_WB_wallet_sales'] = '-'
    price = wait2.until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'price-block__final-price wallet'))) # парсим цену процессора, WB кошелёк старая цена
    try: # Доработать проверку на ошибки!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        data_parsing['price_WB_wallet_old'] = float(re.sub(r'[^\d.]+', '', price[1].text))
    except Exception:
        data_parsing['price_WB_wallet_old'] = '-'
    price = wait2.until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'price-block__final-price'))) # парсим цену процессора, цена распродажа
    try: # Доработать проверку на ошибки!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        data_parsing['price_sales'] = float(re.sub(r'[^\d.]+', '', price[1].text))
    except Exception:
        data_parsing['price_sales'] = '-'  
    price = wait2.until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'price-block__old-price'))) # парсим цену процессора, старая цена до распродажи
    try: # Доработать проверку на ошибки!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        data_parsing['price_old'] = float(re.sub(r'[^\d.]+', '', price[1].text))
    except Exception:
        data_parsing['price_old'] = '-'

    data_parsing['brend'] = wait2.until(EC.presence_of_element_located((By.CLASS_NAME, "product-page__header-brand"))).text # Парсим бренд процессора
    data_parsing['url'] = url_item # Ссылка на процессор

    button = WebDriverWait(driver2, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, 'product-page__btn-detail')) # Находим клабельный элемент "Все характеристики и описание" чтобы получить открыть таблицу с данными
    )
    button.click() # Имитируем клик на кнопку "Все характеристики и описание"

    # Обрабатываем табличные данные
    table_row_name = wait2.until(EC.presence_of_all_elements_located((By.XPATH, '//div[@class="popup popup-product-details shown"]//th')))
    table_row_param = wait2.until(EC.presence_of_all_elements_located((By.XPATH, '//div[@class="popup popup-product-details shown"]//td')))
    # Заносим данные в зависимости от названия
    for i in range(len(table_row_name)):
        if table_row_name[i].text == 'Процессор':
            try:
                data_parsing['processor'] = table_row_param[i].text
            except Exception:
                data_parsing['processor'] = "-"
        elif table_row_name[i].text == 'Линейка процессоров':
            try:
                data_parsing['family_processor'] = table_row_param[i].text
            except Exception:
                data_parsing['family_processor'] = "-"
        elif table_row_name[i].text == 'Сокет':
            try:
                data_parsing['soked'] = table_row_param[i].text
            except Exception:
                data_parsing['soked'] = "-"
        elif table_row_name[i].text == 'Тактовая частота процессора':
            try:
                val = table_row_param[i].text.strip()
                val, *_ = val.split()
                data_parsing['cpu_clock_speed'] = int(re.sub(r'[^\d.]+', '', val))
                # data_parsing['cpu_clock_speed'] = table_row_param[i].text
            except Exception:
                data_parsing['cpu_clock_speed'] = "-"
        elif table_row_name[i].text == 'Максимальная частота в турбо режиме':
            try:
                val = table_row_param[i].text.strip()
                val, *_ = val.split()
                data_parsing['bost_cpu_clock_speed'] = int(re.sub(r'[^\d.]+', '', val))
                # data_parsing['bost_cpu_clock_speed'] = table_row_param[i].text
            except Exception:
                data_parsing['bost_cpu_clock_speed'] = "-"
        elif table_row_name[i].text == 'Количество ядер процессора':
            try:
                val = table_row_param[i].text.strip()
                val, *_ = val.split()
                data_parsing['processor_cores'] = int(re.sub(r'[^\d.]+', '', val))
                # data_parsing['processor_cores'] = table_row_param[i].text
            except Exception:
                data_parsing['processor_cores'] = "-"
        elif table_row_name[i].text == 'Максимальное число потоков':
            try:
                val = table_row_param[i].text.strip()
                val, *_ = val.split()
                data_parsing['Max_count_threads'] = int(re.sub(r'[^\d.]+', '', val))
                # data_parsing['Max_count_threads'] = table_row_param[i].text
            except Exception:
                data_parsing['Max_count_threads'] = "-"
        elif table_row_name[i].text == 'Техпроцесс':
            try:
                val = table_row_param[i].text.strip()
                val, *_ = val.split()
                data_parsing['technical_process'] = int(re.sub(r'[^\d.]+', '', val))
                # data_parsing['technical_process'] = table_row_param[i].text
            except Exception:
                data_parsing['technical_process'] = "-"
        elif table_row_name[i].text == 'Встроенная графическая система':
            try:
                data_parsing['processor_graphic'] = table_row_param[i].text
            except Exception:
                data_parsing['processor_graphic'] = "-"
        elif table_row_name[i].text == 'Объем кэша L3':
            try: 
                val = table_row_param[i].text.strip()
                val, *_ = val.split()
                data_parsing['l3'] = int(re.sub(r'[^\d.]+', '', val))
            except Exception:
                data_parsing['l3'] = None
        elif table_row_name[i].text == 'Страна производства':
            try: 
                data_parsing['counry'] = table_row_param[i].text
            except Exception:
                data_parsing['counry'] = None

    data_list.append(data_parsing) # Добавляем спарсеные значения в базу

print(f'Обработано {len(data_list)} страниц')

df = pd.DataFrame(data_list)
df.head()