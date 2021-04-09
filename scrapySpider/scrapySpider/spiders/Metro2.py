
# Import libraries
import scrapy
import re
import json
from unidecode import unidecode as rm_accent #remove accents
from datetime import date

# Import Porperty Item
from ..items import PropertyItem

# NOTE: All 'DTESTING' chunks should be deleted (or turned into comments) for deployment
#       'PTESTING' chunks may stay if desired.

# Set up short list of urls to test the app
test_url = ['https://www.metrocuadrado.com/inmueble/venta-casa-medellin-san-lucas-5-habitaciones-5-banos/12133-380']

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
        

        # We create a Property object and store some data in it.
        # -- It looks funny because we are taking data from one dictionary
        # -- to another dictionary. Note that all information to the rigth
        # -- of the equal sign comes from data stored as JSON in the webpage.
        property = PropertyItem()
        
        #Basic Data
        property['propID'] = basic['propertyId']
        property['propType'] = basic['propertyType']['nombre'].upper()
        property['businessType'] = basic['businessType'].upper()
        property['salePrice'] = basic['salePrice']
        property['rentPrice'] = basic['rentPrice']
        property['rentTotalPrice'] = basic['rentTotalPrice']
        property['areaBuilt'] = basic['area']
        property['rooms'] = basic['rooms']
        property['bathrooms'] = basic['bathrooms']
        property['garages'] = basic['garages']
        property['cityID'] = basic['city']['id']
        property['cityName'] = rm_accent(basic['city']['nombre']).upper()
        
        if basic['zone']==None:
            property['zoneID'] = None
            property['zoneName'] = None
        else:
            property['zoneID'] = basic['zone']['id']
            property['zoneName'] = basic['zone']['nombre'].upper()
        
        
        try:
            property['neighborhood'] = rm_accent(basic['neighborhood']).upper()
        except:
            property['neighborhood'] = None
        try:
            property['commonNeighborhood'] = rm_accent(basic['commonNeighborhood']).upper()
        except:
            property['commonNeighborhood'] = None

        comment = rm_accent(basic['comment']).lower().rstrip()
        property['comment'] = comment


        
        #Company Data
        property['companyId'] = basic['companyId']
        try:
            property['companyName'] = rm_accent(basic['companyName']).upper()
        except:
            property['companyName'] = None
        
        #Other Data
        property['propertyState'] = basic['propertyState'].upper()
        property['builtTime'] = rm_accent(basic['builtTime']).upper()
        property['stratum'] = basic['stratum']
        property['adminPrice'] = basic['detail']['adminPrice']


        #Georeference
        property['latitude'] = basic['coordinates']['lat']
        property['longitude'] = basic['coordinates']['lon']

        #Amenities (Error handling due to sometimes non-available data)
        
        #////////////// OPTIMIZABLE\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
        #I think this section can be optimized by assigning direct values
        #to property object inside try:
        try:
            featured = main_branch['basic']['featured']
            try:
                interior = rm_accent(", ".join(featured[0]['items'])).lower()
            except:
                interior = ""
                
            property['hasChimney'] = int('chimenea' in interior + comment) #int used to transform boolean to 1 and 0
            property['hasServiceRoom'] = int(any(x in (interior + comment) for x in ['cuarto de servicio','cuarto util']))
            property['hasStorageSpace'] = None
            property['hasInterphone'] = int('citofonos' in interior + comment)
            property['extCoveredGarage'] = int(any(x in (interior + comment) for x in ['garaje cubierto', 'garage cubierto', 'parqueadero cubierto'])) #checks if any of these sentences appear
            
            try:
                exterior = rm_accent(", ".join(featured[1]['items'])).lower()
            except:
                exterior = ""

            property['hasBalcony'] = int('balcon' in exterior + comment) 
            property['extColsedComplex'] = int(any(x in (exterior + comment) for x in['conjunto cerrado', 'unidad cerrada']))
            property['extVigilance'] = int('vigilancia' in exterior + comment)
            
            
            try:
                common = rm_accent(", ".join(featured[2]['items'])).lower()
            except:
                common = ""
            
            property['extGreenZones'] = int('zonas verdes' in common + comment)

            try:
                sector = rm_accent(", ".join(featured[3]['items'])).lower()
            except :
                sector = ""

            property['publishedSectorAmenities'] = int(len(sector)>0)

            
            property['amenitiesInteriors'] = interior
            property['amenitiesExteriors'] = exterior
            property['amenitiesCommonZones'] = common
            property['amenitiesSector'] = sector
        except:
            pass
        #\\\\\\\\\\\\\\\\\\\___________/////////////////////////////

        #Time on Market
        property['timeMarket'] = 1
        property['firstCapture'] = date.today().strftime('%d-%m-%Y')
        property['lastCapture'] = date.today().strftime('%d-%m-%Y')


        yield property

# We can run this spider by going to the scrapySpider mother file and using
# 1. scrapy crawl Metro2
# 2. scrappy crawl Metro2 -o filename.json \\ This option writes a json file with the downloaded data