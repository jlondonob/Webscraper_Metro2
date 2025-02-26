# Scrapy settings for scrapySpider project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'scrapySpider'

SPIDER_MODULES = ['scrapySpider.spiders']
NEWSPIDER_MODULE = 'scrapySpider.spiders'

FEED_EXPORT_ENCODING = 'utf-8'

# Export order
FEED_EXPORT_FIELDS = ['source',
                      'propID',
                      'propType',
                      'businessType',
                      'salePrice',
                      'rentPrice',
                      'rentTotalPrice',
                      'areaBuilt',
                      'rooms',
                      'bathrooms',
                      'garages',
                      'stratum',
                      'cityID',
                      'cityName',
                      'zoneID',
                      'zoneName',
                      'neighborhood',
                      'commonNeighborhood',
                      'propAddress',
                      'floor',
                      'adminPrice',
                      'comment',
                      'numPictures',
                      'companyId',
                      'companyName',
                      'propertyState',
                      'builtTime',
                      'latitude',
                      'longitude',
                      'hasBalcony',
                      'hasChimney',
                      'hasServiceRoom',
                      'hasStorageSpace',
                      'hasInterphone',
                      'hasAirConditioner',
                      'extColsedComplex',
                      'extVigilance',
                      'extGreenZones',
                      'extCoveredGarage',
                      'publishedSectorAmenities',
                      'amenitiesInteriors',
                      'amenitiesExteriors',
                      'amenitiesCommonZones',
                      'amenitiesSector',
                      'timeMarket',
                      'firstCapture',
                      'lastCapture']

# Crawl responsibly by identifying yourself (and your website) on the user-agent
USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.95 Safari/537.36'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
CONCURRENT_REQUESTS = 36

# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
DOWNLOAD_DELAY = 0.5
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
#COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
#}

# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'scrapySpider.middlewares.ScrapyspiderSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#DOWNLOADER_MIDDLEWARES = {
#    'scrapySpider.middlewares.ScrapyspiderDownloaderMiddleware': 543,
#}

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
#ITEM_PIPELINES = {
#    'scrapySpider.pipelines.ScrapyspiderPipeline': 300,
#}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 0.5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 3
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 5
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = True

# Enable and configure HTTP caching (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
HTTPCACHE_ENABLED = True
HTTPCACHE_EXPIRATION_SECS = 3
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'
