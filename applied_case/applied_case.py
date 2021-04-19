#In this file we present an application of database
#-- Its objective is to measure if general indices of the 
#-- housing market in Medellin changed due to the announecment of
#-- weekend curfews.

#Importing libraries
from geopandas.geodataframe import GeoDataFrame
import pandas as pd

pd.set_option('display.max_columns', None)

#Importing data files
file_pre = "/Users/puchu/Desktop/WebScraper_Metro2/scrapySpider/db_FRtest/test_22_03_2021.csv"
file_post = "/Users/puchu/Desktop/WebScraper_Metro2/scrapySpider/db_FRtest/test_15_04_21.csv"

housing_pre = pd.read_csv(file_pre)
housing_post = pd.read_csv(file_post)

housing_pre.columns.tolist()

#Creating variable price/m2 
housing_pre['price_m2'] = housing_pre.salePrice/housing_pre.areaBuilt
housing_post['price_m2'] = housing_post.salePrice/housing_post.areaBuilt

#Dropping duplicates
duplicate_criteria = ["propType","rooms","bathrooms","stratum","cityName","salePrice","areaBuilt","companyName"]

housing_pre = housing_pre.drop_duplicates(duplicate_criteria)
housing_post = housing_post.drop_duplicates(duplicate_criteria)

#----------------------------------------------------------------------------------------------------------------#
#------------------------------------| GEODATAFRAME | -----------------------------------------------------------#
#----------------------------------------------------------------------------------------------------------------#

#Installing geopandas, matplotlib, and rtree
import geopandas as gpd
import matplotlib.pyplot as plt
from shapely.geometry import Point

#Reading shapefile that contains `barrios` and `veredas`
barrios = gpd.read_file("/Users/puchu/Desktop/WebScraper_Metro2/applied_case/Barrio_Vereda/Barrio_Vereda.shp")

#Creating plotly Points for houses (objective is to later merge with shape)
geometry_pre = [Point(xy) for xy in zip(housing_pre.longitude,housing_pre.latitude)]
housing_pre = gpd.GeoDataFrame(housing_pre, crs="EPSG:4326", geometry=geometry_pre)

geometry_post = [Point(xy) for xy in zip(housing_post.longitude,housing_post.latitude)]
housing_post = gpd.GeoDataFrame(housing_post, crs="EPSG:4326", geometry=geometry_post)

#Merging barrios and housing to get exact neighborhood
housing_pre_merged = gpd.sjoin(housing_pre, barrios, how="inner", op="intersects") 
housing_post_merged = gpd.sjoin(housing_post, barrios, how="inner", op="intersects")

#----------------------------------------------------------------------------------------------------------------#
#----------------------------------| GROUPBY BARRIO | -----------------------------------------------------------#
#----------------------------------------------------------------------------------------------------------------#

housing_pre_merged.to_csv("casa.csv")

housing_pre_analysis = housing_pre_merged.groupby(["NOMBRE_COM"], as_index=False).agg({'salePrice':'mean', 'propID': 'count', 'geometry':'first'})
housing_post_analysis = housing_post_merged.groupby(["NOMBRE_COM"], as_index=False).agg({'salePrice':'mean', 'propID': 'count', 'geometry':'first'})

pre_analysis_shape = housing_pre_analysis.merge(barrios[['NOMBRE_COM', 'geometry']], on="NOMBRE_COM", how='left')
pre_analysis_shape = gpd.GeoDataFrame(pre_analysis_shape, crs="EPSG:4326")

pre_analysis_shape.to_file('pre_analysis.shp')






