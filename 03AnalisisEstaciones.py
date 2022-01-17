# -*- coding: utf-8 -*-
"""
Created on Fri Oct 25 09:00:27 2019

@author: nicole.rodriguez

ANÁLISIS DE LAS ESTACIONES SELECCIONADAS
1.Espacialización de las estaciones que tienen información de precipitación.
2.Gráfica de distancia vs Px/P de la estación escogida.
"""

import geopandas as gdp
import pandas as pd
import matplotlib.pyplot as plt

####################LECTURA DE DATOS####################

#Los csv que se usarán son algunos de los resultados obtenidos en la programación de 02Insumos_Datos

CoordenadasPlanas=pd.read_csv('M:/Relleno_Sanitario_BGA/03_ESTUDIO UIS/08_GEOHIDRICO/16 Python/02Precipitación/01 Llenado de datos faltantes/02Insumos/02CoordenadasPlanas.csv')
CoordenadasPlanas["Estacion"]=CoordenadasPlanas["Estacion"].astype(str)

RelacionPrecip=pd.read_csv('M:/Relleno_Sanitario_BGA/03_ESTUDIO UIS/08_GEOHIDRICO/16 Python/02Precipitación/01 Llenado de datos faltantes/02Insumos/02RelacionPrecipitacion.csv')
RelacionPrecip["Estacion"]=RelacionPrecip["Estacion"].astype(str)

Distancias=pd.read_csv('M:/Relleno_Sanitario_BGA/03_ESTUDIO UIS/08_GEOHIDRICO/16 Python/02Precipitación/01 Llenado de datos faltantes/02Insumos/02Distancias.csv')
Distancias["Estacion"]=Distancias["Estacion"].astype(str)

EstacionesApoyo=pd.read_csv('M:/Relleno_Sanitario_BGA/03_ESTUDIO UIS/08_GEOHIDRICO/16 Python/02Precipitación/01 Llenado de datos faltantes/02Insumos/02EstacionesApoyo.csv')
EstacionesApoyo.fillna(0,inplace=True)
EstacionesApoyo=EstacionesApoyo.astype(int)
EstacionesApoyo=EstacionesApoyo.astype(str)

Estaciones=pd.read_csv('M:/Relleno_Sanitario_BGA/03_ESTUDIO UIS/08_GEOHIDRICO/16 Python/02Precipitación/01 Llenado de datos faltantes/02Insumos/02EstacionesSelect.csv')
Estaciones["Estacion"]=Estaciones["Estacion"].astype(str)
Estaciones.set_index('Estacion',inplace=True)
Estaciones.drop(['index'],axis='columns',inplace=True)

####################ESPACIALIZACIÓN DE LAS ESTACIONES EN LA ZONA DE ESTUDIO####################

#Se generán las listas de las coordenadas y de los códigos de las estaciones.
x=CoordenadasPlanas['X']
y=CoordenadasPlanas['Y']
N=CoordenadasPlanas['Estacion']

#Se imprime el dataframe de las estaciones con su respectivo código y nombre.
print('Los códigos de las estaciones seleccionadas para el llenado de datos faltantes son:' )
print(Estaciones)

#Se hace las espacialización de las estaciones.
fig, ax = plt.subplots(1, 1, figsize=(12, 12))
ax.plot(x,y,color='g',marker='o',linestyle=' ',label='Estaciones Seleccionadas')
ax.set_xlabel("Longitud")
ax.set_ylabel("Latitud")
ax.set_title('Ubicación de Estaciones Seleccionadas', pad = 20, fontdict={'fontsize':20, 'color': '#4873ab'})

#Se agrega el área de estudio en formato shape para un mejor análisis.
map_Zona=gdp.read_file('M:/Relleno_Sanitario_BGA/01_CART/02_SHP/01_BASE/Area_Estudio/Area_Est_60Km+Cuencas.shp')
map_Zona.plot(ax=ax, color='#89c0e8', zorder=0)

#Se hace la respectiva etiqueta de los códigos de las estaciones.
for i, txt in enumerate(N):
    plt.annotate(str(txt), (x[i],y[i]))

plt.legend(loc='upper right')
plt.show()

fig.savefig('03MapaEstacionesSelect.pdf')
fig.savefig('03MapaEstacionesSelect.jpg')

####################ESPACIALIZACIÓN DE LA ESTACIÓN ESCOGIDA####################

print('Los códigos de las estaciones seleccionadas para el llenado de datos faltantes son:' )
print(Estaciones)
print('¿Qué estación desea analizar? (Copie y pegue el código sin espacios)')
Estacion_Base=str(input())
Nombre_Estacion_Base=Estaciones.loc[Estacion_Base]['Nombre']

