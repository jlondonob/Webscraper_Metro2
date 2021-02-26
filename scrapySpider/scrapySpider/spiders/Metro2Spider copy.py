import scrapy
import json # read house_links.txt

# Store links retrieved in previous step (Main_scraper.py) in object
path2urls = '/Users/puchu/Desktop/WebScraper_Metro2/collectedURLS.txt'
with open(path2urls,'r') as fp:
    global_urls = json.load(fp)

# Set up short list of urls to test the app
test_urls = ['https://www.metrocuadrado.com/inmueble/venta-casa-medellin-loma-de-los-bernal-5-habitaciones-4-banos-2-garajes/11281-M2789539']

# Scraper body
class MetroScraper(scrapy.Spider):

    # Naming the spider
    name = 'Metro2'

    # List of URLs 
    start_urls = global_urls    # Use `global_urls` when ready to use
    
    
    #|-------------| SELECTING HTML ELEMENTS TO RETRIEVE |------------------- #
    #|
    #| Note: section currently contains a lot of ad hoc rules for robustness.
    #|       If possible try to generalize in the future/ make more readable.
    #|________________________________________________________________________#

    def parse(self, response):
        
        # Rooms, bathrooms & stratus,
        main_stats = response.css(
            '.d-block h2::text').getall()
        
        # Terrible solution to solve stratum=='null'
        try:
            main_stats[4] = int(main_stats[4])
        except ValueError:
            main_stats[4] = float('nan')
       
        # City
        subtitle = response.css(
            '.card-headline .card-subtitle::text').get()
        if ',' in subtitle:
            subtitle = subtitle.split(', ')[1]

        # Agent
        agent = response.css(
            '.mb-md-0::text').getall()                                 
        if len(agent)>0: 
            agent = agent[0].replace('Conoce este inmueble de ','')   
        else:
            agent = 'Ninguno'  
               
        # Code, neighborhood, price, age, area, parking (details)       
        details = response.css(
            '.card-details .card-text::text').getall()

        # Text description of house
        description = response.css(
            '.mb-3.card-text::text').get()
        
        # Administration price
        has_admin = response.xpath("//h3[contains(text(), 'Valor administración')]").getall()                           #implementation from stack overflow
        if len(has_admin)>0:
            admin_price = response.xpath(
                "(//p[preceding::h3[contains(text(), 'Valor administración')]]/text())[1]").get() # text of first tag <p> after header with text `Valor Administracion`
            admin_price = int(admin_price.replace('$','').replace('.',''))  # removes $ and . and turns into integer
        else:
            admin_price = float('nan')

        # Parking spaces
        has_parking = response.xpath(
            "//h3[contains(text(), 'Parqueaderos')]").getall()                           #implementation from stack overflow
        if len(has_parking)>0:
            parking = response.xpath(
                "(//p[preceding::h3[contains(text(), 'Parqueaderos')]]/text())[1]").get()
            parking = int(parking.replace('$','').replace('.',''))  # removes $ and . and turns into integer
        else:
            parking = int(0)


       

        
        
        # Print the desired information in output
        yield {
                    'url': response.request.url,                                    #for testing purposes
                    'city': subtitle,
                    'rooms': int(main_stats[2]),
                    'restrooms': int(main_stats[3]),
                    'stratum': main_stats[4],
                    'agent': agent.replace('Conoce este inmueble de ',''),           #extract agent name
                    'property_code_Metro2': details[0],
                    'neighborhood_common': details[1],
                    'neighborhood_official': details[2],
                    'price' : int(details[3].replace('$','').replace('.','')),       #removes $ and thousand separators
                    'parking_places' : parking,
                    'age': details[4],
                    'area_built': float(details[5].split(' ')[0]),                     #removes 'm2'
                    'area_private': float(details[6].split(' ')[0]),                   #removes 'm2'
                    'admin_price': admin_price,                                      #removes $ and thousand separators
                    'description': " ".join(description.split())
        }

# We can run this spider by going to the scrapySpider mother file and using
# 1. scrapy crawl Metro2
# 2. scrappy crawl Metro2 -o filename.json \\ This option writes a json file with the downloaded data