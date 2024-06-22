import scrapy

class AnimeSpider(scrapy.Spider):
    name = "anime"
    allowed_domains = ["animefox.org"]
    start_urls = ["https://animefox.org/anime/"]
    page_count = 1

    # Функция скрапинга
    def parse(self, response):
        for ani in response.xpath('//article[@class="short clearfix with-mask"]'):
            anime_name = ani.xpath('.//div[@class="short-in"]/a/@title').get()
            anime_genre = ani.xpath('.//div[@class="short-cat"]/text()').get()
            anime_rating = ani.xpath('.//div[@class="rate_nums"]/text()').get()
            anime_rating = anime_rating + "/10" if anime_rating else None
            link = ani.xpath('.//div[@class="short-in"]/a[@class="short-title"]//@href').get()
            yield response.follow(url=link, callback=self.anime_parse, meta={
                'anime_name': anime_name,
                'anime_genre': anime_genre,
                'anime_rating': anime_rating
            })
        # Пагинация на следующию страницу
        if self.page_count < 3:
            next_page = response.xpath('//div[@class="pagi-nav clearfix"]/span[@class="pnext"]/a/@href').get()
            if next_page is not None:
                self.page_count += 1
                yield response.follow(next_page, callback=self.parse)
            
    # Функция реквеста скапинга
    def anime_parse(self, response):
        for link_ani in response.xpath('//div[@class="fx-row"]/ul'):
            # Перенос с первой части кода
            name = response.request.meta['anime_name']
            genre = response.request.meta['anime_genre']
            rating = response.request.meta['anime_rating']
            # Парсим таблицу на другой странице
            voiceover = link_ani.xpath('.//li[contains(@class, "vis") and contains(., "Озвучка")]/text()').get()
            date_realese = link_ani.xpath('.//li[contains(@class, "vis") and contains(., "Выход:")]/text()').get()
            episods = link_ani.xpath('.//li[contains(@class, "vis") and contains(., "Эпизоды:")]/text()').get()
            studia = link_ani.xpath('.//li[contains(@class, "vis") and contains(., "Студия:")]/a/text()').get()

            yield {
                'Название аниме' : name,
                'Жанр аниме' : genre,
                'Рейтинг аниме' : rating,
                'Озвучка аниме' : voiceover,
                'Дата выхода' : date_realese,
                'Количество эпизодов' : episods,
                'Студия произодства' : studia
                }

# Запуск и сохранение
# scrapy crawl anime -o anime_list.json