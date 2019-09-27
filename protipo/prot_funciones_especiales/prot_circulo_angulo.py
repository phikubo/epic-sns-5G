import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import numpy as np
import math

def obtener_linea(angulos):
	'''Funcion. A partir de unos angulos, calcula la coordenada cartesiana en {x} y {y}, en un valor normalizado'''
	ang_x=[]
	ang_y=[]
	for i in angulos:
		ang_x.append(math.cos(math.radians(i)))
		ang_y.append(math.sin(math.radians(i)))
	return ang_x, ang_y

def dibujar_circulo(radio,angulos):
	'''Funcion. Dibuja un conjunto de angulos dados sobre la circunferencia de radio dado.'''
	fig = plt.figure()
	ax = plt.axes()
	ax.set_aspect(1)
	
	angx,angy=obtener_linea(angulos)
	
	theta = np.linspace(-np.pi, np.pi, 200) #200 es el numero de puntos.
	plt.plot(radio*np.sin(theta), radio*np.cos(theta)) #dibujo la cirfunferencia
	#dibujo los puntos sobre la circunferencia y multiplico por el radio para desnormalizar.
	for x,y in zip(angx, angy):
		print( "for", x,y)
		plt.plot(radio*x,radio*y, 'r*')
	#el resultado es la figura con los angulos presentes.	
	return fig

	
def coordenadas_circulo(radio, angulos):
	#no implementado
	angx,angy=obtener_linea(angulos)
	theta = np.linspace(-np.pi, np.pi, 200)
	cx=radio*np.sin(theta)
	cy=radio*np.cos(theta)
	angx,angy=obtener_linea(angulos)
	return cx,cy, angx,angy
	
if __name__ == "__main__":
	radio=10
	angulos=[0, 90]
	
 
	dibujar_circulo(radio, angulos)
	plt.show()
else:
	pass
