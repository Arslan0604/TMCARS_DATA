# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class RealEstate3Item(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field()
    pass

# def serialize_price(value):
#     cleaned = value.replace("TMT", "").replace(" ", "").strip()
#     return int(cleaned)

class RealThirdItem(scrapy.Item):
    title = scrapy.Field()
    price = scrapy.Field()
    location = scrapy.Field()
    description = scrapy.Field()
    link = scrapy.Field()
    phone = scrapy.Field()
    time_to_paste = scrapy.Field()