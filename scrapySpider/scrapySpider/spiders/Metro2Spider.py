import scrapy
import csv   # To read links stored in a csv file. Don'y know if json file would
             # be more efficient

# Store links retrieved in previous step (Main_scraper.py) in object
global_links = []
filepath = '/Users/puchu/Desktop/WebScraper_Metro2/urls.csv'
with open(filepath, newline='') as csvfile:
    reader = csv.reader(csvfile)

    for row in reader:
        global_links.append(row[0])

global_links

# This is the actual scraper
class MetroScraper(scrapy.Spider):
    # Gives a name to the spider. This will be used to call it through the terminal
    name = 'Metro2'
    
    # Gives URLs for spider to get
    start_urls = global_links
    # Scraping begins.
    def parse(self, response):
        # Retrieve all instances of .d-block h2::text
        main_stats = response.css('.d-block h2::text').getall()
            #price = response.css('.d-sm-none .eovJcI::text').getall()
        agent = response.css('.mb-md-0::text').get()
        details = response.css('.card-details .card-text::text').getall()
        description = response.css('.mb-3.card-text::text').get()
        
        # Print the desired information in output
        yield {
                    'rooms': main_stats[2],
                    'restrooms': main_stats[3],
                    'stratum': main_stats [4],
                    'agent': agent,
                    'property_code_Metro2': details[0],
                    'neighborhood_common': details[1],
                    'neighborhood_official': details[2],
                    'price' : details[3],
                    'age': details[4],
                    'area_built': details[5],
                    'area_private': details[6],
                    'admin price': details[7],
                    'description': description
        }

# We can run this spider by going to the scrapySpider mother file and using
# 1. scrapy crawl Metro2
# 2. scrappy crawl Metro2 -o filename.json \\ This option writes a json file with the downloaded data