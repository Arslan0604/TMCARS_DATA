import scrapy
from scrapy_playwright.page import PageMethod




class RealFirstSpider(scrapy.Spider):
    name = "real_first"
    allowed_domains = ["tmcars.info"]
    start_urls = ["https://tmcars.info/others/nedvijimost/prodaja-kvartir-i-domov"]

    custom_settings = {
        "CLOSESPIDER_ITEMCOUNT": 10
    }

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


# real.css('.h5::text').get() - для получения price из элемента с классом h5
# real.css('.max-lines-p-desc::text').get() - для получения description из элемента с классом max-lines-p-desc
# real.css('.font-weight-bold::text').get() - для получения title из элемента с классом font-weight-bold
# real.css('.mt-2::text').get() - для получения time to paste из элемента с классом mt-2
# real.css('.ms-3::text').get() - для получения location из элемента с классом ms-3
# real.css('span a').attrib['href'] - для получения ссылки из элемента span a