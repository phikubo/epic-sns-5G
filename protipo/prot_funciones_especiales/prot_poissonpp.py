#Implemtenado por Michael phikubo. 
#Script para generar puntos que simulan la posición de UEs en el espacio, mediante el proceso Poisson (Point Processs Poisson)
#El script, presenta dos tipos de pruebas: se generan puntos con la libreŕia scipy y con numpy. Los resultados no difieren.
import numpy as np
import scipy.stats
import matplotlib.pyplot as plt
import math
import time

'''
Phikubo says-> No todos los comentarios pertenecen a la receta. Algunos comentarios en ingles fueron puestos por Phikubo para pruebas y documentación.
Estado: En proceso.
recipe: https://hpaulkeeler.com/simulating-a-poisson-point-process-on-a-disk/, https://stackoverflow.com/questions/31778995/how-to-generate-a-homogeneous-poisson-point-process-in-a-circle
https://en.wikipedia.org/wiki/Poisson_point_process, https://hpaulkeeler.com/poisson-point-process/
recomendations from recipe: none

Resultados: ok
	
'''

def distribuir_circulo(r, x_origen, y_origen, intensidad):
	'''Funcion. Genera las coordenadas de un conjunto de usuarios confinados
	en un espacio deseado (circulo) y de intensidad (densidad) intensidad'''
	#Simulation window parameters
	#r=1;  #radius of disk
	#centre of disk
	area_total=np.pi*r**2; #area of disk
	
	#Point process parameters
	#intensidad=1; #intensity (ie mean density) of the Poisson process
	#print("lambda: ", intensidad)
	
	#Simulate Poisson point process. Este proceso debe ser independiente de maint si se desea que sea el mismo número de puntos.
	numero_de_puntos = np.random.poisson(intensidad*area_total);#Poisson number of points
	print("Numero de points: ", numero_de_puntos)
	theta=2*np.pi*np.random.uniform(0,1,numero_de_puntos); #angular coordinates 
	rho=r*np.sqrt(np.random.uniform(0,1,numero_de_puntos)); #radial coordinates 
	
	#Convert from polar to Cartesian coordinates
	coordenada_x = rho * np.cos(theta);
	coordenada_y = rho * np.sin(theta);
	
	#Shift centre of disk to (x_origen,y_origen) 
	coordenada_x=coordenada_x+x_origen; coordenada_y=coordenada_y+y_origen;
	
	#Plotting
	#plt.scatter(coordenada_x,coordenada_y, edgecolor='b', facecolor='none', alpha=0.5 );
	#plt.xlabel("x"); plt.ylabel("y");
	#plt.axis('equal');
	#plt.grid(True)
	#plt.savefig("test2.png")
	return coordenada_x,coordenada_y
	#plt.show()
	#
	'''

    tamano=1000
    y_axis=10
    #t = np.linspace(0.0, 10.0, N, endpoint=False)
    pppx=np.random.poisson(y_axis,tamano)
    pppy=np.random.poisson(y_axis,tamano)
    x=tamano*np.random.random(tamano)
    #
    plt.plot(pppx, pppy, '.')
    
    plt.xlabel("Prueba de Puntos con distribución Poisson")
    plt.ylabel("y(t)")
    plt.title('Poisson Process Point', fontsize=16, color='r')
    plt.grid(True)
    plt.show()'''
    

if __name__ == "__main__":
	print("ppp fix function")
	radio=1 
	x=5;y=10
	 
	#requisite: create n disk or radius r.
	#radio: radius of disk. origen: coordinates.  
	intensity=10
	distribuir_circulo(radio, x,y, intensity)
else:
    print("importado:ppp")
