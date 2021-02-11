# ------- Aprender a manipular listas ------#

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
