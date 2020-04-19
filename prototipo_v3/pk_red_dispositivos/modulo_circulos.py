import matplotlib.patches as mpatches
from matplotlib.patches import RegularPolygon
import matplotlib.pyplot as plt
import numpy as np
import math
import os

def azimut_lista(angulo_inicial):
	'''Dado un angulo, se calcula el azimut. Como resultado se obtiene una
	lista de 3 angulos, incluyendo el inicial. Esta funcion solo es util para obtener
	3 angulos, por ello se usa para trisectorizar, es decir, a partir de un angulo, encontrar
	los 2 siguientes que estan separados simetricamente entre si.'''
	az=[angulo_inicial +i*120 for i in range(3)]
	return az

def calcular_angulo_v3(angulo_inicial, angulo_particion):
	'''Dado un angulo, se calcula el azimut. Como resultado se obtiene una
	lista de 3 angulos, incluyendo el inicial. Esta funcion solo es util para obtener
	3 angulos, por ello se usa para trisectorizar, es decir, a partir de un angulo, encontrar
	los 2 siguientes que estan separados simetricamente entre si.'''
	n=360/angulo_particion
	angs=[angulo_inicial +i*angulo_particion for i in range(int(n))]
	return angs

def angulos_2_cartesiano_norm(angulos):
	'''Funcion. A partir de unos angulos, calcula la coordenada cartesiana en {x} y {y}, en un valor normalizado'''
	ang_x=[]
	ang_y=[]
	for i in angulos:
		ang_x.append(np.cos(np.radians(i)))
		ang_y.append(np.sin(np.radians(i)))
	return ang_x, ang_y

def angulos_2_cartesiano(ang_x,ang_y, radio):
	'''Funcion. Transfroma coordenadas de circulos ya cartesianas normalizadas, a solo coordenadas cartesianas'''
	ang_cart_x=[]
	ang_cart_y=[]

	for x,y in zip(ang_x, ang_y):
		ang_cart_x.append(radio*x)
		ang_cart_y.append(radio*y)

	return ang_cart_x,ang_cart_y

def dibujar_circulo(radio,angulos):
	'''Funcion. Dibuja un conjunto de angulos dados sobre la circunferencia de radio dado.
	Input: coordenadas cartesianas de angulos, normalizado.
	Output: figura.'''
	fig = plt.figure()
	ax = plt.axes()
	ax.set_aspect(1)

	angx,angy=angulos_2_cartesiano_norm(angulos)

	theta = np.linspace(-np.pi, np.pi, 300) #200 es el numero de puntos.
	plt.plot(radio*np.sin(theta), radio*np.cos(theta)) #dibujo la cirfunferencia
	#dibujo los puntos sobre la circunferencia y multiplico por el radio para desnormalizar.
	for x,y in zip(angx, angy):
		#print( "for", x,y)
		#plt.plot(radio*x,radio*y, 'r*')
		pass
	#el resultado es la figura con los angulos presentes.
	return fig


def coordenadas_angulos(angulos):
	"Regresa las coordenadas x,y de un angulo."
	angx,angy=angulos_2_cartesiano_norm(angulos)
	return angx,angy


def coordenadas_circulo(radio, origen):
	"Retorna las coordenadas de un circulo"
	theta = np.linspace(-np.pi, np.pi, 200)
	cx=radio*np.sin(theta)+origen[0]#cord x
	cy=radio*np.cos(theta)+origen[1]#cord y
	return cx,cy

def tri_sectorizar(angulo_x,angulo_y, radio_ext, cartesian_x, cartesian_y, ax):
	'''Funcion que ubica un conjunto de celdas con centro x,y ajutadas en un angulo angx,angy'''
	apotema_trisec= radio_ext/2 #relaciono el apotema tri con el radio celda grande
	radio_trisec =2*apotema_trisec* math.sqrt((4/3)) #radio a partir del apotema
	radio_circular=radio_trisec #paso extra, no necesario
	colores=["Red","Red","Red"] #por que son 3 mini sectores
	for cartx,carty in zip(cartesian_x, cartesian_y):
		for x,y in zip(angulo_x, angulo_y):
			color = colores[0].lower()
			hexagonal_trisec = RegularPolygon((0.5*radio_ext*x+cartx, 0.5*radio_ext*y+carty), numVertices=6, radius=radio_ext*0.5*1,
								orientation=np.radians(60), facecolor=color, alpha=0.2, edgecolor='k')
			ax.add_patch(hexagonal_trisec)


def prueba_angulos_v30():
	'''Prueba que modifica funcion azimut. Cambio de nombre y funcionalidad. '''
	radio=10
	#x,y=coordenadas_circulo(radio, origen=[10,10])
	angulos=calcular_angulo_v3(angulo_inicial=0, angulo_particion=60)
	angx_norm,angy_norm=angulos_2_cartesiano_norm(angulos)
	x,y=angulos_2_cartesiano(angx_norm,angy_norm,radio)
	#radio*angy

	dibujar_circulo(radio, angulos)
	#plt.figure()
	plt.plot(x,y, "g+")
	#plt.axis("equal")
	plt.grid(True)

	plt.show()

	#prueba exitosa

	#INSIGHT:
	'''Al hacer zoom sobre las coordenas del circulo y la de los angulos, no coinciden.
	Esto se debe a que la resolución de theta afecta la exactitud de esta coinicidencia.'''



def prueba_v00():
	'''Prueba original '''
	radio=10
	angulos=[0, 90]
	dibujar_circulo(radio, angulos)
	#x,y=coordenadas_circulo(radio, origen=[10,10])
	plt.axis("equal")
	plt.grid(True)
	#plt.plot(x,y)
	plt.show()


if __name__ == "__main__":
	#prueba_v00()
	prueba_angulos_v30()
else:
	print("Modulo Importado: [", os.path.basename(__file__), "]")
