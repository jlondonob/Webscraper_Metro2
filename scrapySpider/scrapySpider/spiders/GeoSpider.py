import scrapy
import re
import json


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
        
        #Main Path
        main_branch = dataJson['props']['initialState']['realestate']

        #Paths
        basic = dataJson['props']['initialState']['realestate']['basic']
        featured = dataJson['props']['initialState']['realestate']['basic']['featured']

        yield {
            
            #Basic Information
            'propID' : basic['propertyId'],
            'propType' : basic['propertyType']['nombre'],
            'businessType' : basic['businessType'],
            'publicationStatus' : basic['publicationStatus'],
            'salePrice' : basic['salePrice'],
            'rentPrice' : basic['rentPrice'],
            'rentTotalPrice' : basic['rentTotalPrice'],
            'areaBuilt' : basic['area'],
            'areaPrivate' : basic['areac'],
            'rooms' : basic['rooms'],
            'bathrooms' : basic['bathrooms'],
            'garages' : basic['garages'],
            'cityID' : basic['city']['id'],
            'cityName' : basic['city']['nombre'],
            'zoneID' : basic['zone']['id'],
            'ZoneName' : basic['zone']['nombre'],
            'sectorName' : basic['sector']['nombre'],
            'neighborhood' : basic['neighborhood'],
            'commonNeighborhood' : basic['commonNeighborhood'],
            'comment' : " ".join(basic['comment'].split()),

            #Company Data
            'companyId' : basic['companyId'],
            'companyName' : basic['companyName'],
            'companyAddress' : basic['companyAddress'],
            'contactPhone' : basic['contactPhone'],
            'propertyState' : basic['propertyState'],

            #Other Data
            'builtTime' : basic['builtTime'],
            'stratum' : basic['stratum'],

            #Georeference
            'latitude' : basic['coordinates']['lat'],
            'longitude' : basic['coordinates']['lon'],

            #Amenities
            'amenitiesInteriors' : ", ".join(featured[0]['items']),
            'amenitiesExteriors' : ", ".join(featured[1]['items']),
            'amenitiesCommonZones' : ", ".join(featured[2]['items']),
            'ammenitiesSector' : ", ".join(featured[3]['items'])
        }

# We can run this spider by going to the scrapySpider mother file and using
# 1. scrapy crawl Metro2
# 2. scrappy crawl Metro2 -o filename.json \\ This option writes a json file with the downloaded data