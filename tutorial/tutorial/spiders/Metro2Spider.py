import scrapy

class MetroScraper(scrapy.Spider):
    name = 'Metro2'
    
    start_urls = ['https://www.metrocuadrado.com/inmueble/arriendo-casa-medellin-el-tesoro-3-habitaciones-4-banos-2-garajes/2264-42130']

    def parse(self, response):
        self.logger.info('This is my first spider')
        house_stats = response.css('.d-block h2::text').getall()
        yield {
            'area': house_stats[0],
            'habitaciones': house_stats[2],
            'banos': house_stats[3],
            'estrato': house_stats [4]
            }