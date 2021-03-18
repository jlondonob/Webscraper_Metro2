# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

# Cannot stress importance of this processor enough.
# --- If Field is error returns none. Without it if a Field
# --- is error the scraper would ommit the observation.
# --- A Field might be an error if we try to turn to uppercase a non-present
# --- characteristic, for example if there is no zoneName.
from itemloaders.processors import TakeFirst


class PropertyItem(scrapy.Item):
    
    #Basic Data
    propID = scrapy.Field()
    propType = scrapy.Field()
    businessType = scrapy.Field()
    salePrice = scrapy.Field()
    rentPrice = scrapy.Field()
    rentTotalPrice = scrapy.Field()
    areaBuilt = scrapy.Field()
    rooms = scrapy.Field()
    bathrooms = scrapy.Field()
    garages = scrapy.Field()
    cityID = scrapy.Field()
    cityName = scrapy.Field()
    zoneID = scrapy.Field()
    zoneName = scrapy.Field(output_processor=TakeFirst())
    neighborhood = scrapy.Field(output_processor=TakeFirst())
    commonNeighborhood = scrapy.Field(output_processor=TakeFirst())
    propAddress = scrapy.Field(output_processor=TakeFirst())
    floor = scrapy.Field()
    adminPrice = scrapy.Field()
    
    #Listing Information
    comment = scrapy.Field()
    numPictures = scrapy.Field()
    
    #Company Data
    companyId = scrapy.Field()
    companyName = scrapy.Field(output_processor=TakeFirst())
    propertyState = scrapy.Field() 
    
    #Other Data
    builtTime = scrapy.Field(output_processor=TakeFirst())
    stratum = scrapy.Field()
    
    #Georeference
    latitude = scrapy.Field()
    longitude = scrapy.Field()  
    
    #Amenities
    amenitiesInteriors = scrapy.Field(output_processor=TakeFirst())
    amenitiesExteriors = scrapy.Field(output_processor=TakeFirst())
    amenitiesCommonZones = scrapy.Field(output_processor=TakeFirst())
    amenitiesSector = scrapy.Field(output_processor=TakeFirst())

    #TimeOnMarket
    timeMarket = scrapy.Field()
    firstCapture = scrapy.Field()
    lastCapture = scrapy.Field()

    #AmenitiesInterior
    hasChimney = scrapy.Field()
    hasServiceRoom = scrapy.Field()
    hasStorageSpace = scrapy.Field()
    hasInterphone = scrapy.Field()
    hasBalcony = scrapy.Field()

    #AmenitiesExterior
    extColsedComplex = scrapy.Field()
    extVigilance = scrapy.Field()
    extGreenZones = scrapy.Field()
    extCoveredGarage = scrapy.Field()

    #AmenitiesSector
    publishedSectorAmenities = scrapy.Field()

    