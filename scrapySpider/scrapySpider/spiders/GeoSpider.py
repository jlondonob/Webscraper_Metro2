
# Import libraries
import scrapy
import re
import json
from unidecode import unidecode as rm_accent #remove accents
import sys
import time

# Import Porperty Item
from ..items import PropertyItem

#--------------------------------------------------------------------------------------#
#---------------------| ESTE SCRAPER ES JESUCRISTO |-----------------------------------#
#--------------------------------------------------------------------------------------#

# Set up short list of urls to test the app
test_url = ['https://www.metrocuadrado.com/inmueble/venta-casa-medellin-san-lucas-5-habitaciones-5-banos/12133-380']

# Set global list of urls for deployment
path2urls = '/Users/puchu/Desktop/WebScraper_Metro2/collectedURLS.txt'
with open(path2urls,'r') as fp:
    global_urls = json.load(fp)

print(f'Scraping {len(global_urls):,} properties from Metro Cuadrado.\n')
print(f'Under current download_speed this should take aprox. {len(global_urls)/95:2f} minutes or {(len(global_urls)/95)/60:.2f} hours.\n')

s1 = input('Do you want to continue? [y/n]')
if s1.lower() == "n":
    print('GeoSpider will close')
    time.sleep(2)
    sys.exit(0)


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
        property['cityName'] = rm_accent(basic['city']['nombre'])
        
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
        property['comment'] = rm_accent(" ".join(basic['comment'].split()))
        
        #Company Data
        property['companyId'] = basic['companyId']
        property['companyName'] = rm_accent(basic['companyName'])
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

        property['amenitiesInteriors'] = rm_accent(interiors)
        property['amenitiesExteriors'] = rm_accent(exteriors)
        property['amenitiesCommonZones'] = rm_accent(common)
        property['ammenitiesSector'] = rm_accent(sector)
        #\\\\\\\\\\\\\\\\\\\___________/////////////////////////////
        yield property

# We can run this spider by going to the scrapySpider mother file and using
# 1. scrapy crawl Metro2
# 2. scrappy crawl Metro2 -o filename.json \\ This option writes a json file with the downloaded data