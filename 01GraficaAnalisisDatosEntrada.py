# -*- coding: utf-8 -*-
"""
Created on Wed Oct 16 08:12:00 2019

@author: nicole.rodriguez

ANÁLISIS DE LAS ESTACIONES QUE TIENEN INFORMACIÓN DE PRECIPITACIÓN
1.Mapa de calor dónde se refleja el número de datos faltantes de cada estación para tener en cuenta y así determinar que estaciones se analizarán.
"""
"""ORDEN DEL ANÁLISIS DE DATOS FALTANTES:
    1.01GraficaAnalisisDatosEntrada.py
    2.02Insumos_Datos.py
    3.03AnalisisEstaciones.py
    4.04LlendoDatosFaltantes.py
    5.05GraficaAnalisisDatosSalida.py"""
    
import pandas as pd
import numpy as np
from pyproj import Proj, transform 
import geopandas as gdp
import matplotlib.pyplot as plt
import seaborn as sns; sns.set()

#INTRODUZCA la serie de años a analizar
year1=1945
year2=2017
DF_PorAños=np.arange(year1,year2+1)
DF_PorAños=pd.DataFrame(DF_PorAños,columns=['Año'],dtype=str)

####################LECTURA DE DATOS####################
#Se ingresas el csv con todas las estaciones del IDEAM descargado de la página http://www.ideam.gov.co/solicitud-de-informacion.
DF_IDEAM=pd.read_csv('M:/Relleno_Sanitario_BGA/03_ESTUDIO UIS/08_GEOHIDRICO/16 Python/02Precipitación/01 Llenado de datos faltantes/00CNE_IDEAM.csv',encoding='latin-1')  ##VERIFICAR que el archivo este separado por comas y los números por puntos.
DF_IDEAM=DF_IDEAM[['CODIGO','nombre','ESTADO','altitud','latitud','longitud']]
DF_IDEAM['CODIGO']=DF_IDEAM['CODIGO'].astype(str)

#Se lee el dataframe de los datos de precipitación previamente unidos.
DF_ValoresPrecipitacion=pd.read_csv('M:/Relleno_Sanitario_BGA/03_ESTUDIO UIS/08_GEOHIDRICO/16 Python/02Precipitación/01 Llenado de datos faltantes/00Valores de Precipitacion.csv') 
DF_ValoresPrecipitacion=DF_ValoresPrecipitacion[['cod','date','valor']]
DF_ValoresPrecipitacion['cod']=DF_ValoresPrecipitacion['cod'].astype(str)

#Se determinan las estaciones que tienen información de precipitación.
DF_EstacionesIDEAM=pd.unique(DF_ValoresPrecipitacion['cod']) 
DF_EstacionesIDEAM=pd.DataFrame(DF_EstacionesIDEAM,columns=['Estacion'],dtype=str)

####################ASIGNACIÓN DE LOS NOMBRES A LOS CÓDIGOS DE ESTACIÓN####################

for n in range (0,len(DF_EstacionesIDEAM)):
    #Seleccionamos la estación que analizaremos.
    Estacion_Base=DF_EstacionesIDEAM.loc[n,'Estacion']
    for m in range (0,len(DF_IDEAM)):
        if DF_IDEAM.loc[m,'CODIGO']==Estacion_Base:
            #Le asignamos el nombre a la estación base.
            DF_EstacionesIDEAM.loc[n,'Nombre']=DF_IDEAM.loc[m,'nombre']
            #Le asignamos su estado (Activa/Suspendida) a la estación base.
            DF_EstacionesIDEAM.loc[n,'Estado']=DF_IDEAM.loc[m,'ESTADO']

DF_EstacionesIDEAM['Estacion']=DF_EstacionesIDEAM['Estacion'].astype(str)
print('Las estaciones de las cuales se tiene información de precipitación son: ')
print(DF_EstacionesIDEAM)

####################CANTIDAD DE DATOS FALTANTES POR AÑO POR NOMBRE DE ESTACIÓN####################

