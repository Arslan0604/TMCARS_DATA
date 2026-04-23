import scrapy
# this one we should use scrapy-playwright to get phone number and all stuff.

class RealThirdSpider(scrapy.Spider):
    name = "real_third"
    allowed_domains = ["tmcars.info"]
    start_urls = ["https://tmcars.info/others/nedvijimost/prodaja-kvartir-i-domov"]

    def parse(self, response):
        pass
