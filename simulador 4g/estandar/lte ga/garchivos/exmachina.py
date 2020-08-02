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
random.seed(0)
print("Cargando datos de coordenadas")
cord_x = np.loadtxt("ues_cord_x.txt")
cord_y = np.loadtxt("ues_cord_y.txt")
print("Cargando informacion de capacidad")
throughput_data = pd.read_excel('capacidad.xls')
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
time.sleep(1)
#tbs_tras=np.transpose(tbs[0])

#print(np.shape(cord_x))
#print(np.shape(cord_y))

#x = np.random.rand(equipos_terminales)
#y = np.random.rand(equipos_terminales)

# We want to minimize the distance so the weights have to be negative
#se busca maximizar el throughput, peso es positivo
creator.create("FitnessMax", base.Fitness, weights=(1.0,))
#  The individuals are just single integer (typecode='i') array of dimension 1xequipos_terminales
#  We also assign the creator.FitnessMax that was just created in the line above
creator.create("Individual", array.array, typecode='i', fitness=creator.FitnessMax)
toolbox = base.Toolbox()
# Attribute generator
toolbox.register("indices", random.choices, range(9), k=equipos_terminales )
# Structure initializers
toolbox.register("individual", tools.initIterate, creator.Individual, toolbox.indices)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)
toolbox.register("mate", tools.cxOrdered)
toolbox.register("mutate", tools.mutShuffleIndexes, indpb=0.05)
toolbox.register("select", tools.selTournament, tournsize=3)

def eval_Throughput(individual):
    recursos=np.sum(individual)
    print("prbs",recursos)
    #i: individual
    #for cromosoma in range(30):
        #j: celda
        #for celda in range(4):
            #o podría ser alreves
            #print(i,j)
    #throughput_data=data.iloc[tbs,individual]
    #throughput = np.sum(throughput_data)
    if recursos<90 or recursos>110 :
        throughput=throughput-0.3*throughput
    #evaluar los 10 valores de cada tbs de 4 celdas
    #comprar el individuo en la tabla de capacidad con tbs
    #evaluar thoruput, maximizar

    #sinr se convierte en un multiplicador que afecta el throuput, con 100%
    #el valor maximo de sinr. Es necesario procesar el resto de valores.
    return max,

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
    #time.sleep(10)
    return distance,

toolbox.register("evaluate", evalTSP)

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
