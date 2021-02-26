
# Import libraries
import scrapy
import re
import json

# Import Porperty Item
from ..items import PropertyItem

#--------------------------------------------------------------------------------------#
#---------------------| ESTE SCRAPER ES JESUCRISTO |-----------------------------------#
#--------------------------------------------------------------------------------------#

# Set up short list of urls to test the app
test_url = ['https://www.metrocuadrado.com/inmueble/venta-casa-medellin-belencito-4-habitaciones-4-banos/2895-1042303']

# Set global list of urls for deployment
path2urls = '/Users/puchu/Desktop/WebScraper_Metro2/collectedURLS.txt'
with open(path2urls,'r') as fp:
    global_urls = json.load(fp)


# Scraper body
class GeoScraper(scrapy.Spider):

    # Naming the spider
    name = 'GeoSpider'

    # List of URLs 
    start_urls = global_urls

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
        property['propID'] = basic['propertyId']
        property['propType'] = basic['propertyType']['nombre']
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
        
        if basic['zone']==None:
            property['zoneID'] = None
            property['ZoneName'] = None
        else:
            property['zoneID'] = basic['zone']['id']
            property['ZoneName'] = basic['zone']['nombre']
            
        if basic['sector']==None:
            property['sectorName'] = None
        else:
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

        #Amenities (Error handling due to sometimes non-available data)
        
        #////////////// OPTIMIZABLE\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
        #I think this section can be optimized by assigning direct values
        #to property object inside try:
        try:
            interiors = ", ".join(featured[0]['items'])
        except:
            interiors = None
        
        try:
            exteriors = ", ".join(featured[1]['items'])
        except:
            exteriors = None

        try:
            common = ", ".join(featured[2]['items'])
        except:
            common = None
        
        try:
            sector = ", ".join(featured[3]['items'])
        except :
            sector = None

        property['amenitiesInteriors'] = interiors
        property['amenitiesExteriors'] = exteriors
        property['amenitiesCommonZones'] = common
        property['ammenitiesSector'] = sector
        #\\\\\\\\\\\\\\\\\\\___________/////////////////////////////
        yield property

# We can run this spider by going to the scrapySpider mother file and using
# 1. scrapy crawl Metro2
# 2. scrappy crawl Metro2 -o filename.json \\ This option writes a json file with the downloaded data