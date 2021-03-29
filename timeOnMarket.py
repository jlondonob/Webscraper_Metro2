import pandas as pd



#--------------------------------------------------------#
#----------| Most basic duplicate removal | -------------#
#--------------------------------------------------------#

#Read data from FincaRaiz
data_first = pd.read_csv("/Users/puchu/Desktop/WebScraper_Metro2/scrapySpider/db_FRtest/test_22_03_2021.csv")
data_second = pd.read_csv("/Users/puchu/Desktop/WebScraper_Metro2/scrapySpider/db_FRtest/test_23_03_2021.csv")

data = data_first.append(data_second, ignore_index=False)



#Change NA for -1. Aggregation deletes rows with NA
data = data.fillna(-1)

#Remove variables for aggregation purposes. They are added back later
vars = data.columns.tolist()
vars_to_remove = ['firstCapture','lastCapture']
vars = [var_kept for var_kept in vars if var_kept not in vars_to_remove] 

#Aggregate data
data_agg = data.groupby(vars, as_index=False).agg({'firstCapture':'first', 'lastCapture': 'last' })

#Calculate time in the market as difference (days) between first and last capture
data_agg['firstCapture'] = pd.to_datetime(data_agg['firstCapture'])
data_agg['lastCapture'] = pd.to_datetime(data_agg['lastCapture'])
data_agg['timeMarket'] = (data_agg['lastCapture'] - data_agg['firstCapture']).dt.days + 1

#Write file
data_agg.to_csv("data.csv", index=False)