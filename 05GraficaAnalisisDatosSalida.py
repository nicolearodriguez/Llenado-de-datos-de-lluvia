# -*- coding: utf-8 -*-
"""
Created on Thu Oct 17 15:41:02 2019

@author: nicole.rodriguez

ANÁLISIS DE LAS ESTACIONES QUE TIENEN INFORMACIÓN DE PRECIPITACIÓN
1.Mapa de calor dónde se refleja el número de datos faltantes de cada estación analizada.
"""

import pandas as pd
import numpy as np
import seaborn as sns; sns.set()
import matplotlib.pyplot as plt
import geopandas as gdp

#INTRODUZCA la serie de años a analizar
year1=1970
year2=2017
DF_PorAños=np.arange(year1,year2+1)
DF_PorAños=pd.DataFrame(DF_PorAños,columns=['Año'],dtype=str)

####################LECTURA DE DATOS####################

#Lectura del dataframe con los datos diarios de precipitación ya llenados en la programación anterior.
DF_ValoresPrecipitacion=pd.read_csv('M:/Relleno_Sanitario_BGA/03_ESTUDIO UIS/08_GEOHIDRICO/16 Python/02Precipitación/01 Llenado de datos faltantes/04LlenadoDatosFaltantes/04Datos Faltantes_Nuevo.csv')

#DataFrame de las estaciones que se analizaran.
DF_EstacionesEstudio=pd.read_csv('M:/Relleno_Sanitario_BGA/03_ESTUDIO UIS/08_GEOHIDRICO/16 Python/02Precipitación/01 Llenado de datos faltantes/02Insumos/02EstacionesLlenar.csv')
DF_EstacionesEstudio["Estacion"]=DF_EstacionesEstudio["Estacion"].astype(str)

####################CANTIDAD DE DATOS FALTANTES POR AÑO POR ESTACIÓN####################

for i in range (0,len(DF_EstacionesEstudio)):###len(DF_EstacionesEstudio)
    #print(i)
    #Estación a analizar
    Estacion_Base=DF_EstacionesEstudio.loc[i,'Estacion']
    Nombre_Estacion_Base=DF_EstacionesEstudio.loc[i,'Nombre']
    ###print('La estación en estudio es: ',E)
    #Separo las precipitaciones por estación
    DF_PrecipitacionPorEstacion=DF_ValoresPrecipitacion[['date',Estacion_Base]]
    ###print(DF_PrecipitacionPorEstacion)
    DF_PrecipitacionPorEstacion["date"]=DF_PrecipitacionPorEstacion["date"].astype(str)
    ###print(DF_PrecipitacionPorEstacion)
    for k in range (0,len(DF_PorAños)):
        #Se determina el año de estudio
        Año=DF_PorAños.loc[k,'Año']
        ##print('El año de estudio es :',A)
        #Tomo los datos de precipitación del año de estudio
        DF_EstacionPorAño=DF_PrecipitacionPorEstacion[DF_PrecipitacionPorEstacion['date'].str.contains(Año)]
        ###print(DF_EstacionPorAño)
        #Determino cuántos datos nulos hay en el año año
        DF_PorAños.loc[k,Nombre_Estacion_Base]=sum(pd.isnull(DF_EstacionPorAño[Estacion_Base]))
        ##print('Los datos nulos del año son: ',DF_PorAños.loc[k,E])
        if len(DF_EstacionPorAño)==0:
            DF_PorAños.loc[k,Nombre_Estacion_Base]=365
        ##print('Los NaN en el año son: ',DF_PorAños.loc[k,E])

DF_PorAños.set_index("Año",inplace=True)
###print(DF_PorAños)
###DF_PorAños.reset_index().to_csv('CantidadDatosFaltantesAnualSalida.csv',header=True,index=False)

#Se suman los datos faltantes de las estaciones en todo el periodo de tiempo escogido.
for t in range (0,len(DF_EstacionesEstudio)):
    Nombre=DF_EstacionesEstudio.loc[t,'Nombre']
    DF_EstacionesEstudio.loc[t,'DatosFaltantes']=sum(DF_PorAños[Nombre])

####################MAPA DE CALOR DE LOS DATOS FALTANTES####################

Map=plt.figure(figsize = (20,20)) 
sns.heatmap(DF_PorAños, linewidths=.5, cmap ='coolwarm',cbar=True, annot=True, fmt="g") 
plt.title('CANTIDAD DE DATOS FALTANTES POST LLENADO', fontsize = 20) 
plt.xlabel('Estaciones', fontsize = 15) 
plt.ylabel('Años', fontsize = 15)
plt.show()
Map.savefig('05GraficaAnalisisDatosSalida.pdf')
Map.savefig('05GraficaAnalisisDatosSalida.jpg')
    
####################ESPACIALIZACIÓN DE DATOS####################

#Se generán las listas de las coordenadas y de los códigos de las estaciones.
x=DF_EstacionesEstudio['X']
y=DF_EstacionesEstudio['Y']
N=DF_EstacionesEstudio['Estacion']
C=DF_EstacionesEstudio['DatosFaltantes']

#Se hace las espacialización de las estaciones.
fig, ax = plt.subplots(1, 1, figsize=(12, 12))
M = ax.scatter(x,y,marker='o',c=C, cmap ='coolwarm')
ax.set_xlabel("Longitud")
ax.set_ylabel("Latitud")
ax.set_title('UBICACIÓN DE ESTACIONES-Cantidad de Datos Faltantes', pad = 20, fontdict={'fontsize':20, 'color': '#4873ab'})
  
fig.colorbar(M, ax=ax, orientation='vertical')                                                            
                                                            
#Se agrega el área de estudio en formato shape para un mejor análisis.
map_Zona=gdp.read_file('M:/Relleno_Sanitario_BGA/01_CART/02_SHP/01_BASE/Area_Estudio/Area_Est_60Km+Cuencas.shp')
map_Zona.plot(ax=ax, color='#89c0e8', zorder=0)
                         
#Se hace la respectiva etiqueta de los códigos de las estaciones.
for i, txt in enumerate(N):
    plt.annotate(str(txt), (x[i],y[i]))

plt.legend(loc='upper right')
plt.show()

fig.savefig('05MapaDatosSalida.pdf')
fig.savefig('05MapaDatosSalida.jpg')