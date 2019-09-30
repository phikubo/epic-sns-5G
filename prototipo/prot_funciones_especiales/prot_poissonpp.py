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

#matrix
https://www.programiz.com/python-programming/matrix
https://www.python-course.eu/matrix_arithmetic.php

#mapas de calor(potencias recibidas), libreria. https://seaborn.pydata.org/, https://likegeeks.com/seaborn-heatmap-tutorial/
https://riptutorial.com/es/matplotlib/example/17254/mapa-de-calor
https://www.analyticslane.com/2019/02/25/mapas-de-calor-y-diagramas-de-arana-en-python/
https://codeday.me/es/qa/20181211/19168.html
https://codeday.me/es/qa/20190509/663129.html

https://www.absentdata.com/python-graphs/create-a-heat-map-with-seaborn/
https://seaborn.pydata.org/generated/seaborn.heatmap.html
	
'''



'''
Hay dos posibles formas de distribuir puntos:
1. la primera es distribuir en cada hexagono
2. la segunda es distribuir en cada sector
'''
def distribuir_en_sector():
	'''Funcion. Distribuye usuarios en un sector. Retorna una matriz por celda mas no por sector.'''
	pass

def distribuir_en_celdas(r, x_origen, y_origen, intensidad):
	'''Funcion. Distribuye un conjunto de usuarios en un conjunto de celdas. El resultado
	es las coordenadas de usuarios por celda, empaquetados en una matriz. Con esta matriz se 
	calcula la distancia. Retorna una matriz de matrices (matriz de celda).'''
	area_total=np.pi*r**2
	cantidad_de_puntos = np.random.poisson(intensidad*area_total) 
	#de esta forma todas las celdas tiene el mismo numero de usuarios.
	#llamar funcion
	print("ppp: puntos de entrada ", len(x_origen))
	'''Recordar que x_origen y y_origen de esta funcion tiene un formato dinamico
	esto debe ser tenido en cuenta como se hizo para la sectorizacion.(revisar si 
	lo dicho anterior, es verdad. parece que no)'''
	lista_x=[]
	lista_y=[]

	for x,y in zip(x_origen,y_origen):
		#print(x,y)
		coordenada_x, coordenada_y = distribuir_usuarios(r, cantidad_de_puntos)
		#print("antes: ", coordenada_x, "sumando ", x)
		coordenada_x=coordenada_x + x 
		
		lista_x.append(coordenada_x)
		#print("dapues: ", coordenada_x)
		coordenada_y=coordenada_y + y
		lista_y.append(coordenada_y)
	#e.g., para celdas=19, hay cantidad_de_puntos distribuidos con ppp.
	
	#convierto la lista de array en array de listas #issue: no sirve .shape
	'''Por cada coordenada x,y, existen n usuarios de coordenadas cordenada_x,cordenada_y'''
	coordenada_np_x=np.asarray(lista_x)
	coordenada_np_y=np.asarray(lista_y)
	return coordenada_np_x, coordenada_np_y
	#print(coordenada_np_x[0])
	#print(coordenada_np_x[0][1])
	#print(coordenada_np_x.shape())

	#return 
	#print(len(lista_x)) #ahora si convierto a numpy

	
	#print("ppp output: puntos de salida en y ", len(coordenada_x))
	#coordenada_x=coordenada_x+x_origen
	#coordenada_y=coordenada_y+y_origen

def distribuir_usuarios(r, cantidad_puntos):
	'''Funcion. Copia el comportamiento de distribuir_circuo, pero en una forma modular'''
	#calcular theta y rho en esta funcion, garantiza que sean distintos.
	try:
		theta=2*np.pi*np.random.uniform(0,1,cantidad_puntos)
		rho=r*np.sqrt(np.random.uniform(0,1,cantidad_puntos))
		coord_x = rho * np.cos(theta)
		coord_y = rho * np.sin(theta)
	except Exception as ex:
		print(ex)
	return coord_x, coord_y
	#alto ahi vaquero, esto puede ir afuera para modular el problema, lo que resulta mas conveniente
	#coordenada_x=coordenada_x+x_origen
	#coordenada_y=coordenada_y+y_origen


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
