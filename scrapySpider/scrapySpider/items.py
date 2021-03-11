# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


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
    ZoneName = scrapy.Field()
    sectorName = scrapy.Field()
    neighborhood = scrapy.Field()
    commonNeighborhood = scrapy.Field()
    propAddress = scrapy.Field()
    floor = scrapy.Field()
    adminPrice = scrapy.Field()
    
    #Listing Information
    comment = scrapy.Field()
    numPictures = scrapy.Field()
    
    #Company Data
    companyId = scrapy.Field()
    companyName = scrapy.Field()
    propertyState = scrapy.Field() 
    
    #Other Data
    builtTime = scrapy.Field()
    stratum = scrapy.Field()
    
    #Georeference
    latitude = scrapy.Field()
    longitude = scrapy.Field()  
    
    #Amenities
    amenitiesInteriors = scrapy.Field()
    amenitiesExteriors = scrapy.Field()
    amenitiesCommonZones = scrapy.Field()
    ammenitiesSector = scrapy.Field()