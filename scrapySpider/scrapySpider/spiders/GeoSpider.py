import scrapy



# Set up short list of urls to test the app
test_urls = ['https://www.metrocuadrado.com/inmueble/venta-casa-medellin-loma-de-los-bernal-5-habitaciones-4-banos-2-garajes/11281-M2789539']

# Scraper body
class MetroScraper(scrapy.Spider):

    # Naming the spider
    name = 'GeoSpider'

    # List of URLs 
    start_urls = test_urls  

    



    def parse(self, response):
        
        longtext = response.css('#__NEXT_DATA__').get()
        
        yield {
           'Decode' : longtext
        }

# We can run this spider by going to the scrapySpider mother file and using
# 1. scrapy crawl Metro2
# 2. scrappy crawl Metro2 -o filename.json \\ This option writes a json file with the downloaded data