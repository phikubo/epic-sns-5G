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
celda=0
random.seed(0)
#
print("Cargando datos de coordenadas")
cord_x = np.loadtxt("ues_cord_x.txt")
cord_y = np.loadtxt("ues_cord_y.txt")
#

#
#ajuste de variables


#
#se busca maximizar el throughput, peso es positivo





def main(celda, tbs, sinr, capacidad_data):
    print("Carga ok ...ajustando variables")
    tbs_run1=tbs[celda]
    tbs_run1t=np.transpose(tbs_run1)
    sinr_run1 = sinr[celda]
    sinr_run1t =np.transpose(sinr_run1)

    #otras variables
    maximo = np.max(sinr_run1t[celda])
    minimo = np.min(sinr_run1t[celda])
    #
    multiplicador = (sinr_run1t[celda]-minimo)/maximo
    #
    throughput30=np.zeros(30)
    #

    def eval_Throughput(individual):
        for cromosoma in range(30):
            throughput30[cromosoma] = int(capacidad_data.iloc[int(tbs_run1t[celda][cromosoma])+1,individual[cromosoma]])

        for cromosoma in range(30):

            throughput30[cromosoma]=throughput30[cromosoma]*(multiplicador[cromosoma] )
    
        throughput=np.sum(throughput30)
        recursos=np.sum(individual)
        thinit=throughput
    #maximo, 0,8 y 0.45
        if recursos>100:
            throughput=throughput-0.81*throughput
        if np.count_nonzero(individual)!=29:
            throughput=throughput-0.56*throughput
        return throughput,   
    #
    creator.create("FitnessMax", base.Fitness, weights=(1.0,))
    creator.create("Individual", array.array, typecode='i', fitness=creator.FitnessMax)
    toolbox = base.Toolbox()
    toolbox.register("indices", random.choices, range(9), k=equipos_terminales )

    toolbox.register("individual", tools.initIterate, creator.Individual, toolbox.indices)
    toolbox.register("population", tools.initRepeat, list, toolbox.individual)
    toolbox.register("mate", tools.cxOrdered)
    toolbox.register("mutate", tools.mutShuffleIndexes, indpb=0.09) #antes 0.05
    toolbox.register("select", tools.selTournament, tournsize=5)
    #
    toolbox.register("evaluate", eval_Throughput)


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
    algorithms.eaSimple(pop, toolbox, 0.7, 0.2, 200, stats=stats, halloffame=hof) #antes 0.1

    return pop, stats, hof


if __name__ == "__main__":
    print("Exmachina says: Welcome!")
    #
    ganadores=[]
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
    #definicion de coordenadas x,y
    x=cord_x
    y=cord_y
    plt.plot(x, y, 'o', color='green')
    #pop, stats, hof = main(celda, tbs, sinr, capacidad_data)
    # plot the best one
    #ind = hof[0]
    #print ("Solution: ", ind, "prbs: ", np.sum(ind), "forma ", np.shape(ind))

    for celda in range(4):
        print("Interacion: ",celda+1)
        pop, stats, hof = main(celda, tbs, sinr, capacidad_data)
        ind = hof[0]
        print ("Solution: ", ind, "prbs: ", np.sum(ind), "forma ", np.shape(ind))
        ganadores.append(ind)
    
    #ganadores1=np.transpose(ganadores[0])
    #ganadores2=np.transpose(ganadores[1])
    #ganadores3=np.transpose(ganadores[2])
    #ganadores4=np.transpose(ganadores[3])
    ganadores=np.transpose(ganadores)
    #np.savetxt('gandadores1.txt', ganadores1 )
    #np.savetxt('gandadores2.txt', ganadores2 )
    #np.savetxt('gandadores3.txt', ganadores3 )
    #np.savetxt('gandadores4.txt', ganadores4 )

    np.savetxt('ganadores.txt', ganadores, fmt='%d')
    plt.show()
