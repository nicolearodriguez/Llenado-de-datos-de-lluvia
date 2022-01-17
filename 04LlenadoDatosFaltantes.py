# -*- coding: utf-8 -*-
"""
Created on Tue Oct  8 15:57:18 2019

@author: nicole.rodriguez
LLENADO DE DATOS FALTANTES
1.Llenado de datos faltantes.
2.Calculo de las precipitaciones anuales en cada estación.
3.Calculo de la precipitacion media anual por estación.
"""

import pandas as pd
import math
import numpy as np

####################LECTURA DE DATOS####################

#Se ingresa el CSV de los datos de precipitación diaria de todas las estaciones a estudiar anteriormente reorganizado en insumos.
DF_PrecipitacionDiariaReorganizada=pd.read_csv('M:/Relleno_Sanitario_BGA/03_ESTUDIO UIS/08_GEOHIDRICO/16 Python/02Precipitación/01 Llenado de datos faltantes/02Insumos/02Precipitacion Diaria.csv')
DF_PrecipitacionDiariaReorganizada=DF_PrecipitacionDiariaReorganizada.infer_objects()
###DF_PrecipitacionDiariaReorganizada['date']=pd.to_datetime(DF_PrecipitacionDiariaReorganizada['date'])

#Se ingresan los valores de precipitación media anual obtenidos ya en los insumos.
DF_InsumoPrecipitacionMediaAnual=pd.read_csv('M:/Relleno_Sanitario_BGA/03_ESTUDIO UIS/08_GEOHIDRICO/16 Python/02Precipitación/01 Llenado de datos faltantes/02Insumos/02Precipitación_Media_Anual_NaN.csv')
DF_InsumoPrecipitacionMediaAnual["Estacion"]=DF_InsumoPrecipitacionMediaAnual["Estacion"].astype(str)
DF_InsumoPrecipitacionMediaAnual.set_index('Estacion',inplace=True)

#Se ingresa el csv con los valores de las distancias entre las estaciones obtenidas ya en los insumos.
DF_InsumoDistancias=pd.read_csv('M:/Relleno_Sanitario_BGA/03_ESTUDIO UIS/08_GEOHIDRICO/16 Python/02Precipitación/01 Llenado de datos faltantes/02Insumos/02DistanciasCondicion.csv')
DF_InsumoDistancias["Estacion"]=DF_InsumoDistancias["Estacion"].astype(str)

#Se ingresa el csv con los valores de los cuadrantes entre las estaciones obtenidas ya en los insumos.
CuadranteAngulo=pd.read_csv('M:/Relleno_Sanitario_BGA/03_ESTUDIO UIS/08_GEOHIDRICO/16 Python/02Precipitación/01 Llenado de datos faltantes/02Insumos/02CuadranteAngulo.csv')
CuadranteAngulo["Estacion"]=CuadranteAngulo["Estacion"].astype(str)
CuadranteAngulo.set_index('Estacion',inplace=True)

#DataFrame de las estaciones que se analizaran anterioremente seleccionadas en insumos.
DF_EstacionesEstudio=pd.read_csv('M:/Relleno_Sanitario_BGA/03_ESTUDIO UIS/08_GEOHIDRICO/16 Python/02Precipitación/01 Llenado de datos faltantes/02Insumos/02EstacionesLlenar.csv')
DF_EstacionesEstudio["Estacion"]=DF_EstacionesEstudio["Estacion"].astype(str)

#Dataframe de las precipitaciones anuales por estación.
DF_PrecipitacionAnual=pd.read_csv('M:/Relleno_Sanitario_BGA/03_ESTUDIO UIS/08_GEOHIDRICO/16 Python/02Precipitación/01 Llenado de datos faltantes/02Insumos/02Precipitacion Anual.csv')
DF_PrecipitacionAnual=DF_PrecipitacionAnual[['Año']]
DF_PrecipitacionAnual['Año']=DF_PrecipitacionAnual['Año'].astype(str)

####################LLENADO DE DATOS FALTANTES####################

#DataFrame que se llenará con los datos de precipitación faltantes.
DF_DatosDiarios=DF_PrecipitacionDiariaReorganizada
DF_DatosDiarios=DF_DatosDiarios[['date']]

