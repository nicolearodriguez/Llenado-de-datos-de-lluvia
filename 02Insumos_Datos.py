# -*- coding: utf-8 -*-
"""
Created on Fri Oct 11 08:33:53 2019

@author: nicole.rodriguez

INSUMOS LLENADO DE DATOS FALTANTES.
1.Datos de precipítación anual y media anual de cada estación.
2.Distancias entre estaciones.
3.Compilar precipitaciones de varias estaciones en 1 dataframe.
4.Transformación a coordenadas planas y cálculo d ángulos entre las estaciones.
5.Cálculo de la relación de precipitación media anual entre las estaciones escogidas.
6.Selección de las estciones de apoyo según las condiciones de distancia y de relación de precipitación.
7.Selección de las estaciones que tienen suficientes estaciones de apoyo para hacer el llenado de datos faltantes.
8.Dataframe en el que se llenará la precipitación media anual.
9.Determinación del cuadrante en el que se encuentras las estaciones de apoyo de las estciones seleccionadas.
10.Determinación de la distancia entre las estaciones seleccionadas únicamente.
"""
"""VALORES QUE SE DEBEN INTRODUCIR:
    1.Intervalo de años a analizar. (Línea 30-31)
    2.Estaciones que desea analizar. (Línea 37-38)
    3.Rago de años que se tendran en cuenta para la precipitación media anual.(Línea 98)"""

import pandas as pd
import math
import numpy as np
from pyproj import Proj, transform 
 
#INTRODUZCA el intervalo de años a analizar en base al diagrama de calor de la cantidad de datos faltantes.
year1=1970 #
year2=2017 #
DF_PorAños=np.arange(year1,year2+1)
DF_PorAños=pd.DataFrame(DF_PorAños,columns=['Año'],dtype=str)

#INTRODUZCA los códigos de las estaciones que desea analizar en base al diagrama de calor de la cantidad de datos faltantes.

DF_Estaciones=[23190130,23190140,23190260,23190280,23190300,23190340,23190350,23190360,23190380,23190400,23190440
     ,23190460,23190590,23190600,23190700,23195090,23195110,23195200,24050100,24055030,24060050,24060070,37015020
     ,24060040,24060080,24050070] ##
DF_Estaciones=pd.DataFrame(DF_Estaciones,columns=['Estacion'],dtype=str)

####################LECTURA DE DATOS BASE####################

#Se lee el dataframe de los datos de precipitación previamente unidos.
DF_ValoresPrecipitacion=pd.read_csv('M:/Relleno_Sanitario_BGA/03_ESTUDIO UIS/08_GEOHIDRICO/16 Python/02Precipitación/01 Llenado de datos faltantes/00Valores de Precipitacion.csv')
DF_ValoresPrecipitacion=DF_ValoresPrecipitacion[['cod','date','valor']]
DF_ValoresPrecipitacion['cod']=DF_ValoresPrecipitacion['cod'].astype(str)
DF_ValoresPrecipitacion.set_index("cod",inplace=True)

#Se ingresas el csv con todas las estaciones del IDEAM descargado de la página http://www.ideam.gov.co/solicitud-de-informacion.
DF_IDEAM=pd.read_csv('M:/Relleno_Sanitario_BGA/03_ESTUDIO UIS/08_GEOHIDRICO/16 Python/02Precipitación/01 Llenado de datos faltantes/00CNE_IDEAM.csv',encoding='latin-1') ##VERIFICAR que el archivo este separado por comas y los números por puntos.
DF_IDEAM=DF_IDEAM[['CODIGO','nombre','ESTADO','altitud','latitud','longitud']]
DF_IDEAM['CODIGO']=DF_IDEAM['CODIGO'].astype(str)
            
####################DATOS DE PRECIPITACIÓN ANUAL####################

