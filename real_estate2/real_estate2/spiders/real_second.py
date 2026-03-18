import scrapy
import re


class RealSecondSpider(scrapy.Spider):
    name = "real_second"
    allowed_domains = ["tmcars.info"]
    start_urls = ["https://tmcars.info/others/nedvijimost/prodaja-kvartir-i-domov"]

    token = "dsotqunvo9htc4t6rq6j8k38mu8h8cal"
    devid = "web-9e29cc45-be0f-41c1-add3-601807aeb30a"

    cookies = {
        "SESSION": "_ym_uid=1750511050905819409; _ym_d=1773135408; currentUsername=arslan.datascience%40gmail.com; token=dsotqunvo9htc4t6rq6j8k38mu8h8cal; _gid=GA1.2.1901953467.1773744358; JSESSIONID=CDBD49617D437869EE6F3114B5FAA444; devId=web-9e29cc45-be0f-41c1-add3-601807aeb30a; _ym_isad=2; _ga_4MHT9PVHPE=GS2.1.s1773822607$o41$g1$t1773825722$j27$l0$h0; _ga_NJWV91RXNX=GS2.1.s1773822606$o42$g1$t1773825722$j27$l0$h0; _ga=GA1.1.132075739.1773135408"
    }

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
            detail_url = response.urljoin(item.css("span a::attr(href)").get())
            meta_data = {
                'title': item.css('.font-weight-bold::text').get(),
                'description': item.css('.max-lines-p-desc::text').get(),
                'time_to_paste': item.css('.mt-2::text').get(),
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

        phone_api = "https://tmcars.info/productData/getContacts"

        headers = {
            "Token": self.token,
            "devId": self.devid
        }
        phone_api = f"https://tmcars.info/productData/getContacts?productId={product_id}&productType=OTHER"


        yield scrapy.Request(
            phone_api,
            method="GET",
            headers=headers,
            cookies=self.cookies,
            cb_kwargs={
                "title": response.meta["title"],
                "price": response.meta["price"],
                "location": response.meta["location"],
                "link": response.url,
                "description": description,
                "details": details
            },
            callback=self.parse_phone,
            dont_filter=True
        )


    # -----------------------------
    # PHONE API RESPONSE
    # -----------------------------
    def parse_phone(self, response, title, price, location, link, description, details):

        data = response.json()
        print("RAW API RESPONSE:", data) # eto vremmeno 

        phone = None

        if data.get("status"):
            phone = data.get("contacts", {}).get("phoneNumber")

        yield {
            "title": title,
            "price": price,
            "location": location,
            "description": description,
            "link": link,
            "phone": phone,
            "details": details
        }





    

