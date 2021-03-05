
# Import libraries
import scrapy
from scrapy.exceptions import CloseSpider
from scrapy.http import Request

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
    start_urls = [URL.format(1)]  

    def __init__(self):
        self.page_number = 1
    
    def parse(self,response):
        print(self.page_number)
        print("----------")

        next_page = response.xpath('//a[@title="Ir a la pagina Siguiente"]')
        if not next_page:
            raise CloseSpider("No more pages")

        self.page_number += 1
        yield Request(URL.format(self.page_number))
