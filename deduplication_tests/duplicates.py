import pandas as pd
import numpy as np

#Importing FincaRaiz and MetroCuadrado scraped data
fincaRaiz = pd.read_csv("scrapySpider/FRmde.csv")
metroCuadrado = pd.read_csv("scrapySpider/M2mde.csv")

#Appending both data tables
properties = fincaRaiz.append(metroCuadrado, ignore_index=True)

#Selecting list of variables that will determine if duplicate or not.
duplicated_criteria_vars = ["propType","rooms","bathrooms","stratum","cityName"]
possible_duplicate_criteria = ["salePrice","areaBuilt","companyName"]                                                 #Construct range criteria with these variables
test_duplicate_criteria = ["propType","rooms","bathrooms","stratum","cityName","salePrice","areaBuilt","companyName"] #For testing purposes

#Write a csv file with all duplicated variables (Testing purposes)
duplicates = properties[properties.duplicated(test_duplicate_criteria, keep=False)]
duplicates.to_csv("duplicates.csv")