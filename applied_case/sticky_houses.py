#Importing geopandas, matplotlib, and rtree (GeoData packages)
import pandas as pd
import numpy as np

import geopandas as gpd
import matplotlib.pyplot as plt
from shapely.geometry import Point


files =["/Users/puchu/Documents/WebScraper_Metro2/scrapySpider/db_FRtest/test_22_03_2021.csv", "/Users/puchu/Documents/WebScraper_Metro2/scrapySpider/db_FRtest/test_15_04_21.csv"]

houses1 = pd.read_csv(files[0])
houses2 = pd.read_csv(files[1])

db = pd.concat([houses1, houses2])
db = db.fillna(-1)

vars = db.columns.tolist()
vars.remove("firstCapture")
vars.remove("lastCapture")
vars.remove("source")
vars.remove("propertyState")

db = db.groupby(vars, as_index=False).agg({'firstCapture':'first', 'lastCapture': 'last', 'timeMarket':'sum' })

#Compare total unique houses to the number of houses that stayed in the market during both dates
len(db.index)
len(db[db['timeMarket']==2])


db['stuck'] = np.where(db.timeMarket==2,1,0)
db = db[db['firstCapture']=="22-03-2021"]
geom = [Point(xy) for xy in zip(db.longitude,db.latitude)]

db = gpd.GeoDataFrame(db, crs="EPSG:4326", geometry=geom)

barrios = gpd.read_file("/Users/puchu/Desktop/WebScraper_Metro2/applied_case/shapes/Barrio_Vereda/Barrio_Vereda.shp")
data_stuck_barrio = gpd.sjoin(db, barrios, how="right", op="intersects")  #how='right' to keep barrio polygon and not house point

data_stuck_barrio = data_stuck_barrio[['NOMBRE_COM', 'geometry','stuck']]
houses_stuck = data_stuck_barrio.dissolve(by="NOMBRE_COM", aggfunc='mean', dropna=False)

houses_stuck.to_file("applied_case/shapes/stuck/stuck.shp")

houses_stuck.head()