for h in range (0,len(DF_EstacionesEstudio)): #len(DF_EstacionesEstudio)
    #Se define la estación en estudio
    Estacion_Base=DF_EstacionesEstudio.loc[h,'Estacion']
    print(f'{h} LA ESTACIÓN EN ESTUDIO ES: ',Estacion_Base)
    #Se ordenan las distancias de menor a mayor.
    DF_InsumoDistancias=DF_InsumoDistancias.sort_values(by=[Estacion_Base],ascending=[True])
    #Se remplantea el índice con el nuevo orden y se borra el anterior
    DF_InsumoDistancias.reset_index(level=0, inplace=True)
    DF_InsumoDistancias.drop(['index'],axis='columns',inplace=True)
    #Se extrae la precipitación media anual de la estación en estudio.
      #Px=Precipitación media anual en la estación en estudio.
    Px=DF_InsumoPrecipitacionMediaAnual.loc[Estacion_Base]['PrecipitacionMediaAnual']
    ###print('La precipitación media anual de la estación en estudio es: ',Px)
    for i in range (0,len(DF_PrecipitacionDiariaReorganizada)):
        if math.isnan(DF_PrecipitacionDiariaReorganizada.loc[i,Estacion_Base])==True:
            contador=0
            #Defino el dataframe de apoyo para llenar con (Px/Pi)*hpi
            DF_PrecipitacionFaltanteApoyo=pd.DataFrame(columns=['Estacion','Precipitacion Faltante'],dtype=float)
            #Con el fin de que hayan estacionesde apoyo en todos los cuadrantes, se tomarán estaciones por cuadrante análizados mediante un for de 1 a 4.
            for c in [1,2,3,4,1,2,3,4,1,2,3,4,1,2,3,4,1,2,3,4,1,2,3,4,1,2,3,4,1,2,3,4]: 
                ###print(c)
                for a in range(1,len(DF_InsumoDistancias)):
                    #Se determina la estación auxiliar cercana.
                    Estacion_Apoyo=DF_InsumoDistancias.loc[a,'Estacion']
                    ###print('El cuadrante es: ', CuadranteAngulo.loc[E][ES])
                    #Se define en que cuadrante está la estación escogida y si corresponde al cuadrate que necesito.
                    if c==CuadranteAngulo.loc[Estacion_Apoyo][Estacion_Base] and len(DF_PrecipitacionFaltanteApoyo[DF_PrecipitacionFaltanteApoyo['Estacion'].isin([Estacion_Apoyo])])==0:    
                        #Si la estación está en el cuadrante que necesito se hará el análisis con esta.
                        Estacion_Apoyo=Estacion_Apoyo
                        ###print('La estacion cercana es: ',E)
                    else:
                        #Si la estación está en un cuadrante diferente,se continua el for hasta encontrar alguna.
                        continue
                    #Se extrae la precipitación media anual de la estación auxiliar cercana.
                     #P=precipitación media anual en la estación auxiliar i.
                    P=DF_InsumoPrecipitacionMediaAnual.loc[Estacion_Apoyo]['PrecipitacionMediaAnual']
                    ###print('El valor de P es: ',P)
                    #Se extrae la altura de la precipitación registrada el día en cuestión en la estación auxiliar cercana.
                     #hp=Altura de precipitación registrada el día en cuestión en la estación auxiliar i.
                    hp=DF_PrecipitacionDiariaReorganizada.loc[i,Estacion_Apoyo]
                    ###print('El valor de hp: ',hp)
                    if math.isnan(hp)==True:
                        break
                    else:
                        contador=contador+1
                    #Se llena un nuevo dataframe con los valores de las estaciones cercanas análizadas.
                    DF_PrecipitacionFaltanteApoyo.loc[a,'Estacion']=Estacion_Apoyo
                    DF_PrecipitacionFaltanteApoyo.loc[a,'Precipitacion Faltante']=(Px/P)*hp
                    ###print('EL VALOR DE LA PRECIPITACIÓN ES: ',DF_PrecipitacionFaltanteApoyo.loc[a,'Precipitacion Faltante'])
                    break
                if contador==6:
                    break
            #Si llegado el caso no hay estaciones cercanas suficientes con valores de precipitación del día en cuestión, el resultado seguirá siedo NaN.
            if contador<2:
                DF_DatosDiarios.loc[i,Estacion_Base]=np.NaN    
                continue
            ###print('El numero de estaciones fueron: ',contador)
            ###print(DF_PrecipitacionFaltanteApoyo)
            #Se suman los valores de las estacones auxiliares.
            val=DF_PrecipitacionFaltanteApoyo['Precipitacion Faltante'].sum()
            ###print('La suma de las estaciones es: ',val)
            #Se aplica la formula para deducción de datos faltantes y así obtener la precipitación faltante diaria. 
            DF_DatosDiarios.loc[i,Estacion_Base]=(1/contador)*val
            ###print(DF_DatosDiarios.loc[i,ES])
        else:
            DF_DatosDiarios.loc[i,Estacion_Base]=DF_PrecipitacionDiariaReorganizada.loc[i,Estacion_Base]
            ###print('EL VALOR DE LA PRECIPITACIÓN TOTAL ES: ',DF_DatosDiarios.loc[i,ES])

