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
Estado: concluida.
recipe: https://hpaulkeeler.com/poisson-point-process-simulation/
recomendations from recipe: "For simulation of point processes, see, for example, the books Statistical Inference and Simulation for Spatial Point Processes by Møller and Waagepetersen, or Stochastic Geometry and its Applications by Chiu, Stoyan, Kendall and Mecke."

Resultados:
	#how many points?: numpypoints, numbpoints. 
	#xdelta, ydelta si tiene incidencia en la ventanada de ploteo de numpy, cuando (xdelta,ydelta)=!(1,1)
	#when using rvs(a,b,c), a,b=(0,1), outputs are proportional to n*ndelta. But, when using a,b=(-1,1) or other combination, outputs are critically afected.
	#another results but in spanish v:
	#la funcion scatter() sirve para parametrizar algunas caracteristicas del ploteo e.g, color y forma.
	#plot() no funciona correctamente, con los parámetros fijos, pero sí sin parámetros, como aparece abajo comentado.
'''

def maint():
	#Simulation window parameters
	#p:xmin,ymin, are (x0,y0) the origin in the left.
	xMin=0;xMax=1; #size of rectangle in x cartesian coordinates
	yMin=0;yMax=1; #size of rectangle in y cartesian coordinates
	xDelta=xMax-xMin;yDelta=yMax-yMin; #rectangle dimensions, p:useful when (x0,y0 =! 0,0) are not in the origin.
	areaTotal=xDelta*yDelta;
	
	#Point process parameters
	lambda0=100; #intensity (ie mean density) of the Poisson process. ¿What density is needed for UEs?
	print("A_tot", lambda0*areaTotal ) 
	#Simulate Poisson point process
	numbPoints = scipy.stats.poisson( lambda0*areaTotal ).rvs()#Poisson number of points. rvs() method provides the sample (number).
	nunpyPoints = np.random.poisson(lambda0*areaTotal) #But this one, already provides the sample.
	print("scipy: ", numbPoints, "numpy: ", nunpyPoints)
	#
	xx = xDelta*scipy.stats.uniform.rvs(0,1,((numbPoints,1)))+xMin#x coordinates of Poisson points
	yy = yDelta*scipy.stats.uniform.rvs(0,1,((numbPoints,1)))+yMin#y coordinates of Poisson points
	print(len(xx),len(yy))
	xxn = 4*xDelta*scipy.stats.uniform.rvs(-1,1,((nunpyPoints,1)))+xMin#x coordinates of Poisson points, using numpy
	yyn = 4*yDelta*scipy.stats.uniform.rvs(-1,1,((nunpyPoints,1)))+yMin#y coordinates of Poisson points, using numpy
	# 
	#Plotting
	plt.scatter(xx,yy, edgecolor='b', facecolor='none', alpha=0.5 )
	plt.scatter(xxn,yyn, edgecolor='r', facecolor='none', alpha=0.5)
	#plt.plot(xxn,yyn, '.')
	plt.xlabel("x"); plt.ylabel("y")
	#
	plt.xlabel("Prueba de Puntos con distribución Poisson")
	plt.ylabel("y(t)")
	plt.title('Rectangular Point Poisson Process', fontsize=16, color='r')
	plt.grid(True)
	plt.show()
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
	maint()
else:
    print("importado:ppp")
