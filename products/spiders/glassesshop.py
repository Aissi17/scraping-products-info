from scrapy import Spider, Request


class GlassesshopSpider(Spider):
    name = 'glassesshop'
    allowed_domains = ['www.glassesshop.com']
    start_urls = ['https://www.glassesshop.com/bestsellers']

    def parse(self, response):
        products = response.xpath('//div[@id="product-lists"]/div')

        for product in products:
            link = product.xpath(
                './/div[@class="p-title"]/a/@href').extract_first()
            if link:
                yield Request(link, callback=self.parse_product)

        next_page = response.xpath(
            "//ul[@class='pagination']/li[position() = last()]/a/@href").get()
        if next_page:
            yield Request(url=next_page, callback=self.parse)

    def parse_product(self, response):

        title = response.xpath(
            '//h1[@class="product-info-title"]/text()').extract_first().strip()
        subtitle = response.xpath(
            '//h2[@class="product-subtitle"]/text()').extract_first().strip()
        colors = response.xpath(
            '//ul[@class="product-colors"]/li/@title').extract()
        original_price = response.xpath(
            './/span[@class="product-price-original" or @class="product-price-pre"]/text()').extract_first()
        current_price = response.xpath(
            './/span[@class="product-price-cur"]/text()').extract_first()
        product_size_type = response.xpath(
            './/span[@class="product-size-type"]/text()').extract_first().strip()
        product_size = response.xpath(
            './/span[@class="product-size-type"]/following-sibling::span/text()').extract_first()

        # get products details
        product_image = response.xpath(
            './/img[@class="product-banner lazy"]/@data-src').extract_first()

        details = response.xpath(
            './/*[@id="collapseDefaultComputer"]/div[1]/div[1]/div[1]/ul/li')
        product_sku = details[0].xpath('.//text()').extract_first()
        product_frame = details[1].xpath('.//a/text()').extract_first()
        product_shape = details[2].xpath('.//a/text()').extract_first()
        product_weight = details[3].xpath('.//text()').extract_first().strip()
        product_gender = details[4].xpath(
            './/a/text()').extract_first().strip()
        product_material = details[5].xpath('.//a/text()').extract()

        yield {
            "title": title,
            "subtitle": subtitle,
            "colors": colors,
            "original_price": original_price,
            "current_price": current_price,
            "product_size_type": product_size_type,
            "product_size": product_size,
            "product_image": product_image,
            "product_sku": product_sku,
            "product_frame": product_frame,
            "product_shape": product_shape,
            "product_weight": product_weight,
            "product_gender": product_gender,
            "product_material": product_material,
        }
