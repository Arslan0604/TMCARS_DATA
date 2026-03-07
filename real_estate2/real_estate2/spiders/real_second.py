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
            meta={"offset": offset, "playwright": True },
        )                                 # extracting data from the first page

    def parse(self, response):
        reals = response.css('.item-card2-desc')
        
        for real in reals:
            detail_url = response.urljoin(real.css("span a::attr(href)").get())
            meta_data = {
                "title": real.css('.font-weight-bold::text').get(),
                "price": real.css('.h5::text').get(),
            }
            yield scrapy.Request(
                detail_url,
                callback=self.parse_detail,
                meta={
                    "playwright": True,
                    "playwright_page_methods": [
                        PageMethod("click", "button.show-phone"),
                        PageMethod("wait_for_selector", "a[href^='tel']")  # надо найти селектор телефона по поставить здесь
                    ],
                    **meta_data
                }
            )
                
        # pagination
        offset = response.meta["offset"] + 150
        next_url = f"{self.start_urls[0]}?offset={offset}&max=150&lang=ru"
        
        #stop if no items returned
        if reals:
            yield scrapy.Request(
                next_url,
                callback=self.parse,
                meta={"offset": offset, "playwright": True }
            )
            
            
    def parse_detail(self, response):
        phone = response.css("a[href^='tel']::text").get()  # замените на правильный селектор для телефона
        
        rows = response.css("tbody tr")
        
        data = {}
        
        for row in rows:
            key = row.css("span::text").get()
            value = row.css("td::text").get()
            
            if key:
                key = key.replace(" :", "").strip()
                data[key] = value
        
        yield {
           "title": response.meta["title"],
           "price": response.meta["price"],
           "link": response.url,
           "phone": phone,
           "details": data 
            }
                           
                
                
            
        #  response.css(".entry-content-text p::text").get() # selector description
        # response.css("td:has(span.font-weight-bold)::text").get() # selector for category 
        