EstacionEstudio=pd.DataFrame(columns=['Estacion','X','Y'],dtype=float)
for m in range (0,len(CoordenadasPlanas)):
    if CoordenadasPlanas.loc[m,'Estacion']==Estacion_Base:
        EstacionEstudio.loc[m,'Estacion']=Estacion_Base
        EstacionEstudio.loc[m,'X']=CoordenadasPlanas.loc[m,'X']
        EstacionEstudio.loc[m,'Y']=CoordenadasPlanas.loc[m,'Y']
        
#Se generán las listas de las coordenadas y de los códigos de las estaciones.
x2=EstacionEstudio['X'].tolist()
y2=EstacionEstudio['Y'].tolist()
N2=EstacionEstudio['Estacion'].tolist()

EstacionesGrafica=pd.DataFrame(columns=['Estacion','X','Y'],dtype=float)
for n in range (0,len(EstacionesApoyo)):
    Estacion_Apoyo=EstacionesApoyo.loc[n,Estacion_Base]
    if Estacion_Apoyo==str(0):
        continue
    for m in range (0,len(CoordenadasPlanas)):
        if CoordenadasPlanas.loc[m,'Estacion']==Estacion_Apoyo:
            EstacionesGrafica.loc[m,'Estacion']=Estacion_Apoyo
            EstacionesGrafica.loc[m,'X']=CoordenadasPlanas.loc[m,'X']
            EstacionesGrafica.loc[m,'Y']=CoordenadasPlanas.loc[m,'Y']

#Se generán las listas de las coordenadas y de los códigos de las estaciones.
x3=EstacionesGrafica['X'].tolist()
y3=EstacionesGrafica['Y'].tolist()
N3=EstacionesGrafica['Estacion'].tolist()
     
#Se hace las espacialización de las estaciones.
fig, ax = plt.subplots(1, 1, figsize=(12, 12))
ax.plot(x,y,'m. ',label='Estaciones Lejanas')
ax.plot(x3,y3, 'sg ',label='Estaciones de Apoyo')
ax.plot(x2,y2,'yD ',label='Estación en Estudio')
ax.set_xlabel("Longitud")
ax.set_ylabel("Latitud")
ax.set_title(f'Estación en Estudio, {Nombre_Estacion_Base}', pad = 20, fontdict={'fontsize':20, 'color': '#4873ab'})
   
#Se agrega el área de estudio en formato shape para un mejor análisis.
map_Zona=gdp.read_file('M:/Relleno_Sanitario_BGA/01_CART/02_SHP/01_BASE/Area_Estudio/Area_Est_60Km+Cuencas.shp')
map_Zona.plot(ax=ax, color='#F5FFFA', zorder=0)

#Se hace la respectiva etiqueta de los códigos de las estaciones.
for i, txt in enumerate(N):
    plt.annotate(str(txt), (x[i],y[i]))

plt.legend(loc='upper right')
plt.show()
        
####################GRÁFICA DISTANCIAS vs Px/Pi DE LA ESTACIÓN ESCOGIDA####################

#Se hace el llenado de un nuevo dataframe con las distancias y la relación de precipitación para cada una de las estaciones.
DF_GraficaPvsD=pd.DataFrame(columns=['Estacion','Distancia','Relacion_Precipitacion'],dtype=float)
for n in range (0,len(Distancias)):
    DF_GraficaPvsD.loc[n,'Estacion']=Distancias.loc[n,'Estacion']
    DF_GraficaPvsD.loc[n,'Distancia']=Distancias.loc[n,Estacion_Base]
    DF_GraficaPvsD.loc[n,'Relacion_Precipitacion']=RelacionPrecip.loc[n,Estacion_Base]

#Se ordenan los valores de distancia de mayor a menor para una mejor visualización del gráfico.
DF_GraficaPvsD=DF_GraficaPvsD.sort_values(by=['Distancia'],ascending=[True])    
print(DF_GraficaPvsD)

#Se generán las listas de las distancias y relación de precipitación de las estaciones.
x=DF_GraficaPvsD['Distancia'].tolist()
y=DF_GraficaPvsD['Relacion_Precipitacion'].tolist()
N=DF_GraficaPvsD['Estacion'].tolist()

#Se hace el gráfico D vs Px/Pi.
fig, ax = plt.subplots(1, 1, figsize=(12, 12))
ax.plot(x,y,color='g',marker='o',linewidth=1,linestyle='--')
ax.set_xlabel("Distancia (km)")
ax.set_ylabel("Relacion Precipitacion Px/P")
ax.set_title(f"D vs Px/P de la estación, {Nombre_Estacion_Base}", pad = 20, fontdict={'fontsize':20, 'color': '#4873ab'})

#Se hace la respectiva etiqueta de los códigos de las estaciones.
for i, txt in enumerate(N):
    plt.annotate(str(txt), (x[i],y[i]))
print(f"D vs Px/P de la estación, {Nombre_Estacion_Base}")
plt.show()

