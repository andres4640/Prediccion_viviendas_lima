# -*- coding: utf-8 -*-
"""
Created on Sun Nov 29 02:16:52 2020

@author: Andres
"""

from bs4 import BeautifulSoup
import requests
import pandas as pd

def importar_datos(num_paginas):
    raw_data_frame=pd.DataFrame({'Precio':[],'NCuartos':[],'Area':[],'NBaños':[],'Distrito':[], 'Amoblado':[],'Mantenimiento':[],'Cochera':[],'Azotea':[]})
    count = 1
    while count <= num_paginas:
      if count == 1 :
        url='https://www.laencontre.com.pe/alquiler/t-departamentos/lima'
      else:
        url=str('https://www.laencontre.com.pe/alquiler/t-departamentos/lima/p_'+str(count))
      page=requests.get(url)
      soup=BeautifulSoup(page.content,'html.parser')
      for link in soup.find_all('a'):
        if str(link.get('href'))[1:9] == 'inmueble' :
            url_page='https://www.laencontre.com.pe/'+str(link.get('href'))[1:] 
            page_dep=requests.get(url_page)
            soup_page_dep=BeautifulSoup(page_dep.content,'html.parser')
            precio_t = soup_page_dep.find_all('div', class_ ='price')
            ncuartos_t=soup_page_dep.find_all('li', class_ ='bedrooms')
            nbanos_t=soup_page_dep.find_all('li', class_ ='bathrooms')
            distrito_t=soup_page_dep.find_all('li', class_ ='elementBC detail-bread-li')
            area_t=soup_page_dep.find_all('li', class_ ='dimensions')
            extra_t=soup_page_dep.find_all('li', class_ ='tick')
            precio_v=list()
            ncuartos_v=list()
            nbanos_v=list()
            distrito_v=list()
            area_v=list()
            amob_v=list()
            mantenimiento_v=list()
            cochera_v=list()
            azotea_v=list()
            for i in precio_t :
              precio_v.append(i.text)
            for i in ncuartos_t :
              ncuartos_v.append(i.text)
            for i in nbanos_t :
              nbanos_v.append(i.text)
            for i in distrito_t:
              distrito_v.append(i.text)
            for i in area_t:
              area_v.append(i.text)
            for i in extra_t: 
              if i.text[0:19]=='Valor Mantenimiento':
                mantenimiento_v.append(i.text)
              elif i.text[0:4]=='Amob':
                amob_v.append(i.text)
              elif i.text[0:11]=='Cantidad de':
                cochera_v.append(i.text)
              elif i.text[0:10]=='Acceso a A':
                azotea_v.append(i.text)
    
            raw_data_frame=raw_data_frame.append({'Precio': precio_v ,'NCuartos': ncuartos_v[0:1],'Area':area_v[0:1],'NBaños':nbanos_v[0:1],
                                                  'Distrito':distrito_v[4:5],'Amoblado':amob_v,'Mantenimiento':mantenimiento_v,'Cochera':cochera_v,'Azotea':azotea_v}, ignore_index=True)
      print(count)
      count += 1
    return raw_data_frame