print(DF_DatosDiarios)
DF_DatosDiarios.reset_index().to_csv('04Datos Faltantes_Nuevo.csv',header=True,index=False)

####################CALCULO DE LAS PRECIPITACIONES ANUALES DE CADA ESTACIÓN####################

PrecipitacionDiaria=pd.read_csv('04Datos Faltantes_Nuevo.csv')
DF_DatosDiarios["date"]=DF_DatosDiarios["date"].astype(str)

#Se calcularan las precipitaciones anuales para cada estación
for h in range (0,len(DF_EstacionesEstudio)): #len(DF_EstacionesEstudio)
    #Se define la estación en estudio
    Estacion_Base=DF_EstacionesEstudio.loc[h,'Estacion']
    ###print('LA ESTACIÓN EN ESTUDIO ES: ',ES)
    for k in range (0,len(DF_PrecipitacionAnual)):
        #Se determina el año de estudio
        A=DF_PrecipitacionAnual.loc[k,'Año']
        ###print('El año de estudio es :',A)       
        #Tomo los datos de precipitación del año de estudio
        DF_EstacionPorAño=DF_DatosDiarios[DF_DatosDiarios['date'].str.contains(A)]
        ###print(DF_EstacionPorAño)
        #Determino si aún hay datos nulos en el año cuántos hay
        nullo=sum(pd.isnull(DF_EstacionPorAño[Estacion_Base]))
        ###print('Los datos nulos del año son: ',nullo)
        if nullo==0:
            DF_PrecipitacionAnual.loc[k,Estacion_Base]=DF_EstacionPorAño[Estacion_Base].sum()
        else:
            DF_PrecipitacionAnual.loc[k,Estacion_Base]=np.NaN
        #En dado caso que la estación no tenga el año de estudio se reemplazará su precipitación anual por NaN
        if len(DF_EstacionPorAño)==0:
            DF_PrecipitacionAnual.loc[k,Estacion_Base]=np.NaN
        ###print('La precipitación es: ',DF_PrecipitacionAnual.loc[k,ES])
        #Exporto las precipitaciones por año por estación.
print(DF_PrecipitacionAnual)

####################CALCULO DE LA PRECIPITACIÓN MEDIA ANUAL DE CADA ESTACIÓN####################

#DF_PrecipitacionMediaAnual=pd.DataFrame(columns=['Estacion','PrecipitacionMediaAnual'],dtype=float)
for h in range (0,len(DF_EstacionesEstudio)): #len(DF_EstacionesEstudio)
    #Se define la estación en estudio
    Estacion_Base=DF_EstacionesEstudio.loc[h,'Estacion'] 
    #Se hace el promedio de las precipitaciones anuales de la estación en estudio
    DF_EstacionesEstudio.loc[h,'PrecipitacionMediaAnual']=DF_PrecipitacionAnual[Estacion_Base].mean()
DF_EstacionesEstudio=DF_EstacionesEstudio[['Estacion','X','Y','PrecipitacionMediaAnual']]

print(DF_EstacionesEstudio)
DF_EstacionesEstudio.reset_index().to_csv('04Precipitación_Media_Anual.csv',header=True,index=False)


