import scrapy

class AnimeSpider(scrapy.Spider):
    name = "anime"
    allowed_domains = ["animefox.org"]
    start_urls = ["https://animefox.org/anime/"]


    def parse(self, response):
        for restr in response.xpath('//article[@class="short clearfix with-mask"]'):
            name = restr.xpath('.//div[@class="short-in"]/a/@title').get()
            genre = restr.xpath('.//div[@class="short-cat"]/text()').get()
            raiting = restr.xpath('.//div[@class="rate_nums"]/text()').get()
            reyting = raiting + "/10" if raiting else None
            yield {
                "Anime Name" : name,
                "Anime Genre" : genre,
                "Anime Rainting" : reyting
            }
