import pandas as pd
import numpy as np
import os

import pandas_dedupe
# Esta libreria sirve para strings, precio, LatLong

os.chdir("/Users/puchu/Desktop/WebScraper_Metro2/tests")

fr = pd.read_csv("../scrapySpider/FRmde.csv")
m2 = pd.read_csv("../scrapySpider/M2mde.csv")

data = fr.append(m2)
data['LatLong'] = "(" + data['latitude'].astype(str) + "," + data['longitude'].astype(str) + ")"



match2 = [
    ('propType', 'Exact','has missing'),
    ('salePrice', 'Price','has missing'),
    ('LatLong', 'LatLong','has missing'),
    ('areaBuilt', 'Exact','has missing'),
    ('rooms', 'Exact','has missing'),
    ('bathrooms', 'Exact','has missing'),
    ('stratum', 'Exact','has missing'),
    ('cityName', 'Exact')
    ]

match3 = [
    ('propType','Exact','has missing'),
    ('LatLong','LatLong','has missing'),
    ('rooms','Exact','has missing'),
    ('bathrooms','Exact','has missing'),
    ('stratum','Exact','has missing'),
    ('cityName','Exact'),
    ('salePrice','Price','has missing'),
    ('areaBuilt','Exact','has missing'),
    ('companyName','String','has missing')
]

inmo_dedup = pandas_dedupe.dedupe_dataframe(data,match3)
inmo_dedup.to_csv("result_fuzzy_duplicate.csv")



