# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import psycopg2
from itemadapter import ItemAdapter



class RealEstate3Pipeline:
    
    def open_spider(self, spider):
        self.conn = psycopg2.connect(
            host="localhost",
            port=5432,
            database="parser_db",
            user="macbookpro"
        )
        self.cur = self.conn.cursor()
    def close_spider(self, spider):
        self.conn.commit()
        self.cur.close()
        self.conn.close()
        
    def process_item(self, item, spider):
        
        adapter = ItemAdapter(item)
        
        ## Stripping whitespace from all string fields
        field_names = adapter.field_names()
        for field_name in field_names:
            if field_name != "description":
                value = adapter.get(field_name)
                if isinstance(value, str):
                    adapter[field_name] = value.strip()
        
        
        ## Price --> converting to float
        price_keys = ['price']
        for price_key in price_keys:
            value = adapter.get(price_key)
            if isinstance(value, str):
                value = value.replace("TMT", "").strip()
                adapter[price_key] = str(value)
            else:
                adapter[price_key] = None
                
                

        # INSERT INTO DB
        self.cur.execute("""
            INSERT INTO real_estate3 (
                title,
                price,
                location,
                description,
                link,
                phone,
                time_to_paste
            )
            VALUES (%s,%s,%s,%s,%s,%s,%s)
            ON CONFLICT (link) DO NOTHING
        """, (
            adapter.get("title"),
            adapter.get("price"),
            adapter.get("location"),
            adapter.get("description"),
            adapter.get("link"),
            adapter.get("phone"),
            adapter.get("time_to_paste")
        ))

        return item
        
