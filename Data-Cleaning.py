# -*- coding: utf-8 -*-
"""
Created on Sun Nov 29 02:24:49 2020

@author: Andres
"""

import pandas as pd
from webScraping import importar_datos

def limpieza_datos(row):
    columnas = raw_data_frame.columns
    
    for x in columnas:
        if isinstance(row[x], list) and len(row[x]) ==0 :
            row[x] = ""
        else:
            row[x] = row[x][0].replace("\n", "")

    return row

def limpiar_datos(df_raw):
    
    df = df_raw.copy()
    
    df = df.apply(limpieza_datos, axis=1)
    df["Precio"] = df["Precio"].str.replace("$","").str.replace(",","").str.replace('Desde$','').str.replace('(Precio a consultar)','0').str.replace("Desde","").str.replace("0Pregunta el precio al anunciante","0").str.strip()
    df["Precio"] = pd.to_numeric(df["Precio"])
    df["NCuartos"] = df["NCuartos"].str.extract('(\d+)')
    df["Area"] = df["Area"].str.extract('(\d+)')
    df["NBaños"] = df["NBaños"].str.extract('(\d*\.?\d+)')
    df["Mantenimiento"] = df["Mantenimiento"].str.extract('(\d+)')
    df["Cochera"] = df["Cochera"].str.extract('(\d+)')

    df["Amoblado"] = df["Amoblado"].str.strip()
    df["Azotea"] = df["Azotea"].str.strip()
    df["Distrito"] = df["Distrito"].str.strip()

    df["Azotea"] = df["Azotea"].apply(lambda x: "si" if x == "Acceso a Azotea" else "no")
    
    return df

######## Elegir la cantidad de paginas a exportar y limpiar ###################

num_paginas = 146
raw_data_frame = importar_datos(num_paginas)
df_clean = limpiar_datos(raw_data_frame)
df_clean.to_csv("datos.csv", index=False)