for i in range (0,len(DF_Estaciones)):###len(DF_Estaciones)
    #print(i)
    #Estación a analizar
    Estacion_Base=DF_Estaciones.loc[i,'Estacion']
    ##print('La estación en estudio es: ',E)
    #Separo las precipitaciones por estación
    DF_PrecipitacionPorEstacion=DF_ValoresPrecipitacion.loc[Estacion_Base]
    DF_PrecipitacionPorEstacion["date"]=DF_PrecipitacionPorEstacion["date"].astype(str)
    ###print(DF_PrecipitacionPorEstacion)
    #Determino cuántos datos nulos hay en la estación
    nullo=sum(pd.isnull(DF_PrecipitacionPorEstacion['valor']))
    ##print('Los datos nullos de la estación en estudio son: ',nullo)
    for k in range (0,len(DF_PorAños)):
        #Se determina el año de estudio
        Año=DF_PorAños.loc[k,'Año']
        ##print('El año de estudio es :',A)
        #Tomo los datos de precipitación del año de estudio
        DF_EstacionPorAño=DF_PrecipitacionPorEstacion[DF_PrecipitacionPorEstacion['date'].str.contains(Año)]
        ##print(DF_EstacionPorAño)
        #Determino cuántos datos nulos hay en el año año
        nullo=sum(pd.isnull(DF_EstacionPorAño['valor']))
        ##print('Los datos nulos del año son: ',nullo)
        if nullo==0:
            DF_PorAños.loc[k,Estacion_Base]=DF_EstacionPorAño['valor'].sum()
        else:
            DF_PorAños.loc[k,Estacion_Base]=np.NaN
        ##print(len(DF_EstacionPorAño))
        #En dado caso que la estación no tenga el año de estudio se reemplazará su precipitación anual por NaN
        if len(DF_EstacionPorAño)==0:
            DF_PorAños.loc[k,Estacion_Base]=np.NaN
        ##print('La precipitación es: ',DF_PorAños.loc[k,E])

print('DATOS DE PRECIPITACIÓN ANUAL')
print(DF_PorAños)
DF_PorAños.reset_index().to_csv('02Precipitacion Anual.csv',header=True,index=False)

####################DATOS DE PRECIPITACIÓN MEDIA ANUAL####################

DF_PorAños.set_index("Año",inplace=True)

#INTRODUZCA el rago de años que se tendran en cuenta para la precipitación media anual teniendo en cuenta 
 #que en algunas estaciones hay varios años con NaN
DF_PorAños=DF_PorAños.loc['1989':'1992']  ##
##print(DF_PorAños)

DF_PrecipitacionMediaAnual=pd.DataFrame(columns=['Estacion','PrecipitacionMediaAnual'],dtype=float)
for h in range (0,len(DF_Estaciones)): ###len(DF_Estaciones)
    #Se define la estación en estudio
    Estacion_Base=DF_Estaciones.loc[h,'Estacion'] 
    #Llenamos el dataframe con el código de la estación
    DF_PrecipitacionMediaAnual.loc[h,'Estacion']=Estacion_Base
    #Se cálcula el promedio de las precipitaciones anuales.
    DF_PrecipitacionMediaAnual.loc[h,'PrecipitacionMediaAnual']=DF_PorAños[Estacion_Base].mean()
 
DF_PrecipitacionMediaAnual['Estacion']=DF_PrecipitacionMediaAnual['Estacion'].astype(str)
print('DATOS DE PRECIPITACIÓN MEDIA ANUA')
print(DF_PrecipitacionMediaAnual)
DF_PrecipitacionMediaAnual.reset_index().to_csv('02Precipitación_Media_Anual_NaN.csv',header=True,index=False)

####################DISTANCIAS ENTRE LAS ESTACIONES####################

#DataFrame en el que se llenarán las distancias.
Distancias=pd.DataFrame(DF_Estaciones,columns=['Estacion'],dtype=str)

