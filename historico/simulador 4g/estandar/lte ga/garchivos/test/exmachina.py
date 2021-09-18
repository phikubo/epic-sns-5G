# Kling, Ronn. Learning DEAP from examples.

import matplotlib.pyplot as plt
import sys
import array
import random
import numpy as np
import pandas as pd
from deap import algorithms, base, creator, tools
import time
import math

equipos_terminales = 30
rangos=10
celda=0
random.seed(0)
#
print("Cargando datos de coordenadas")
cord_x = np.loadtxt("ues_cord_x.txt")
cord_y = np.loadtxt("ues_cord_y.txt")
#
print("Cargando informacion de capacidad")
capacidad_data = pd.read_excel('capacidad.xls')
#
print("Cargando información de tbs y snr")
tbs = [np.loadtxt('garchivos/run1/tbs1.txt'), np.loadtxt('garchivos/run1/tbs2.txt'), np.loadtxt('garchivos/run1/tbs3.txt'), 
np.loadtxt('garchivos/run1/tbs4.txt'), np.loadtxt('garchivos/run1/tbs5.txt'), np.loadtxt('garchivos/run1/tbs6.txt'), 
np.loadtxt('garchivos/run1/tbs7.txt'), np.loadtxt('garchivos/run1/tbs8.txt'), np.loadtxt('garchivos/run1/tbs9.txt'),
np.loadtxt('garchivos/run1/tbs10.txt')]
##
sinr = [np.loadtxt('garchivos/run1/snr1.txt'), np.loadtxt('garchivos/run1/snr2.txt'), np.loadtxt('garchivos/run1/snr3.txt'), 
np.loadtxt('garchivos/run1/snr4.txt'), np.loadtxt('garchivos/run1/snr5.txt'), np.loadtxt('garchivos/run1/snr6.txt'), 
np.loadtxt('garchivos/run1/snr7.txt'), np.loadtxt('garchivos/run1/snr8.txt'), np.loadtxt('garchivos/run1/snr9.txt'),
np.loadtxt('garchivos/run1/snr10.txt')]
#
#ajuste de variables
print("Carga ok ...ajustando variables")
tbs_run1=tbs[0]
tbs_run1t=np.transpose(tbs_run1)
sinr_run1 = sinr[0]
sinr_run1t =np.transpose(sinr_run1)
#definicion de coordenadas x,y
x=cord_x
y=cord_y
#otras variables
maximo = np.max(sinr_run1t[celda])
minimo = np.min(sinr_run1t[celda])
#
multplicador = (sinr_run1t[celda]-minimo)/maximo
#
throughput30=np.zeros(30)
#
#se busca maximizar el throughput, peso es positivo
creator.create("FitnessMax", base.Fitness, weights=(1.0,))
#  The individuals are just single integer (typecode='i') array of dimension 1xequipos_terminales
#  We also assign the creator.FitnessMax that was just created in the line above
creator.create("Individual", array.array, typecode='i', fitness=creator.FitnessMax)
toolbox = base.Toolbox()
# Attribute generator
#register(<nombre>, funcion de probabilidad,distribucion, parametro1, parameetro2, etc.)
toolbox.register("indices", random.choices, range(9), k=equipos_terminales )
# Structure initializers
toolbox.register("individual", tools.initIterate, creator.Individual, toolbox.indices)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)
toolbox.register("mate", tools.cxOrdered)
toolbox.register("mutate", tools.mutShuffleIndexes, indpb=0.05)
toolbox.register("select", tools.selTournament, tournsize=3)



def eval_Throughput(individual):
    recursos=np.sum(individual)

    #print("prbs",recursos)
    for cromosoma in range(30):
        throughput30[cromosoma] = int(capacidad_data.iloc[int(tbs_run1t[celda][cromosoma])+1,individual[cromosoma]])
    
    #for cromosoma in range(30):
        #sin 1-multplicador, genera valores de throughput negativo, eso no es posible.
        #sin embargo en la suma, estos valores se compensan
    #    throughput30[cromosoma]=int(math.floor( throughput30[cromosoma]*(multiplicador[cromosoma] )))
    
    throughput=np.sum(throughput30)
    if recursos>110 :
        throughput=throughput-0.3*throughput
    print("recursos: ",recursos)
    return throughput

def evalTSP(individual):
    print("----------->individuo", individual)
    print("----------->gen: ", individual[0], individual[1])
    #print("tipo: ", type(individual))
    recursos=np.sum(individual)
    print("suma:" , np.sum(individual))
    #print("coordenadas de individuos")
    #print(x[individual])
    #print(">>>>end")
    diffx = np.diff(x[individual])
    diffy = np.diff(y[individual])
    distance = np.sum(diffx**2 + diffy**2)
    print("suma1: ", distance)
    #ajuste de tamaño de cadena de acuerdo a la maximizacion de distancia
    if np.sum(individual)>100:
        distance=distance-2*distance
    print("suma2: ",distance)
    time.sleep(10)
    return distance,

toolbox.register("evaluate", eval_Throughput)

#toolbox.register("evaluate", eval_Throughput)


def main():
    #start with a population of 300 individuals
    pop = toolbox.population(n=300)
    #only save the very best one
    hof = tools.HallOfFame(1)
    stats = tools.Statistics(lambda ind: ind.fitness.values)
    stats.register("avg", np.mean)
    stats.register("std", np.std)
    stats.register("min", np.min)
    stats.register("max", np.max)
    # use one of the built in GA's with a probablilty of mating of 0.7
    # a probability of mutating 0.2 and 140 generations.
    algorithms.eaSimple(pop, toolbox, 0.7, 0.1, 100, stats=stats, halloffame=hof)

    return pop, stats, hof


if __name__ == "__main__":
    print("Coordinate x", "\t", "Coordinate y")
    for xi, yi in zip(x, y):
        print( xi, "\t", yi)
    plt.plot(x, y, 'o', color='black')
    pop, stats, hof = main()
    # plot the best one
    ind = hof[0]
    print ("Solution: ", ind)
    plt.figure(2)
    plt.plot(x[ind], y[ind])
    plt.show()
    # raw_input("Press any key to continue.")
