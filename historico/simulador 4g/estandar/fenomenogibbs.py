#Implemtenado por Michael phiku
import numpy as np
import matplotlib.pyplot as plt
import math
import time
#ecuacion de fourier para generar un pulso rectangular con la ecuacion del fenomeno de gibbs    

'''
La ecuacion que simula la suma parcial de armonicos de un pulso rectangular
y(t)=(4/pi)*sum((sen(2*k-1)/(2*k-1))*t), k=1->n
Fuente:http://sistemyse.blogspot.com/
El indice ha cambiado para evitar los numeros pares:
http://mathworld.wolfram.com/FourierSeriesSquareWave.html 

'''


def maint(K, N=100):
    y_sum=0
    y_record=[]
    t = np.linspace(0.0, 10.0, N, endpoint=False)
    for k in range(1,K+1):
        ##print(k)
        y = (4/math.pi)*(np.sin((2*k-1)*t)/(2*k-1))
        #y_sum=y #si se puede hacer
        y_sum=np.add(y_sum,y)
        #print(np.shape(y))
        #y_record.append(y)
        plt.plot(t, y_sum)
        #if k>1:
        #    y_sum=np.add(y_record)
        #    plt.plot(t, y_sum)
    plt.plot(t, y_sum)
    plt.xlabel("t")
    plt.ylabel("y(t)")
    plt.title('Fenomeno de Gibbs', fontsize=16, color='r')
    plt.grid(True)
    plt.show()
    print("main")





if __name__ == "__main__":
    k=7
    maint(k)
    #tarea, realizar el mismo procedimiento sin la libreria numpy.
else:
    print("importado gibss")
