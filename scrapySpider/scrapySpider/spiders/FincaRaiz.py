
# Import libraries
import scrapy
from scrapy.exceptions import CloseSpider
from scrapy.http import Request
from urllib.parse import urljoin
from unidecode import unidecode as rm_accent #remove accents
import re                                    #regex
import json                                  #read data as json

from datetime import date

# Import property item. Created in items.py
from ..items import PropertyItem

# Initial URL.
# -- Change later to also include apartment sales and sales in other cities
# -- Fortunately its very easy to do so as website shows infinite pages
# -- As expl: https://www.fincaraiz.com.co/apartamento-casa/venta/cundinamarca-antioquia-valle-del-cauca-atlantico/?ad=30|1000||||1||8,9|||67,55,82,57|||||||||||||||||1|||1||griddate%20desc||||-1||||
# -- 8,9 refers to houses and aptmts. 67, 55, ... referst ot departments
# -- Try deleting all text between .co/ and /? and search will be the same
URL = 'https://www.fincaraiz.com.co/casas/venta/medellin/?ad=30|{0}||||1||9|||55|5500006|||||||||||||||||||1||griddate%20asc||||||||'

# Body
# -- Starts at `URL` when {0} == 1. Checks if there is a next page button
# -- If next page button exists it goes to next page else the spider closes.
class FincaraizSpider(scrapy.Spider):
    name = 'FincaRaiz'

    # Specific Settings (override settings.py) we want this scraper to be slower than the others
    custom_settings = {
        'DOWNLOAD_DELAY': 1,
        'CONCURRENT_REQUESTS': 5,
    }

    start_urls = [URL.format(1)]  

    def __init__(self):
        self.page_number = 1

    #---------------------------------------------------------------------------------#
    #----------------| EXTRACT INDIVIDUAL URLS FROM GENERAL PAGES |-------------------#
    #---------------------------------------------------------------------------------#

    # Define method to parse (read html and extract information) general requests
    def parse(self,response):
        print(self.page_number)
        print("----------")

        # Extract propertiy urls from each page
        # -- Need to change xpath when we include apts
        base_url = "https://www.fincaraiz.com.co/"
        partial_urls = response.xpath("//a[contains(@href, 'casa-en-venta')]/@href").getall()
        property_urls = [urljoin(base_url, partial_url) for partial_url in partial_urls]

        # Parse individual propery urls extracted before
        # -- To parse properties we use the parse_prop class, which we define later
        for property_url in property_urls:
            yield Request(property_url, callback=self.parse_prop)
        
        # After collecting individual properties' urls we check if there is a next page button
        next_page = response.xpath('//a[@title="Ir a la pagina Siguiente"]')
        # -- If button doesn't exist spider closes, else it goes to the next page
        if next_page:
            # -- Else, it goes to the next page and begins cycle again
            self.page_number += 1
            yield Request(URL.format(self.page_number))

    #---------------------------------------------------------------------------------#
    #----------------------| EXTRACT DATA FROM INDIVIDUAL URLS |----------------------#
    #---------------------------------------------------------------------------------#

    def parse_prop(self, response):
        # Retrieve JSON data stored in HTML as text
        dataRaw = response.xpath("//script[contains(., 'var sfAdvert = ')]").get()
        dataClean = re.findall(
            pattern = "(?<=var sfAdvert = )(.*)(?=;)",
            string= dataRaw)
        # Turn text into actual readable JSON data object
        FincaRaiz = []
        if dataClean:
            FincaRaiz = json.loads(dataClean[0])

        # -------------------- START FILLING PROPERTY ITEM --------------------- #
        #1. Create Property Item
        property = PropertyItem()

        #2. Populate item

        # -- Company information
        property['companyId'] = FincaRaiz['ClientId']
        property['companyName'] = rm_accent(FincaRaiz['ClientName'])

        property['propID'] = FincaRaiz['AdvertId'] 
        # -- Retrieve the type of property (casa/apartment) from the title
        property['propType'] = re.findall("(.*?)[\s]", FincaRaiz['Title'])[0]
        property['propertyState'] = FincaRaiz['AdvertType']
        property['businessType'] = FincaRaiz['TransactionType'] 
        property['salePrice'] = FincaRaiz['Price'] 
        property['areaBuilt'] = FincaRaiz['Surface'] 
        property['rooms'] = FincaRaiz['Rooms'] 
        property['bathrooms'] = FincaRaiz['Baths'] 
        property['garages'] = FincaRaiz['Garages'] 
        property['floor'] = re.findall("\d+" , FincaRaiz['Floor']) # Only selects digits (of any length)
        property['cityID'] = FincaRaiz['Location2Id'] 
        property['cityName'] = rm_accent(FincaRaiz['Location2'])
        
        property['zoneID'] = FincaRaiz['Location3Id']
        property['zoneName'] = rm_accent(FincaRaiz['Location3'])
        property['propAddress'] = FincaRaiz['Address']
        property['neighborhood'] = rm_accent(FincaRaiz['Location4'])
        property['commonNeighborhood'] =rm_accent(FincaRaiz['Location4'])
        property['comment'] = rm_accent(FincaRaiz['Description'])
        
        
        #Other Data
        
        property['builtTime'] = rm_accent(FincaRaiz['Ages'])
        property['stratum'] = FincaRaiz['Stratum']
        property['numPictures'] = FincaRaiz['NumPhotos']
        property['adminPrice'] = FincaRaiz['AdministrationPrice']


        #Georeference
        property['latitude'] = FincaRaiz['Latitude']
        property['longitude'] = FincaRaiz['Longitude']
        
        #Extras
        Extras = rm_accent(FincaRaiz['Extras'])
        
        property['amenitiesInteriors'] = re.findall(
            pattern="(?<=Interiores\$)(.*?)(?=\||\Z)",
            string=Extras)
        property['amenitiesExteriors'] = re.findall(
            pattern="(?<=Exteriores\$)(.*?)(?=\||\Z)",
            string=Extras)
        property['ammenitiesSector'] = re.findall(
            pattern="(?<=Sector\$)(.*?)(?=\||\Z)",
            string=Extras)

        #Time on Market
        # ---- Idea is that if duplicate keep first observation of `firstCapture`
        # ---- and last observation of `lastCapture`
        property['timeMarket'] = 1
        property['firstCapture'] = date.today().strftime('%d-%m-%Y')
        property['lastCapture'] = date.today().strftime('%d-%m-%Y')


        # Output
        yield property