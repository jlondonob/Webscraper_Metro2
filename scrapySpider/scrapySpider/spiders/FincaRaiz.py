#--------------------------------------------------------------------------------------#
#-----------------------| SCRAPER SETUP |----------------------------------------------#
#--------------------------------------------------------------------------------------#

#LIBRARIES
import scrapy
from scrapy.exceptions import CloseSpider
from scrapy.http import Request
from urllib.parse import urljoin
from unidecode import unidecode as rm_accent #remove accents
import re                                    #regex
import json                                  #read data as json
from datetime import date                    #for firstCapture and lastCapture

from ..items import PropertyItem            # Import `property` item from items.py

# INITIAL URL
# -- 8,9 refers to houses and aptmts. 67,55,82,57 refers to departments
URL = 'https://www.fincaraiz.com.co/casas/venta/?ad=30|{0}||||1||8,9|||67,55,82,57|||||||||||||||||1|||1||griddate%20asc||||-1|||'

#--------------------------------------------------------------------------------------#
#-----------------------| SCRAPER BODY |-----------------------------------------------#
#--------------------------------------------------------------------------------------#
class FincaraizSpider(scrapy.Spider):
    name = 'FincaRaiz'

    #make scraper slower than the rest (override settings.py).
    custom_settings = {
        'DOWNLOAD_DELAY': 0.6,
        'CONCURRENT_REQUESTS': 5,
    }

    #start scraping at page 1
    start_urls = [URL.format(1)]  

    #set internal page number to 1
    def __init__(self):
        self.page_number = 1

    #-----------------------| EXTRACT PROPERTY URLS FROM SCROLLING PAGES |-------------------#

    # DEFINE PARSE METHOD (how to handle scrolling page requests)
    def parse(self,response):

        #1. print page number
        print(self.page_number)
        print("----------")

        #2. extract all urls of properties shown in scrolling page.
        base_url = "https://www.fincaraiz.com.co/"
        partial_urls = response.xpath("//a[contains(@href,'casa-en-venta') or contains(@href,'apartamento-en-venta')]/@href").getall()
        property_urls = [urljoin(base_url, partial_url) for partial_url in partial_urls]

        #3. parse propery pages extracted in step 2 using the parse_prop method
        for property_url in property_urls:
            yield Request(property_url, callback=self.parse_prop) #note that callback is set to `parse_prop`
        
        #4. check if next_page button exists. if it does go to the next page
        next_page = response.xpath('//a[@title="Ir a la pagina Siguiente"]')
        if next_page:
            self.page_number += 1
            yield Request(URL.format(self.page_number))           #note that callback is not defined. thus scrapy uses the `parse` method


    #-----------------------| EXTRACT DATA FROM PROPERTY PAGES |----------------------------#

    # DEFINE PARSE_PROP METHOD (how to handle property page requests)
    def parse_prop(self, response):

        #1. capture the script that contains the property's data
        dataRaw = response.xpath("//script[contains(., 'var sfAdvert = ')]").get()
        
        #2. select only the json part (located between texts "?<=var sfAdvert = " and ";")
        dataClean = re.findall(
            pattern = "(?<=var sfAdvert = )(.*)(?=;)",
            string= dataRaw)

        #3. turn text into actual readable JSON data object
        FincaRaiz = []
        if dataClean:
            FincaRaiz = json.loads(dataClean[0])

        #4. --------------------* START FILLING PROPERTY ITEM *---------------------------- #
        
        #4.1. create Property Item
        property = PropertyItem()

        #4.2. Populate item using clean data from step 3.

        property['source'] = "FINCARAIZ"

        #Company information
        property['companyId'] = FincaRaiz['ClientId']
        property['companyName'] = rm_accent(FincaRaiz['ClientName']).upper()

        property['propID'] = FincaRaiz['AdvertId'] 
        #Property info------------------------------------------
        property['propType'] = re.findall("(.*?)[\s]", FincaRaiz['Title'])[0].upper() #extract first word of TITLE before a space character (to get type of property)
        
        propertyState = FincaRaiz['AdvertType'].upper()                               #translate propertyState to spanish (make it comparable with Metro Cuadrado)
        property['propertyState'] = "USADO" if propertyState=="USED" else "NUEVO"     #
        
        property['businessType'] = FincaRaiz['TransactionType'].upper() 
        property['salePrice'] = FincaRaiz['Price'] 
        property['areaBuilt'] = FincaRaiz['Surface'] 
        property['rooms'] = FincaRaiz['Rooms'] 
        property['bathrooms'] = FincaRaiz['Baths'] 
        property['garages'] = FincaRaiz['Garages'] 
        property['floor'] = re.findall("\d+" , FincaRaiz['Floor'])                     #selects only digits (of any length)
        
        #Location-----------------------------------------------
        property['cityID'] = FincaRaiz['Location2Id'] 
        property['cityName'] = rm_accent(FincaRaiz['Location2']).upper()
        property['zoneID'] = FincaRaiz['Location3Id']
        property['zoneName'] = rm_accent(FincaRaiz['Location3']).upper()
        property['neighborhood'] = rm_accent(FincaRaiz['Location4']).upper()
        property['propAddress'] = rm_accent(FincaRaiz['Address']).upper()

        #Comment-----------------------------------------------
        comment = rm_accent(FincaRaiz['Description']).lower()
        comment = ' '.join(comment.split())                                              #remove double spaces from comments
        property['comment'] = comment
        
        #Other Data-----------------------------------------------
        property['builtTime'] = rm_accent(FincaRaiz['Ages']).upper()
        property['stratum'] = FincaRaiz['Stratum']
        property['numPictures'] = FincaRaiz['NumPhotos']
        property['adminPrice'] = FincaRaiz['AdministrationPrice']

        #Georeference-----------------------------------------------
        property['latitude'] = FincaRaiz['Latitude']
        property['longitude'] = FincaRaiz['Longitude']
        
        #Extras
        Extras = rm_accent(FincaRaiz['Extras'])

        #Interior Amenities----------------------------------------------
        try:
            interior = re.findall(
                pattern="(?<=Interiores\$)(.*?)(?=\||\Z)",                               #this means select text from "Interiores\" to "|"" or to end of string if "|" does not exist
                string=Extras)[0].lower()
        except IndexError:
            interior = ""
        
        property['amenitiesInteriors'] = interior
            #check if words are in either interior or comment
        property['hasBalcony'] = int('balcon' in interior + comment)                     #int used to transform boolean to 1 and 0
        property['hasChimney'] = int('chimenea' in interior + comment)
        property['hasServiceRoom'] = int(any(x in (interior + comment) for x in ['cuarto de servicio','cuarto util']))
        property['hasStorageSpace'] = int('bodega' in interior + comment)
        property['hasInterphone'] = int('citofono' in interior + comment)
        property['hasAirConditioner'] = int('aire acondicionado' in interior + comment)

        #Exterior Amenities-----------------------------------------------
        try:
            exterior = re.findall(
                pattern="(?<=Exteriores\$)(.*?)(?=\||\Z)",
                string=Extras)[0].lower()
        except IndexError:
            exterior = ""

        property['amenitiesExteriors'] = exterior
            #check if words are in either exterior or comment
        property['extColsedComplex'] = int(any(x in (exterior + comment) for x in['conjunto cerrado', 'unidad cerrada']))
        property['extVigilance'] = int('vigilancia' in exterior + comment)
        property['extGreenZones'] = int('zonas verdes' in exterior + comment)
        property['extCoveredGarage'] = int(any(x in (exterior + comment) for x in ['garaje cubierto', 'garage cubierto', 'parqueadero cubierto'])) #checks if any of these sentences appear

        #Sector Amenities-----------------------------------------------
        try:
            sector = re.findall(
                pattern="(?<=Sector\$)(.*?)(?=\||\Z)",
                string=Extras)[0].lower()
        except IndexError:
            sector = ""

        property['amenitiesSector'] = sector
        property['publishedSectorAmenities'] = int(len(sector)>0)

        #Time on Market-----------------------------------------------
            #idea is that if duplicate keep first observation of `firstCapture`
            #and last observation of `lastCapture`
        property['timeMarket'] = 1
        property['firstCapture'] = date.today().strftime('%d-%m-%Y')
        property['lastCapture'] = date.today().strftime('%d-%m-%Y')


        #PROPERTY PAGE'S OUTPUT
        yield property