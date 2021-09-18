# Kling, Ronn. Learning DEAP from examples.
'''Test bench cumple su funcion, pero se descarta: Al implementar el multiplicador sinr se encuentra
que la funcion de evaluacion solo tiene en cuenta un individuo (conjunto de bloques de recursos) para todo el
sistema cuando en realidad seria para cada celda. El resultado de este algoritmo debe ser por 
celda, cuatro iteraciones resulta en el algoritmo final, para la capacidad del sistema de 4 celdas.'''
#Se crea un nuevo testbench con las siguientes caractersiticas:
    #throughput30 vuelve a ser de (30,1) tbs
    #tbs vuelve a ser de (30,1)
    #los calculos se realizan en la celda 0
import matplotlib.pyplot as plt
import sys
import array
import random
import numpy as np
import pandas as pd
from deap import algorithms, base, creator, tools
import time
import math

#funciones de prueba
def eval_throughput(individual, throughput30, tbs_run1t, capacidad_data, sinr_run1t):
    recursos=np.sum(individual)
    #print("prbs",recursos)
    #i: individual
    for celda in range(4):
        #j: celda
        for cromosoma in range(30):
            #print("tbs->",int(tbs_run1t[celda][cromosoma]))
            #print("ind->",individual[cromosoma])
            print("-----")
            throughput30[celda][cromosoma] = int(capacidad_data.iloc[int(tbs_run1t[celda][cromosoma])+1,individual[cromosoma]])
            print(throughput30[celda][cromosoma])
            print("----")
            #time.sleep(1)
            #print(np.shape(throughput30), "total celda ",celda, " : ", np.sum(throughput30[celda]))
    print("matriz throughput")
    print(throughput30)
    #a=np.sum(throughput30[0])
    #b=np.sum(throughput30[1])
    #c=np.sum(throughput30[2])
    #d=np.sum(throughput30[3])
    #print("celda 1")
    #print(a)
    #print("celda 2")
    #print(b)
    #print("celda 3")
    #print(c)
    #print("celda 4")
    #print(d)
    #print("suma total: ", a+b+c+d )
            #print(throughput30[celda][cromosoma])
            #print(celda, cromosoma)
            #time.sleep(0.5)
    #throughput_data=capacidad_data.iloc[tbs,individual]
    #throughput = np.sum(throughput_data)

    #se ajusta el snr a valores de porcentaje: el mayor =100, el resto se ajusta en realcion al mayor.
    #ahora se ajusta el throughput con la penalizacion de sinr.
    #luego se penaliza los recursos segun el throughput

    throughput=np.sum(throughput30)
    print("prbs",recursos)
    if recursos<90 or recursos>110 :
        throughput=throughput-0.3*throughput
    #evaluar los 10 valores de cada tbs de 4 celdas
    #comprar el individuo en la tabla de capacidad con tbs
    #evaluar thoruput, maximizar
    print(throughput) #este esta alterado por la penalizacion.
    #sinr se convierte en un multiplicador que afecta el throuput, con 100%
    #el valor maximo de sinr. Es necesario procesar el resto de valores.
    return throughput,

#procesamiento de multiplicador sinr.
def multiplicador_sinr(sinr_run1t):
    '''Convertierne una matriz con valores sirn de equipos terminales, en una matriz
    de porcentajes respecto al maximo de la matriz.'''
    print("multiplicador sinr")
    print(sinr_run1t[0])

    print("maximo celda 0: ",np.max(sinr_run1t[0]))
    print("maximo celda 1: ",np.max(sinr_run1t[1]))
    print("maximo celda 2: ",np.max(sinr_run1t[2]))
    print("maximo celda 3: ",np.max(sinr_run1t[3]))
    print("---")
    print("maximo sistema: ",np.max(sinr_run1t))


def main():
    pass


if __name__ == "__main__":
    equipos_terminales = 30
    rangos=10
    random.seed(0)
    print("Cargando datos de coordenadas")
    cord_x = np.loadtxt("ues_cord_x.txt")
    cord_y = np.loadtxt("ues_cord_y.txt")
    print("Cargando informacion de capacidad")
    capacidad_data = pd.read_excel('capacidad.xls')
    print("Cargando información de tbs y snr")
    tbs = [np.loadtxt('garchivos/run1/tbs1.txt'), np.loadtxt('garchivos/run1/tbs2.txt'), np.loadtxt('garchivos/run1/tbs3.txt'), 
    np.loadtxt('garchivos/run1/tbs4.txt'), np.loadtxt('garchivos/run1/tbs5.txt'), np.loadtxt('garchivos/run1/tbs6.txt'), 
    np.loadtxt('garchivos/run1/tbs7.txt'), np.loadtxt('garchivos/run1/tbs8.txt'), np.loadtxt('garchivos/run1/tbs9.txt'),
    np.loadtxt('garchivos/run1/tbs10.txt')]

    sinr = [np.loadtxt('garchivos/run1/snr1.txt'), np.loadtxt('garchivos/run1/snr2.txt'), np.loadtxt('garchivos/run1/snr3.txt'), 
    np.loadtxt('garchivos/run1/snr4.txt'), np.loadtxt('garchivos/run1/snr5.txt'), np.loadtxt('garchivos/run1/snr6.txt'), 
    np.loadtxt('garchivos/run1/snr7.txt'), np.loadtxt('garchivos/run1/snr8.txt'), np.loadtxt('garchivos/run1/snr9.txt'),
    np.loadtxt('garchivos/run1/snr10.txt')]
    print("Carga ok ...ajustando variables")
    #ajuste de variables
    tbs_run1=tbs[0]
    tbs_run1t=np.transpose(tbs_run1)
    sinr_run1 = sinr[0]
    sinr_run1t =np.transpose(sinr_run1)
    #definicion de coordenadas x,y
    x=cord_x
    y=cord_y
    #definicion de matriz de throughtput
    throughput30=np.zeros((4,30))

    #time.sleep(1)
    #muestra de cromosomas del individuo, no aplica. Generación aleatoria.
    individual=random.choices(range(9),k=30)
    print(individual)

    
    #print("304: ",throughput30[2][24])
    #print(eval_throughput(individual,throughput30, tbs_run1t, capacidad_data, sinr_run1t))


    multiplicador_sinr(sinr_run1t)
else:
    print("modulo test importado")