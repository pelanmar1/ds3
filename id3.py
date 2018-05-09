# -*- coding: utf-8 -*-

import pandas as pd
import math

# Leemos datos y los pasamos a un DataFrame
data = pd.read_csv('dataID3.csv',header=0)


def id3(tabla,indNodo=0):
    # Recibe un DataFrame con columnas (atr1,atr2,...,atr(n-1),clase)
    df = tabla.copy()
    indClase = df.shape[1]-1
    # Calculamos la entropia del sistema completo como referencia
    ref = calculaEntropia(df.iloc[:,indClase])
    atribs = [i for i in range(indClase)]
    # Calculamos las ganancias de cada atributo
    ganancias = calculaGanancias(df,atribs,indClase,ref)
    r=ganancias.index(max(ganancias))
    # El atributo que mas reduzca incertidumbre es seleccionado como nodo-decision
    print('NODO '+str(indNodo)+': ' + df.columns[r])
    # Calculamos las entropias de los valores del atributo nodo
    temp = calcEntropias(df, r, indClase)
    sigDf = None
    pendientes = []
    indActual = indNodo
    # Recorremos buscando decisiones sin incertidumbre (nodos-hoja)
    # o atributos aun por analizar
    for k,v in temp.items():
        if v[0]==0:
            print('- SI '+str(k) + ' => ' + str(v[1]))
        else:
            sigDf = (df.loc[df.iloc[:,r]==k])
            sigDf = sigDf.drop([df.columns[r]], axis=1)
            indActual +=1
            print('- SI ' + str(k) + ' => NODO '+str(indActual))
            pendientes.append((sigDf,indActual))
            
    # Analizamos atributos restantes recursivamente
    if sigDf is not None:
        for p in pendientes:    
            id3(p[0],p[1])
    else:
        return
    # Finalizamos cuando no resten atributos por analizar
    
def calculaGanancias(df,vals,indClase,ref):
    # Calcula las ganancias para los valores de columna dados
    ganancias = []
    for i in vals:
        temp = df.iloc[:,i]
        obj = calcEntropias(df, i, indClase,True)
        ent = ref
        for k,v in obj.items():
            ent-=v[0]
        ganancias.append(ent)
    return ganancias
    

def calculaEntropiaCol(col):
    # Calcula la entropia de una sola columna dada
    opciones = col.unique()
    numTotal = col.shape[0]
    numOpciones= opciones.shape[0]
    entropia = 0
    for i in range(numOpciones):
        temp = col.loc[col==opciones[i]]
        p = temp.shape[0]/numTotal
        entropia += -p*math.log(p)/math.log(2)
    return entropia

def calcEntropias(df, i, j,pon=False):
    # Calcula las entropias de los valores de la columna i con respecto 
    # a la clase j
    # Se regresa la entropia al separar por cada valor. Si la entropia es 0
    # se regresa la decision resultante (nodo hoja)
    p=1
    ref = df.iloc[:,j]
    col = df.iloc[:,i]
    numTotal = col.shape[0]
    opciones = col.unique()
    numOpciones= opciones.shape[0]
    res = {}
    for i in range(numOpciones):
        entropia = 0
        temp = df.loc[col==opciones[i]]
        d= None
        if pon == True:
            p = temp.shape[0]/numTotal
        e = calculaEntropia(temp.iloc[:,j])*p
        if (e == 0):
            d = temp.iloc[0,j]
        res[opciones[i]]=(e,d)
        
    return res


id3(data)


'''
OUTPUT >>
    
    NODO 0: Travel Cost
    - SI Cheap => NODO 1
    - SI Standard => Train
    - SI Expensive => Car
    NODO 1: Gender
    - SI Male => Bus
    - SI Female => NODO 2
    NODO 2: Car Ownership
    - SI 1 => Train
    - SI 0 => Bus
'''