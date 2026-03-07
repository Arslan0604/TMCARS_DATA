import scrapy


class RealSecondSpider(scrapy.Spider):
    name = "real_second"
    allowed_domains = ["tmcars.info"]
    start_urls = ["https://tmcars.info/others/nedvijimost/prodaja-kvartir-i-domov"]

    def parse(self, response):
        pass
