# ------- Aprender a manipular listas ------#
# Nota: instalar pylance para mejor autocomplete en vscode

#Creamos objetos a y b 
a = ['Hola', 'Adios']
b = ['Rob','Tom']

#Tenemos dos formas de combinar estas listas: usando el metodo
#.append() o el metodo .extend(), veamos la diferencia

a.extend(b)
print(a)

c = ['Hola', 'Adios']
d = ['Rob','Tom']

c.append(d)
print(c)

# ------- Aprender a manipular datos en general ------#

import numpy as np #numpy permite crear estructuras de n dimensiones (base de todo proyecto de data science)
import pandas as pd #manipulacion de datos

s = pd.Series([1,2,np.nan,6,8]) #creates vector. note that index starts at 0
dates = pd.date_range("20130101",periods=6)

df = pd.DataFrame(np.random.rand(6,4), index=dates, columns=list("ABCD"))
# exp: creamos un data frame con numeros extraidos de una distribucion normal
#      estandar para crear una matrix 6x4. Luego asignamos al indice las fechas
#      del objeto dates y llamamos a las columnas A,B,C y D
df

# La funcion de la clase list es muy particular, este es su comportamiento:
list('KPRS')

#_____ Viewing data ___#
df.head()
df.index
df.columns

df.to_numpy() #turns arrray from pandas to numpy. Fast computing! But cannot mix data types

df.describe() # equivalente a summary() de R
df.T          # transpose the dataframe
df.sort_index(axis=1, ascending=False) #sorts columns in descending order. Use axis=0 to sort rows (index)
df.sort_values(by="C")

df["A"]
df[0:3] #Selects rows 1 to 3

df.loc[dates[0]] # recordar que el objeto 'dates' contiene las fechas del indice
df.loc[:,["A", "B"]] #con .loc accedemos a nomenclatura de filas y columnas
df.loc[dates[0],"A"]

df.iloc[0:3] #used to select based on row number
df.loc[0:3] #used to select based on index names

df.iloc[0:3,:] #explicitly filter rows

df[df["A"]>0] #filter by column condition
df[df > 0.1]

#using the isin method

df2 = df.copy()
df2["E"] = ["one", "one", "two", "three", "four", "three"]

df2[df2["E"].isin(["two","four"])]

#setting values at a specific position

# by names
df.at[dates[0],"A"] = 0

#by position
df.iat[0,1] = 0

## MISSING GATA

# methos dropna() and fillna

## APPLY

df.apply(lambda x: x.max() - x.min())




