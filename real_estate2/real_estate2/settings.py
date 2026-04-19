# # Scrapy settings for real_estate2 project
# #
# # For simplicity, this file contains only settings considered important or
# # commonly used. You can find more settings consulting the documentation:
# #
# #     https://docs.scrapy.org/en/latest/topics/settings.html
# #     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
# #     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = "real_estate2"

SPIDER_MODULES = ["real_estate2.spiders"]
NEWSPIDER_MODULE = "real_estate2.spiders"

ADDONS = {}
# # Playwright settings
# DOWNLOAD_HANDLERS = {
#     "http": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
#     "https": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
# }

# TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"

# PLAYWRIGHT_BROWSER_TYPE = "chromium"

# # Playwright settings


# # Crawl responsibly by identifying yourself (and your website) on the user-agent
# #USER_AGENT = "real_estate2 (+http://www.yourdomain.com)"

# # Obey robots.txt rules
ROBOTSTXT_OBEY = True
CLOSESPIDER_ITEMCOUNT = 10 # vremmenno, dlya testov. Udalit posle
# # Concurrency and throttling settings
CONCURRENT_REQUESTS = 2
CONCURRENT_REQUESTS_PER_DOMAIN = 3
DOWNLOAD_DELAY = 4
USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/147.0.0.0 Safari/537.36"
RANDOMIZE_DOWNLOAD_DELAY = True
FEED_EXPORT_ENCODING = "utf-8"
# # Disable cookies (enabled by default)
# #COOKIES_ENABLED = False

# # Disable Telnet Console (enabled by default)
# #TELNETCONSOLE_ENABLED = False

# # Override the default request headers:
# #DEFAULT_REQUEST_HEADERS = {
# #    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
# #    "Accept-Language": "en",
# #}

# # Enable or disable spider middlewares
# # See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
# #SPIDER_MIDDLEWARES = {
# #    "real_estate2.middlewares.RealEstate2SpiderMiddleware": 543,
# #}

# # Enable or disable downloader middlewares
# # See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
    "real_estate2.middlewares.RealEstate2DownloaderMiddleware": 543,
}

# # Enable or disable extensions
# # See https://docs.scrapy.org/en/latest/topics/extensions.html
# #EXTENSIONS = {
# #    "scrapy.extensions.telnet.TelnetConsole": None,
# #}

# # Configure item pipelines
# # See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
   "real_estate2.pipelines.RealEstate2Pipeline": 300,
}

# # Enable and configure the AutoThrottle extension (disabled by default)
# # See https://docs.scrapy.org/en/latest/topics/autothrottle.html
AUTOTHROTTLE_ENABLED = True
# # The initial download delay
AUTOTHROTTLE_START_DELAY = 3
# # The maximum download delay to be set in case of high latencies
AUTOTHROTTLE_MAX_DELAY = 30
# # The average number of requests Scrapy should be sending in parallel to
# # each remote server
# #AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# # Enable showing throttling stats for every response received:
# #AUTOTHROTTLE_DEBUG = False

# # Enable and configure HTTP caching (disabled by default)
# # See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
# #HTTPCACHE_ENABLED = True
# #HTTPCACHE_EXPIRATION_SECS = 0
# #HTTPCACHE_DIR = "httpcache"
# #HTTPCACHE_IGNORE_HTTP_CODES = []
# #HTTPCACHE_STORAGE = "scrapy.extensions.httpcache.FilesystemCacheStorage"

# # Set settings whose default value is deprecated to a future-proof value

# PLAYWRIGHT_LAUNCH_OPTIONS = {
#     "headless": False,
#     "args": [
#         # "--no-sandbox",
#         # "--disable-dev-shm-usage",
#         # "--disable-gpu",
#     ],
# }

# PLAYWRIGHT_DEFAULT_NAVIGATION_TIMEOUT = 120000
# PLAYWRIGHT_DEFAULT_CONTEXT_OPTIONS = {
#     "viewport": {"width": 1280, "height": 720},
#     "ignore_https_errors": True,
# }

# PLAYWRIGHT_ABORT_REQUEST = lambda request: request.resource_type in [
#     "image",
#     "media",
#     "font",
#     "stylesheet"
# ]

# PLAYWRIGHT_MAX_CONTEXTS = 4
# PLAYWRIGHT_MAX_PAGES_PER_CONTEXT = 2

# USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120 Safari/537.36"

# PLAYWRIGHT_DEBUG = True
# LOG_LEVEL = "INFO"