for h in range(0,len(DF_Estaciones)):
    #Se establece la estación base.
    Estacion_Base=DF_Estaciones.loc[h,'Estacion']
    for m in range (0,len(DF_IDEAM)):
        if DF_IDEAM.loc[m,'CODIGO']==Estacion_Base:
            #Se determina la langitud y la longitud de la estación base.
            long1=DF_IDEAM.loc[m,'longitud']
            lat1=DF_IDEAM.loc[m,'latitud']
            for t in range(0,len(DF_Estaciones)):
                #Se establece la estación de apoyo.
                Estacion_Apoyo=DF_Estaciones.loc[t,'Estacion']
                for k in range(0,len(DF_IDEAM)):
                    if DF_IDEAM.loc[k,'CODIGO']==Estacion_Apoyo:
                        #Se determina la longitud y la latitud de la estación de apoyo.
                        long2=DF_IDEAM.loc[k,'longitud']
                        lat2=DF_IDEAM.loc[k,'latitud']
                        r=6371 #Radio terrestre medio en kilometros.
                        c=math.pi/180 #Constante para transformar grados en radianes
                        #Fórmula de Haversine
                        Distancias.loc[t,Estacion_Base]=2*r*math.asin(math.sqrt((math.sin(c*(lat2-lat1)/2))**2+math.cos(c*lat1)*math.cos(c*lat2)*(math.sin(c*(long2-long1)/2))**2))
                        break

print('DISTANCIAS ENTRE LAS ESTACIONES')
print(Distancias)
Distancias.reset_index().to_csv('02Distancias.csv',header=True,index=False)

####################REORGANIZACIÓN DE DATOS DIARIOS DE PRECIPITACIÓN####################

from datetime import datetime, timedelta
inicio = datetime(year1,1,1) #%Y-%m-%d
inicio1 = str(inicio.strftime("%Y-%m-%d"))
fin   = datetime(year2,12,31) #%Y-%m-%d
fin1 = str(fin.strftime("%Y-%m-%d"))
DF_DatosPrecipitacionDiaria= [(inicio + timedelta(days=d)).strftime("%Y-%m-%d")
                    for d in range((fin - inicio).days + 1)] 
DF_DatosPrecipitacionDiaria=pd.DataFrame(DF_DatosPrecipitacionDiaria,columns=['date'],dtype=str)
DF_DatosPrecipitacionDiaria.set_index('date',inplace=True)
###print(DF_DatosPrecipitacionDiaria)

for i in range (0,len(DF_Estaciones)): ###len(DF_Estaciones)
    ###print(i)
    #Estación a analizar
    Estacion_Base=DF_Estaciones.loc[i,'Estacion']
    ###print(f'{i} La estación en estudio es: ',E)
    #Separo las precipitaciones por estación
    DF_Estaciones_Organizacion=DF_ValoresPrecipitacion.loc[Estacion_Base]
    DF_Estaciones_Organizacion.reset_index(level=0, inplace=True)
    DF_Estaciones_Organizacion.set_index("date",inplace=True)
    #Selecciono el rango de fechas de mi interes.
    DF_Estaciones_Organizacion=DF_Estaciones_Organizacion.loc[inicio1:fin1]
    DF_Estaciones_Organizacion.reset_index(level=0, inplace=True)
    #DF_Estaciones_Organizacion.set_index('date',inplace=True)
    DF_DatosPrecipitacionDiaria[Estacion_Base] = np.NaN
    for j in range (0,len(DF_Estaciones_Organizacion)): ###len(DF_Estaciones_Organizacion)
        #Selecciono la fecha en la cual tego datos de precipitación.
        date=DF_Estaciones_Organizacion.loc[j,'date']
        DF_Estaciones_Organizacion.set_index('date',inplace=True)
        #Leo la precipitación correspondiente a la fecha
        Precip=DF_Estaciones_Organizacion.loc[date]['valor']
        #Lleno el nuevo datframe con la precipitación en la fecha correspondiente.
        DF_DatosPrecipitacionDiaria.loc[date][Estacion_Base]=Precip
        DF_Estaciones_Organizacion.reset_index(level=0, inplace=True)
        #DF_DatosPrecipLlenar.loc[[date],[E]] = Precip
        #DF_DatosPrecipitacionDiaria[DF_DatosPrecipitacionDiaria['date']==date][E] = Precip

DF_DatosPrecipitacionDiaria.reset_index(level=0, inplace=True)

print('REORGANIZACIÓN DE DATOS DIARIOS DE PRECIPITACIÓN')
print(DF_DatosPrecipitacionDiaria)
DF_DatosPrecipitacionDiaria.reset_index().to_csv('02Precipitacion Diaria.csv',header=True,index=False)
      
