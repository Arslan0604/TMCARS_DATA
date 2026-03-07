import scrapy
from scrapy_playwright.page import PageMethod

class RealSecondSpider(scrapy.Spider):
    name = "real_second"
    allowed_domains = ["tmcars.info"]
    start_urls = ["https://tmcars.info/others/nedvijimost/prodaja-kvartir-i-domov"]

    def start_requests(self):             # extracting data from the first page 
        offset = 0
        
        urls = f"{self.start_urls[0]}?offset={offset}&max=150&lang=ru"
        
        yield scrapy.Request(
            urls,
            callback=self.parse,
            meta={"offset": offset},
        )                                 # extracting data from the first page

    def parse(self, response):
        reals = response.css('.item-card2-desc')
        
        for real in reals:
            yield {
                'title': real.css('.font-weight-bold::text').get(),
                'description': real.css('.max-lines-p-desc::text').get(),
                'time_to_paste': real.css('.mt-2::text').get(),
                'location': real.css('.ms-3::text').get(),
                'price': real.css('.h5::text').get(),
                'link': real.css('span a').attrib['href'],
            }
            
        # pagination
        offset = response.meta["offset"] + 150
        next_url = f"{self.start_urls[0]}?offset={offset}&max=150&lang=ru"
        
        #stop if no items returned
        if reals:
            yield scrapy.Request(
                next_url,
                callback=self.parse,
                meta={"offset": offset},
            )