import json
import pandas as pd

path = '/Users/puchu/Desktop/WebScraper_Metro2/scrapySpider/medellin_test.json'

with open(path, 'r', encoding= 'utf-8') as j:
    data = json.loads(j.read())
 
pandas_database = pd.DataFrame(data)

pandas_database.to_csv('medellin.csv',sep=';')