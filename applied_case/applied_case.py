#In this file we present an application of database
#-- Its objective is to measure if general indices of the 
#-- housing market in Medellin changed due to the announecment of
#-- weekend curfews.

#Importing libraries
import pandas as pd
import numpy as np

#Importing geopandas, matplotlib, and rtree (GeoData packages)
import geopandas as gpd
import matplotlib.pyplot as plt
from shapely.geometry import Point
pd.set_option('display.max_columns', None)

files =["/Users/puchu/Documents/WebScraper_Metro2/scrapySpider/db_FRtest/test_22_03_2021.csv", "/Users/puchu/Documents/WebScraper_Metro2/scrapySpider/db_FRtest/test_15_04_21.csv"]

#Creating index for shapefile names
index=0
global_data =[]
for file in files:
    

    #Importing data files
    house_data = pd.read_csv(file)

    #Creating variable price/m2
    house_data['price_m2'] = house_data.salePrice/house_data.areaBuilt
    house_data['price_m2'] = np.where(house_data.areaBuilt <10, np.nan, house_data['price_m2'])                 #removing m2 data for abnormally small houses (input error)
    house_data['price_m2'] = np.where(house_data.salePrice >15000000000, np.nan, house_data['price_m2'])        #removing m2 data for abnormally expensive houses (input error)

    house_data['stratum'] = house_data['stratum'].apply(pd.to_numeric, errors = 'coerce')
    #Dropping duplicates
    duplicate_criteria = ["propType","rooms","bathrooms","stratum","cityName","salePrice","areaBuilt","companyName"]
    house_data = house_data.drop_duplicates(duplicate_criteria)

    #----------------------------------------------------------------------------------------------------------------#
    #------------------------------------| GEODATAFRAME | -----------------------------------------------------------#
    #----------------------------------------------------------------------------------------------------------------#

    #Reading shapefile that contains `barrios` and `veredas`
    barrios = gpd.read_file("/Users/puchu/Desktop/WebScraper_Metro2/applied_case/shapes/Barrio_Vereda/Barrio_Vereda.shp")

    #Creating geometry column for houses (in a way that is readable by GeoDataFrame) - GeoDataF requires tuple xy
    geom = [Point(xy) for xy in zip(house_data.longitude,house_data.latitude)]
    house_data_geo = gpd.GeoDataFrame(house_data, crs="EPSG:4326", geometry=geom)

    #Merging barrios_shape and housing_data (adding barrio name and barrio geometry)
    house_data_barrio = gpd.sjoin(house_data_geo, barrios, how="right", op="intersects")  #how='right' to keep barrio polygon and not house point

    #----------------------------------------------------------------------------------------------------------------#
    #----------------------------------| GROUPBY BARRIO | -----------------------------------------------------------#
    #----------------------------------------------------------------------------------------------------------------#

    #Droping columns except:
    house_data_barrio = house_data_barrio[['NOMBRE_COM', 'geometry', 'price_m2','stratum']]

    #Aggregating data by COMUNA
    houses = house_data_barrio.dissolve(by="NOMBRE_COM", aggfunc= ['mean', 'count'], dropna=False)

    #Renaming columns to save as .shp
    houses.rename(columns='_'.join, inplace=True)                       #turn tuple column names to strings
    houses = houses.rename(columns={houses.columns[0]:'geometry'})      #rename first column to 'geometry'

    #Save housing data for firs dataset (for graph of points)
    #if index==0:
    #    house_data_geo.to_file("applied_case/shapes/houses.shp")

    index += 1 

    global_data.append(houses)


#Dumping all prior information into one dataframe
global_data[1] = global_data[1].drop(columns = 'geometry') #This is done to avoid having two 'geometry' columns
total_data = global_data[0].merge(global_data[1], on=["NOMBRE_COM"])

#Creating change variables
total_data['diff_price_m2_mean'] = (total_data.price_m2_mean_y-total_data.price_m2_mean_x) / total_data.price_m2_mean_x
total_data['diff_price_m2_count'] = (total_data.price_m2_count_y-total_data.price_m2_count_x) / total_data.price_m2_count_x

total_data.columns

total_data.columns = ['geometry', 'pricePREm', 'countPRE', 'stratumPREm','countPREstrat','pricePOSTm','countPOST', 'stratumPOSTm','countPOSTstrat','diffPrice', 'diffCount']


#Writing dataframe to file
total_data.to_file("applied_case/shapes/final.shp")

#total_data = gpd.read_file("applied_case/shapes/final.shp")
#total_data.to_csv("total_data_table.csv", sep = ";")








