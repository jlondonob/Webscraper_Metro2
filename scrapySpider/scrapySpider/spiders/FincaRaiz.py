
# Import libraries
import scrapy
from urllib.parse import urljoin

# Scraper body
class FincaraizSpider(scrapy.Spider):
    
    # Naming the spider
    name = 'FincaRaiz'
    
    # Starting URL
    start_urls = ['https://www.fincaraiz.com.co/casas/venta/medellin/?ad=30|1||||1||9|||55|5500006|||||||||||||||||||1||griddate%20asc||||||||']
    
    # Scrape urls from first page
    def parse(self,response):
        base_url = 'https://www.fincaraiz.com.co/'
        urls = response.xpath("//a[contains(@href,'casa-en-venta')]/@href").getall()

        clean_urls = [urljoin(base_url, url) for url in urls]
        
        yield {
            'urls': clean_urls
        }