####################COORDENADAS PLANAS####################

DF_IDEAMPlanas=pd.DataFrame(DF_Estaciones,columns=['Estacion'],dtype=str)

#Se ingresas el csv con las coordenadas de las estaciones.

for h in range(0,len(DF_Estaciones)):
    #Se establece la estación base.
    Estacion_Base=DF_Estaciones.loc[h,'Estacion']
    for m in range (0,len(DF_IDEAM)):
        if DF_IDEAM.loc[m,'CODIGO']==Estacion_Base:
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

print('COORDENADAS PLANAS')                   
print(DF_IDEAMPlanas)
DF_IDEAMPlanas.reset_index().to_csv('02CoordenadasPlanas.csv',header=True,index=False)

####################ANGULOS ENTRE LAS ESTACIONES####################

Angulo=0
for h in range(0,len(DF_IDEAMPlanas)):
    #Se establece la estación base.
    Estacion_Base=DF_IDEAMPlanas.loc[h,'Estacion']
    #Coordenadas planas de la estación base.
    X1=DF_IDEAMPlanas.loc[h,'X']
    Y1=DF_IDEAMPlanas.loc[h,'Y']
    for t in range(0,len(DF_IDEAMPlanas)):
        #Se establece la otra estación.
        Estacion_Apoyo=DF_IDEAMPlanas.loc[t,'Estacion']
        for k in range(0,len(DF_IDEAMPlanas)):
            if DF_IDEAMPlanas.loc[k,'Estacion']==Estacion_Apoyo:
                #Coordenadas planas de la estación de apoyo.
                X2=DF_IDEAMPlanas.loc[k,'X']
                Y2=DF_IDEAMPlanas.loc[k,'Y']
                #Se calcula el delta X y delta Y entre las estaciones.
                dx=X2-X1
                dy=Y2-Y1
                #Se hace el calculo del azimut entre la proyección de la estación base a la estación de apoyo.
                if dx>0 and dy>0: 
                    Angulo=math.atan(dx/dy)
                elif dx>=0 and dy<0:
                    Angulo=(math.pi*0.5)+math.atan(dy/dx)
                elif dx<0 and dy<0:
                    Angulo=(math.pi)+math.atan(dx/dy)
                elif dx<0 and dy>=0:
                    Angulo=(math.pi*1.5)+math.atan(dy/dx)
                else:
                    Angulo=0
            DF_IDEAMPlanas.loc[t,Estacion_Base]=Angulo  

print('ANGULOS EN RADIANES ENTRE LAS ESTACIONES')                              
print(DF_IDEAMPlanas)
#DF_IDEAMPlanas.reset_index().to_csv('Angulos.csv',header=True,index=False)
 
####################RELACIÓN DE LA PRECIPITACIÓN####################

DF_PrecipitacionMediaAnual.set_index('Estacion',inplace=True)
RelacionPrecipitacion=pd.DataFrame(DF_Estaciones,columns=['Estacion'],dtype=str)

for h in range(0,len(DF_Estaciones)):
    #Se establece la estación base.
    Estacion_Base=DF_Estaciones.loc[h,'Estacion']
    #Precipitación media anual de la estación base.
    Px=DF_PrecipitacionMediaAnual.loc[Estacion_Base]['PrecipitacionMediaAnual']
    for t in range(0,len(DF_Estaciones)):
        #Se establece la otra estación.
        Estacion_Apoyo=DF_Estaciones.loc[t,'Estacion']
        #Precipitación media anual de la estación de apoyo.
        P=DF_PrecipitacionMediaAnual.loc[Estacion_Apoyo]['PrecipitacionMediaAnual']
        #Se hace la relación de las precipitaciones.
        RelacionPrecipitacion.loc[t,Estacion_Base]=Px/P

print('RELACIÓN DE LA PRECIPITACIÓN') 
print(RelacionPrecipitacion)
RelacionPrecipitacion.reset_index().to_csv('02RelacionPrecipitacion.csv',header=True,index=False)

####################CONDICIONES PARA LAS ESTACIONES DE APOYO####################

