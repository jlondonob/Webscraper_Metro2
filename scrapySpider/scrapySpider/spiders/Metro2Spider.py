import scrapy
import json # read house_links.txt

# Store links retrieved in previous step (Main_scraper.py) in object
path_to_houselinks = '/Users/puchu/Desktop/WebScraper_Metro2/house_links.txt'
with open(path_to_houselinks,'r') as fp:
    global_urls = json.load(fp)

# Set up short list of urls to test the app
test_urls = ['https://www.metrocuadrado.com/inmueble/venta-casa-medellin-la-mota-3-habitaciones-3-banos-1-garajes/12358-M2784961']

# This is the actual scraper
class MetroScraper(scrapy.Spider):

    # Gives a name to the spider. This will be used to call it through the terminal
    name = 'Metro2'
    
    # Gives URLs for spider to get.
    start_urls = global_urls    #currently in test mode. when ready use `house_links`
    # Scraping begins.
    def parse(self, response):
        # Retrieve all instances of .d-block h2::text
        main_stats = response.css('.d-block h2::text').getall()
            #price = response.css('.d-sm-none .eovJcI::text').getall()
        subtitle = response.css('.card-headline .card-subtitle::text').get()
        agent = response.css('.mb-md-0::text').get()
        details = response.css('.card-details .card-text::text').getall()
        description = response.css('.mb-3.card-text::text').get()
        
        # Print the desired information in output
        yield {
                    'url': response.request.url,                                    #for testing purposes
                    'city': subtitle.split(', ')[1],
                    'rooms': int(main_stats[2]),
                    'restrooms': int(main_stats[3]),
                    'stratum': int(main_stats [4]),
                    'agent': agent.replace('Conoce este inmueble de ',''),           #extract agent name
                    'property_code_Metro2': details[0],
                    'neighborhood_common': details[1],
                    'neighborhood_official': details[2],
                    'price' : int(details[3].replace('$','').replace('.','')),       #removes $ and thousand separators
                    'age': details[4],
                    'area_built': int(details[5].split(' ')[0]),                     #removes 'm2'
                    'area_private': int(details[6].split(' ')[0]),                   #removes 'm2'
                    'admin_price': int(details[7].replace('$','').replace('.','')),  #removes $ and thousand separators
                    'description': description
        }

# We can run this spider by going to the scrapySpider mother file and using
# 1. scrapy crawl Metro2
# 2. scrappy crawl Metro2 -o filename.json \\ This option writes a json file with the downloaded data