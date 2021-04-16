#In this file we present an application of database
#-- Its objective is to measure if general indices of the 
#-- housing market in Medellin changed due to the announecment of
#-- weekend curfews.

#Importing libraries
import pandas as pd

#Importing data files
file_pre = "/Users/puchu/Desktop/WebScraper_Metro2/scrapySpider/db_FRtest/test_22_03_2021.csv"
file_post = "/Users/puchu/Desktop/WebScraper_Metro2/scrapySpider/db_FRtest/test_15_04_21.csv"

housing_pre = pd.read_csv(file_pre)
housing_post = pd.read_csv(file_post)

#Dropping duplicates
duplicate_criteria = ["propType","rooms","bathrooms","stratum","cityName","salePrice","areaBuilt","companyName"]

housing_pre = housing_pre.drop_duplicates(duplicate_criteria)
housing_pre = housing_pre.drop_duplicates(duplicate_criteria)


## Example

from urllib.request import urlopen
import json
with urlopen('https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json') as response:
    counties = json.load(response)

import pandas as pd
df = pd.read_csv("https://raw.githubusercontent.com/plotly/datasets/master/fips-unemp-16.csv",
                   dtype={"fips": str})

counties.keys()
counties['features'].keys()

import plotly.express as px

fig = px.choropleth_mapbox(df, geojson=counties, locations='fips', color='unemp',
                           color_continuous_scale="Viridis",
                           range_color=(0, 12),
                           mapbox_style="carto-positron",
                           zoom=3, center = {"lat": 37.0902, "lon": -95.7129},
                           opacity=0.5,
                           labels={'unemp':'unemployment rate'}
                          )
fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
fig.show()
