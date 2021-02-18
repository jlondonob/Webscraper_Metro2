import scrapy

# This is the actual scraper
class MetroScraper(scrapy.Spider):
    # Gives a name to the spider. This will be used to call it through the terminal
    name = 'Metro2'
    
    # Gives URLs for spider to get
    start_urls = ['https://www.metrocuadrado.com/inmueble/arriendo-casa-medellin-el-tesoro-3-habitaciones-4-banos-2-garajes/2264-42130']

    # Scraping begins.
    def parse(self, response):
        # Retrieve all instances of .d-block h2::text
        house_stats = response.css('.d-block h2::text').getall()
        # Print the desired information in output
        yield {
            'area': house_stats[0],
            'habitaciones': house_stats[2],
            'banos': house_stats[3],
            'estrato': house_stats [4]
            }

# We can run this spider by going to the scrapySpider mother file and using
# 1. scrapy crawl Metro2
# 2. scrappy crawl Metro2 -o filename.json \\ This option writes a json file with the downloaded data