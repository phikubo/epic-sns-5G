#Implemtenado por Michael phikubo. 
#Script para generar puntos que simulan la posición de UEs en el espacio, mediante el proceso Poisson (Point Processs Poisson)
import numpy as np
import matplotlib.pyplot as plt
import math
import time

'''
Resultados: El algoritmo genera una distribución que no corresponde al proceso Poisson, aunque los puntos sean generados
con la distribución poisson de la librería numpy. Una versión más interesante resulta cuando los datos en x o y, son aleatorios,
esto se puede lograr usando random.random(), sin embargo, se desconoce si este cambio siguie el processo. 

Estado: obsoleto

Fuente: https://docs.scipy.org/doc/numpy-1.15.1/reference/generated/numpy.random.poisson.html
'''

def maint():
    tamano=100
    y_axis=10
    #t = np.linspace(0.0, 10.0, N, endpoint=False)
    pppx=np.random.poisson(y_axis,tamano)
    pppy=np.random.poisson(y_axis,tamano)
    s = np.random.poisson(lam=(100., 500.), size=(100, 2))
    x=tamano*np.random.random(tamano)
    #
    plt.plot(pppx, s, '.')
    plt.xlabel("Prueba de Puntos con distribución Poisson")
    plt.ylabel("y(t)")
    plt.title('Poisson Process Point', fontsize=16, color='r')
    plt.grid(True)
    plt.show()
    

if __name__ == "__main__":    
	maint()
else:
    print("importado gibss")
