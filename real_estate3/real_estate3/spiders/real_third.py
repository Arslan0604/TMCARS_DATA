from urllib import response
import scrapy
import re
import json
from real_estate3.items import RealThirdItem
import random

class RealThirdSpider(scrapy.Spider):
    name = "real_third"
    allowed_domains = ["tmcars.info"]
    start_urls = ["https://tmcars.info/others/nedvijimost/prodaja-kvartir-i-domov"]
    
    # s account arslan.dmarketing@gmail.com
    
    # token = "p634rbfnrnb0oq7sin4am575g1vprlvv"
    # devid = "web-ee471187-9287-4287-8485-ac55c7047867"

    # s account aslan.datascience@gmail.com
    
    token = "dh7oqoum9n7j785uvfmrchps81np00ol"  
    devid = "web-c1d1b58b-f86e-4895-a17e-bcdc44593e87" 
    # proxy = "socks5h://sph9pd4cp5:rS49A6z=tieZdm2rIi@gate.decodo.com:7000"

    def start_requests(self):
        offset = 0

        url = f"{self.start_urls[0]}?offset={offset}&max=150&lang=ru"

        
        
        yield scrapy.Request(
            url,
            callback=self.parse,
            meta={"offset": offset}
        )

    # -----------------------------
    # LIST PAGE
    # -----------------------------

    def parse(self, response):
        items = response.css('.item-card2-desc')
        for item in items:
            date_str = item.css('span.pb-0.pt-0.mb-2.mt-2::text').get()
            if date_str:
                date_str = date_str.strip().lower()
                allowed = ["şu wagt"] # mojno dobavit eslit nujno eshe vremya 1 sag on i 2 sag on, esli nujno
                if date_str not in allowed:
                    continue
            else:
                continue
            
            detail_url = response.urljoin(item.css("span a::attr(href)").get())
            meta_data = {
                'title': item.css('.font-weight-bold::text').get(),
                'description': item.css('.max-lines-p-desc::text').get(),
                'time_to_paste': date_str,
                'location': item.css('.ms-3::text').get(),
                'price': item.css('.h5::text').get(),
                'link': item.css('span a').attrib['href'],
            }
            
            
            
            yield scrapy.Request(
                detail_url,
                callback=self.parse_detail,
                meta=meta_data
            )
        # pagination
        offset = response.meta["offset"] + 150

        next_url = f"{self.start_urls[0]}?offset={offset}&max=150&lang=ru"

        if items:
            yield scrapy.Request(
                next_url,
                callback=self.parse,
                meta={"offset": offset}
                
            )
                 
    # -----------------------------
    # DETAIL PAGE
    # -----------------------------

    def parse_detail(self, response):

        # description
        description = response.css("p::text").get()

        # details table
        rows = response.css("tbody tr")

        details = {}

        for row in rows:
            key = row.css("td span::text").get()
            value = row.css("td::text").get()

            if key:
                key = key.replace(" :", "").strip()
                details[key] = value.strip() if value else None

        # product id from url
        product_id = response.url.split("/")[4]



        # -----------------------------
        # PHONE API REQUEST
        # -----------------------------

        
        
        
        headers = {
            "Token": self.token,
            "devId": self.devid,
        }
        phone_api = f"https://tmcars.info/productData/getContacts?productId={product_id}&productType=OTHER"


        yield scrapy.Request(
            phone_api,
            method="GET",
            headers=headers,
            # cookies=self.cookies,
            cb_kwargs={
                "title": response.meta["title"],
                "price": response.meta["price"],
                "location": response.meta["location"],
                "link": response.url,
                "description": description,
                "time_to_paste": response.meta["time_to_paste"]
                # "details": details
            },
            callback=self.parse_phone,
            
            dont_filter=True
        )


    # -----------------------------
    # PHONE API RESPONSE
    # -----------------------------
    def parse_phone(self, response, title, price, location, link, description, time_to_paste): ## zdes ya toje ubral details

       
        try:
            data = json.loads(response.text)
        except:
            data = {}
         

        phone = None

        if data.get("status"):
            contacts = data.get("contacts", {})
            phone = contacts.get("phoneNumber")
            
        if not phone and description:
            m = re.search(r"\+?\d[\d\s\-]{7,}", description)
            if m:
                phone = m.group()

        real_third_item = RealThirdItem()
        
        real_third_item['title'] = title
        real_third_item['price'] = price
        real_third_item['location'] = location
        real_third_item['description'] = description
        real_third_item['link'] = link
        real_third_item['phone'] = phone
        real_third_item['time_to_paste'] = time_to_paste

        yield real_third_item
        # yield {
        #     "title": title,
        #     "price": price,
        #     "location": location,
        #     "description": description,
        #     "link": link,  
        #     "phone": phone,
        #     "time_to_paste": time_to_paste
        #     # "details": details
        # }

## mogu v luboy moment podkluchit details esli nujno
## placed time I need to put somewhere. response.css('span.pb-0.pt-0.mb-2.mt-2::text').get()
## I need to start to do that really fast bro 
## need to proparly filtration urgent Arslan


    


