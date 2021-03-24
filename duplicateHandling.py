import pandas as pd
import numpy as np


# Cargamos las dos bases de datos
data1 = pd.read_csv("VentasCasas_Medellin.csv")
data2 = pd.read_csv("casas.csv")

# data1 tiene un error con los nombres de dos variables. Corregimos
data1 = data1.rename(columns={'propID':'propType2'})
data1 = data1.rename(columns={'propType':'propID'})
data1 = data1.rename(columns={'propType2':'propType'})
data1.columns.tolist()

# Simulamos una variable que va a existir en el futuro
data1['timeMarket'] = 1
data2['timeMarket'] = 1

# Removemos duplicados
data1 = data1.drop_duplicates()
data2 = data2.drop_duplicates()

# Unimos mediante append
data = data1.append(data2, ignore_index=False)

# Corroboramos union
len(data.index)

# Reemplazamos None por -1 para que groupby sirva
data = data.fillna(-1)

# Mientras resolvemos problema de tildes en texto
vars = data.columns.tolist()
vars_to_rm = ['amenitiesCommonZones','amenitiesExteriors','amenitiesInteriors', 'ammenitiesSector', 'areaPrivate', 'builtTime', 'cityName', 'commonNeighborhood', 'companyAddress', 'comment', 'contactPhone', 'neighborhood', 'publicationStatus', 'adminPrice']
# Quita las variables definidas anteriormente.
vars = [ele for ele in vars if ele not in vars_to_rm] 


# Sumamos timeMarket en repetidos
d = data.groupby(vars, as_index=False).agg({'timeMarket':'sum'})

# Exportamos resultados

d.to_csv('Week1.csv', index=False)

