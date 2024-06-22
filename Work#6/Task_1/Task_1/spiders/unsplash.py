import scrapy

# 2. Ваш паук должен уметь перемещаться по категориям фотографий и получать доступ к страницам отдельных фотографий.
# 3. Определите элемент (Item) в Scrapy, который будет представлять изображение. 
# Ваш элемент должен включать такие детали, как URL изображения, название изображения и категорию, к которой оно принадлежит.
# 4. Используйте Scrapy ImagesPipeline для загрузки изображений. 
# Обязательно установите параметр IMAGES_STORE в файле settings.py. 
# Убедитесь, что ваш паук правильно выдает элементы изображений, которые может обработать ImagesPipeline.
# 5. Сохраните дополнительные сведения об изображениях (название, категория) в CSV-файле. 
# Каждая строка должна соответствовать одному изображению и содержать URL изображения, локальный путь к файлу (после загрузки), название и категорию.

class UnsplashSpider(scrapy.Spider):
    name = "unsplash"
    allowed_domains = ["unsplash.com"]
    start_urls = ["https://unsplash.com/"]


    def parse(self, response):
        for image_page in response.xpath('//div[@class="d95fI"]/figure//div/a[@class="Prxeh"]/@href').extract():
            yield scrapy.Request(response.urljoin(image_page), self.parse_image)


    def parse_image(self, response):
        full_image = response.xpath('//img[@itemprop="thumbnailUrl"]/@srcset[contains(., " 2000w")]').extract_first()
        if full_image:
            yield scrapy.Request(response.urljoin(full_image), self.save_image)
    
    def save_image(self, response):
        url_file_name = response.url.split('/')[-1]
        with open(f'images/{url_file_name}', 'wb') as f:
            f.write(response.body)

# //div[@class="d95fI"]//figure//img[@itemprop="thumbnailUrl"]
# //div[@class="d95fI"]//figure//img[@itemprop="thumbnailUrl"]/@srcset
# //img[@itemprop='thumbnailUrl']/@srcset[contains(., ' 200w,')]
# //img[contains(@srcset, "2000w")]/@src
# //img[@itemprop='thumbnailUrl']/@srcset[contains(., ' 1800w,')]
# //img[@itemprop='thumbnailUrl']/@srcset[contains(., ' 2000w')]