DF_ValoresPrecipitacion.set_index("cod",inplace=True)
for i in range (0,len(DF_EstacionesIDEAM)):###len(DF_EstacionesIDEAM)
    #print(i)
    #Seleccionamos la estación que analizaremos.
    Estacion_Base=DF_EstacionesIDEAM.loc[i,'Estacion']
    Nombre_Estacion_Base=DF_EstacionesIDEAM.loc[i,'Nombre']
    ###print('La estación en estudio es: ',E)
    #Seleccionamos los datos de la estación que se está analizando.
    DF_PrecipitacionPorEstacion=DF_ValoresPrecipitacion.loc[Estacion_Base]
    DF_PrecipitacionPorEstacion["date"]=DF_PrecipitacionPorEstacion["date"].astype(str)
    ###print(DF_PrecipitacionPorEstacion)
    for k in range (0,len(DF_PorAños)):
        #Se determina el año de estudio
        Año=DF_PorAños.loc[k,'Año']
        ##print('El año de estudio es :',A)
        #Seleccionamos los datos de precipitación del año de estudio
        DF_EstacionPorAño=DF_PrecipitacionPorEstacion[DF_PrecipitacionPorEstacion['date'].str.contains(Año)]
        ##print(DF_EstacionPorAño)
        #Determino cuántos datos nulos hay en el año en análisis.
        DF_PorAños.loc[k,Nombre_Estacion_Base]=sum(pd.isnull(DF_EstacionPorAño['valor']))
        ##print('Los datos nulos del año son: ',DF_PorAños.loc[k,E])
        #Si la estación no tiene el año en estudio, se le asignaran 365 datos nulos.
        if len(DF_EstacionPorAño)==0:
            DF_PorAños.loc[k,Nombre_Estacion_Base]=365
        ##print('Los NaN en el año son: ',DF_PorAños.loc[k,E])

DF_PorAños.set_index("Año",inplace=True)
###print(DF_PorAños)
#DF_PorAños.reset_index().to_csv('01CantidadDatosFaltantesAnualEntrada.csv',header=True,index=False)

####################MAPA DE CALOR DE LOS DATOS FALTANTES####################

#Se elabora el mapa de calor a partir de los datos nulos por año de cada estación.
Map=plt.figure(figsize = (20,20)) 
sns.heatmap(DF_PorAños, linewidths=.5, cmap ='coolwarm',cbar=True, annot=True, fmt="g") 
plt.title('CANTIDAD DE DATOS FALTANTES PRE LLENADO', fontsize = 20) 
plt.xlabel('Estaciones', fontsize = 15) 
plt.ylabel('Años', fontsize = 15)

print('El análisis de la cantidad de datos faltantes en cada estación es: ')
plt.show()

Map.savefig('01GraficaAnalisisDatosEntrada.pdf')
Map.savefig('01GraficaAnalisisDatosEntrada.jpg')

#Se suman los datos faltantes de las estaciones en todo el periodo de tiempo escogido.
for t in range (0,len(DF_EstacionesIDEAM)):
    Estacion_Base=DF_EstacionesIDEAM.loc[t,'Estacion']
    Nombre_Estacion_Base=DF_EstacionesIDEAM.loc[t,'Nombre']
    DF_EstacionesIDEAM.loc[t,'DatosFaltantes']=sum(DF_PorAños[Nombre_Estacion_Base])

###print(DF_EstacionesIDEAM)

####################COORDENADAS PLANAS####################

DF_IDEAMPlanas=pd.DataFrame(DF_EstacionesIDEAM,columns=['Estacion'],dtype=str)

for h in range(0,len(DF_EstacionesIDEAM)):
    #Seleccionamos la estación que analizaremos
    Estacion_Base=DF_EstacionesIDEAM.loc[h,'Estacion']
    for m in range (0,len(DF_IDEAM)):
        if DF_IDEAM.loc[m,'CODIGO']==Estacion_Base:
            #Le asignamos el nombre de la estación base al nuevo dataframe.
            DF_IDEAMPlanas.loc[h,'Nombre']=DF_IDEAM.loc[m,'nombre']
            #Asignamos la cantidad de datos faltantes en la estación en estudio.
            DF_IDEAMPlanas.loc[h,'DatosFaltantes']=DF_EstacionesIDEAM.loc[h,'DatosFaltantes']
            #Se determinan el epsg de entrada y el epsg de salida.
            inProj = Proj(init='epsg:4326') 
            outProj = Proj(init='epsg:3116') 
            #Latitud y longitud de la estación en estudio.
            x1=DF_IDEAM.loc[m,'longitud']
            y1=DF_IDEAM.loc[m,'latitud']
            #Se aplica la transformación de coordenadas.
            x2,y2 = transform(inProj,outProj,x1,y1)
            #Se llena el datframe con las nuevas coordenadas planas.
            DF_IDEAMPlanas.loc[h,'X']=x2
            DF_IDEAMPlanas.loc[h,'Y']=y2


#Se generán las listas de las coordenadas y de los códigos de las estaciones.
x=DF_IDEAMPlanas['X']
y=DF_IDEAMPlanas['Y']
N=DF_IDEAMPlanas['Estacion']
C=DF_IDEAMPlanas['DatosFaltantes']

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

fig.savefig('01MapaDatosEntrada.pdf')
fig.savefig('01MapaDatosEntrada.jpg')