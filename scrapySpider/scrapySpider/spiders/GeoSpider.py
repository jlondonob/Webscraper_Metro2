
# Import libraries
import scrapy
import re
import json

# Import Porperty Item
from ..items import PropertyItem

#--------------------------------------------------------------------------------------#
#---------------------| ESTE SCRAPER ES JESUCRISTO |-----------------------------------#
#--------------------------------------------------------------------------------------#

# Set up short list of urdataJson to test the app
test_url = ['https://www.metrocuadrado.com/inmueble/venta-casa-medellin-loma-de-los-bernal-5-habitaciones-4-banos-2-garajes/11281-M2789539']

# Scraper body
class GeoScraper(scrapy.Spider):

    # Naming the spider
    name = 'GeoSpider'

    # List of URLs 
    start_urls = test_url

    def parse(self, response):
        
        dataRaw = response.css('#__NEXT_DATA__').get()
        dataClean = re.findall(
            pattern = "(?<=type=\"application/json\">)(.*)(?=</script>)",
            string= dataRaw)
        
        # Read dataClean as JSON library
        dataJson = []
        if dataClean:
            dataJson = json.loads(dataClean[0])
        
        # Website Main Path to JSON
        main_branch = dataJson['props']['initialState']['realestate']

        # Recurrent Paths to data inside JSON
        basic = main_branch['basic']
        featured = main_branch['basic']['featured']

        # We create a Property object and store some data in it.
        # It looks funny because we are taking data from one dictionary
        # to another dictionary. Note that all information to the rigth
        # of the equal sign comes from data stored as JSON in the webpage.
        property = PropertyItem()
        
        #Basic Data
        property['propType'] = basic['propertyId']
        property['propID'] = basic['propertyType']['nombre']
        property['businessType'] = basic['businessType']
        property['publicationStatus'] = basic['publicationStatus']
        property['salePrice'] = basic['salePrice']
        property['rentPrice'] = basic['rentPrice']
        property['rentTotalPrice'] = basic['rentTotalPrice']
        property['areaBuilt'] = basic['area']
        property['areaPrivate'] = basic['areac']
        property['rooms'] = basic['rooms']
        property['bathrooms'] = basic['bathrooms']
        property['garages'] = basic['garages']
        property['cityID'] = basic['city']['id']
        property['cityName'] = basic['city']['nombre']
        property['zoneID'] = basic['zone']['id']
        property['ZoneName'] = basic['zone']['nombre']
        property['sectorName'] = basic['sector']['nombre']
        property['neighborhood'] = basic['neighborhood']
        property['commonNeighborhood'] = basic['commonNeighborhood']
        property['comment'] = " ".join(basic['comment'].split())
        
        #Company Data
        property['companyId'] = basic['companyId']
        property['companyName'] = basic['companyName']
        property['companyAddress'] = basic['companyAddress']
        property['contactPhone'] = basic['contactPhone']
        
        #Other Data
        property['propertyState'] = basic['propertyState']
        property['builtTime'] = basic['builtTime']
        property['stratum'] = basic['stratum']


        #Georeference
        property['latitude'] = basic['coordinates']['lat']
        property['longitude'] = basic['coordinates']['lon']

        #Amenities
        property['amenitiesInteriors'] =  ", ".join(featured[0]['items'])
        property['amenitiesExteriors'] = ", ".join(featured[1]['items'])
        property['amenitiesCommonZones'] = ", ".join(featured[2]['items'])
        property['ammenitiesSector'] = ", ".join(featured[3]['items'])

        yield property

# We can run this spider by going to the scrapySpider mother file and using
# 1. scrapy crawl Metro2
# 2. scrappy crawl Metro2 -o filename.json \\ This option writes a json file with the downloaded data