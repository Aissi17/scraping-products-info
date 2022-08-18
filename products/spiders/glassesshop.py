import scrapy


class GlassesshopSpider(scrapy.Spider):
    name = 'glassesshop'
    allowed_domains = ['www.glassesshop.com']
    start_urls = ['https://www.glassesshop.com/']

    def parse(self, response):
        pass