RelacionPrecipitacion.set_index('Estacion',inplace=True)
Distancias.set_index('Estacion',inplace=True)
DF_EstacionesApoyo=pd.DataFrame(DF_Estaciones,columns=['Estacion'],dtype=str)

for h in range(0,len(DF_Estaciones)):
    #Se establece la estación base.
    Estacion_Base=DF_Estaciones.loc[h,'Estacion']
    for n in range(0,len(DF_Estaciones)):
        #Se establece la estación de apoyo
        Estacion_Apoyo=DF_Estaciones.loc[n,'Estacion']
        #Se condiciona a que la distancia entre la estación base y la estación de apoyo sea menor a 30 km, además de que su relación de precipitación oscile entre 0.7 y 1.4.
        if 0.7<=RelacionPrecipitacion.loc[Estacion_Apoyo][Estacion_Base]<=1.4 and Distancias.loc[Estacion_Apoyo][Estacion_Base]<=30:
            DF_EstacionesApoyo.loc[n,Estacion_Base]=Estacion_Apoyo
    #Si no se tienen suficientes estaciones para el análisis, se extiende la condición de la relación de precipitación entre 0.6 y 1.5.
    if sum(pd.notna(DF_EstacionesApoyo[Estacion_Base]))<4:
        for f in range(0,len(DF_Estaciones)):
            Estacion_Apoyo=DF_Estaciones.loc[f,'Estacion']
            if 0.6<=RelacionPrecipitacion.loc[Estacion_Apoyo][Estacion_Base]<=1.5 and Distancias.loc[Estacion_Apoyo][Estacion_Base]<=30:
                DF_EstacionesApoyo.loc[f,Estacion_Base]=Estacion_Apoyo

##print(DF_EstacionesApoyo)
DF_EstacionesApoyo.reset_index().to_csv('02EstacionesApoyoAntes.csv',header=True,index=False)         
for h in range(0,len(DF_Estaciones)):
    #Se establece la estación base.
    Estacion_Base=DF_Estaciones.loc[h,'Estacion']
    #Si la estación base tiene menos de 3 estaciones de apoyo (incluyendose la estación base) se elimina de la lista de estaciones a análizar
     #pues no se cuenta con suficientes estaciones para su análiis.
    if sum(pd.notnull(DF_EstacionesApoyo[Estacion_Base]))<3:
        DF_EstacionesApoyo.drop([Estacion_Base],axis='columns',inplace=True)

DF_EstacionesApoyo.drop(['Estacion'],axis='columns',inplace=True)
#print(DF_EstacionesApoyo)
DF_EstacionesApoyo.reset_index().to_csv('02EstacionesApoyo.csv',header=True,index=False)

####################ESTACIONES SELECCIONADAS####################

EstacionesSelect=list(DF_EstacionesApoyo)
EstacionesSelect=pd.DataFrame(EstacionesSelect,columns=['Estacion'],dtype=str)
for n in range (0,len(EstacionesSelect)):
    #Determinamos la estación base.
    Estacion_Base=EstacionesSelect.loc[n,'Estacion']
    for m in range (0,len(DF_IDEAM)):
        if DF_IDEAM.loc[m,'CODIGO']==Estacion_Base:
            #Llenamos el dataframe con el nombre y el estado actual de la estación base proporcionado por el IDEAM.
            EstacionesSelect.loc[n,'Nombre']=DF_IDEAM.loc[m,'nombre']
            EstacionesSelect.loc[n,'Estado']=DF_IDEAM.loc[m,'ESTADO']


###print(EstacionesSelect)
EstacionesSelect.reset_index().to_csv('02EstacionesSelect.csv',header=True,index=False)

####################DATAFRAME PARA LLENAR LA PRECIPITACIÓN MEDIA ANUAL####################

for n in range (0,len(EstacionesSelect)):
    #Se establece la estación base.
    Estacion_Base=EstacionesSelect.loc[n,'Estacion']
    for m in range (0,len(DF_IDEAMPlanas)):
        if DF_IDEAMPlanas.loc[m,'Estacion']==Estacion_Base:
            #Se llena el dataframe con las coordenadas de la estación para su posterior espacialización.
            EstacionesSelect.loc[n,'X']=DF_IDEAMPlanas.loc[m,'X']
            EstacionesSelect.loc[n,'Y']=DF_IDEAMPlanas.loc[m,'Y']

