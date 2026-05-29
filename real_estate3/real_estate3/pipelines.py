# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class RealEstate3Pipeline:
    def process_item(self, item, spider):
        
        adapter = ItemAdapter(item)
        
        ## Stripping whitespace from all string fields
        field_names = adapter.field_names()
        for field_name in field_names:
            if field_name != "description":
                value = adapter.get(field_name)
                adapter[field_name] = value.strip()
        
        
        ## Price --> converting to float
        price_keys = ['price']
        for price_key in price_keys:
            value = adapter.get(price_key)
            if value is not None:
                # Remove TMT and any whitespace, then convert to float
                cleaned_value = value.replace("TMT", "").replace(" ", "").strip()
                try:
                    adapter[price_key] = float(cleaned_value)
                except ValueError:
                    adapter[price_key] = None

        return item
