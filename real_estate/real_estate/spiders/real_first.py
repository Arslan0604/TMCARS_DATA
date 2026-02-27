import scrapy


class RealFirstSpider(scrapy.Spider):
    name = "real_first"
    allowed_domains = ["tmcars.info"]
    start_urls = ["https://tmcars.info/others/nedvijimost/prodaja-kvartir-i-domov"]

    def parse(self, response):
        pass