print('ESTACIONES SELECCIONADAS')
print(EstacionesSelect)
EstacionesSelect.reset_index().to_csv('02EstacionesLlenar.csv',header=True,index=False)

####################CUADRANTE DE LAS ESTACIONES ESCOGIDAS EN BASE A LA CONDICIÓN####################

DF_IDEAMPlanas["Estacion"]=DF_IDEAMPlanas["Estacion"].astype(str)
DF_IDEAMPlanas.set_index('Estacion',inplace=True)
DF_EstacionesLlenarCuadrante=pd.DataFrame(DF_Estaciones,columns=['Estacion'],dtype=str)

for h in range(0,len(EstacionesSelect)):
    #Se establece la estación base.
    Estacion_Base=EstacionesSelect.loc[h,'Estacion']
    for n in range(0,len(DF_EstacionesApoyo)):
        #Estación de apoyo.
        Estacion_Apoyo=DF_EstacionesApoyo.loc[n,Estacion_Base]
        #Si Estacion_Apoyo no es una estación de apoyo para ES se llenará con NaN.
        if pd.isnull(Estacion_Apoyo)==True:
            DF_EstacionesLlenarCuadrante.loc[n,Estacion_Base]=np.NaN
            continue
        #Si Estacion_Apoyo si es una estación de apoyo, se determina el cuadrante en el que se encuentra la estación de apoyo respecto a la estación base.
        if 0<=DF_IDEAMPlanas.loc[Estacion_Apoyo][Estacion_Base]<(math.pi/2):
            DF_EstacionesLlenarCuadrante.loc[n,Estacion_Base]=1
        elif (math.pi/2)<=DF_IDEAMPlanas.loc[Estacion_Apoyo][Estacion_Base]<(math.pi):
            DF_EstacionesLlenarCuadrante.loc[n,Estacion_Base]=2
        elif (math.pi)<=DF_IDEAMPlanas.loc[Estacion_Apoyo][Estacion_Base]<(math.pi*1.5):
            DF_EstacionesLlenarCuadrante.loc[n,Estacion_Base]=3
        elif (math.pi*1.5)<=DF_IDEAMPlanas.loc[Estacion_Apoyo][Estacion_Base]<=(math.pi*2):
            DF_EstacionesLlenarCuadrante.loc[n,Estacion_Base]=4
        else:
            DF_EstacionesLlenarCuadrante.loc[n,Estacion_Base]=np.NaN 

#print(DF_EstacionesLlenarCuadrante)
DF_EstacionesLlenarCuadrante.reset_index().to_csv('02CuadranteAngulo.csv',header=True,index=False)   

####################DISTANCIA DE LAS ESTACIONES ESCOGIDAS EN BASE A LA CONDICIÓN####################

Distancias.reset_index(level=0, inplace=True)
DF_EstacionesLlenarDistancia=pd.DataFrame(DF_Estaciones,columns=['Estacion'],dtype=str)

for h in range(0,len(EstacionesSelect)):
    #Se establece la estación base.
    Estacion_Base=EstacionesSelect.loc[h,'Estacion']
    for n in range(0,len(DF_EstacionesApoyo)):
        #Estación de apoyo.
        Estacion_Apoyo=DF_EstacionesApoyo.loc[n,Estacion_Base]
        #Si Estacion_Apoyo no es una estación de apoyo para ES se llenará con NaN.
        if pd.isnull(Estacion_Apoyo)==True:
            DF_EstacionesLlenarDistancia.loc[n,Estacion_Base]=np.NaN
            continue
        #Si Estacion_Apoyo si es una estación de apoyo, se llena el datframe con la distancia correspondiente entre la estación base y la estación de apoyo..
        DF_EstacionesLlenarDistancia.loc[n,Estacion_Base]=Distancias.loc[n,Estacion_Base]
         
###print(DF_EstacionesLlenarDistancia)
DF_EstacionesLlenarDistancia.reset_index().to_csv('02DistanciasCondicion.csv',header=True,index=False) 






















