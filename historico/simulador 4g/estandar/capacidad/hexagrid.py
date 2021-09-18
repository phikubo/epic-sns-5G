#inmortal llega a casa 

import matplotlib.pyplot as plt
from matplotlib.patches import RegularPolygon
import numpy as np
import math
import random
import time
import calculadora
import hacerCirculo_angulo as hc
#http://magomar.github.io/deludobellico//programming/java/hexagonal-maps/2013/10/10/mapas-hexagonales-2.html
#https://joseguerreroa.wordpress.com/2016/11/17/como-producir-rejillas-grid-hexagonales-mediante-pyqgis/
#https://gamedevelopment.tutsplus.com/es/tutorials/introduction-to-axial-coordinates-for-hexagonal-tile-based-games--cms-28820
#https://gamedevelopment.tutsplus.com/es/tutorials/hexagonal-character-movement-using-axial-coordinates--cms-29035
 
#modificado por: John Michael (phikubo)

'''La modificación consiste en que se puede escalar los hexagonos al radio que uno fije, en ese sentido
la grilla de hexagono mantiene su forma.
 
El script permite n celdas, 

En la próxima entrega se hara sectorización (por 3) y se permitirá varios niveles (vueltas respecto al origen) en la grilla.''' 

#NOTA PERSONAL: Si colocar time.sleep(time) ubicar un print() que indique su existencia.

def calcular_radio_externo(radio):
	'''calcula la distancia entre el centro de una celda al centro de otra celda, usand el radio de una celda.'''
	lado=radio*2*math.sin(math.radians(30))
	radio_externo=radio+lado/2 #para una grilla horizontal
	#radio_externo=radio+lado/2+lado/2 +lado/2 +lado/2 #para una grilla vertical
	return radio_externo
	
def guardar_lista(lista,bd_coordenadas):
	'''Guarda la lista creada y adiciona la coordenada z'''
	#print("coordenadas: ",lista, "y ",lista[0],",", lista[1])
	#x+y+z=0 en coordenadas axiales, despejando z=-x-y entonces lo genero
	#en este caso x, y equivalen respectivamente a lista[0] y lista[1]
	coordenada_z = -lista[0]-lista[1]
	lista.append(coordenada_z)
	bd_coordenadas.append(lista)
	return bd_coordenadas
	 
def generar_lista(nivel,rae, bd_coordenadas):
	'''Crea una lista de coordenadas'''
	for j in range(nivel):
		for m in range(nivel):
			l=[j,m]
			guardar_lista(l, bd_coordenadas)
			#proceso
			#guardar
			#limpiar variable
			#volver a empezar
def generar_lista_respecto_a_xy():
	pass

def crear_labels(coord):
	'''Asocia las coordenadas axiales con el numero de la celda, de ese modo crea en el orden una lista de coordenadas'''
	label=[]
	label_aux=[]
	coma="."
	str_aux=""
	conta=0
	for i in coord:
		#print("i: ",i )
		for j in i:
			#print(j)
			str_aux=str_aux+coma+str(j)
		##print("aux: ",str_aux)
		label_aux.append(str_aux)
		label.append(label_aux)
		str_aux=""
		label_aux=[]
	return label
	
#falta crear el algorimo de sectorizacion
def crear_color(coord):
	'''Crea una lista random de colores a partir de una lista core'''
	colores=["Green","Blue","Red"]
	label_aux=[]
	colors=[]
	#print(random.choice(colores))
	for i in range(len(coord)):
		color=random.choice(colores)
		label_aux.append(color)
		colors.append(label_aux)
		label_aux=[]
	return colors
		


def crear_coordenadas_grilla_horizontal(coord, coef, nivel):
	'''Calcula las coordenadas horizontales y verticales. En el caso de las coordenadas verticales se usa las primeras dos
	elementos de la lista para expandir la grilla'''
	#proceo 1 completado
	hcoord = [coef*c[0] for c in coord] #para grilla horizontal
	#hcoord = [1/3*coef*c[0] for c in coord]
	vcoord =[]
	vc_aux=[]
	coordenadas_pares=[]
	coordenadas_impares=[]
	coordenadas=[]
	n=nivel*nivel
	#proceso vertical
	
	if nivel==1:
		pass
	else:
		for i in range(2*nivel):
			coordenadas.append(coord[i])

	for c in coordenadas:
		resultado=1*2. * np.sin(np.radians(60)) * (coef*c[1] - coef*c[2]) /3.
		vc_aux.append(resultado)
	vcoord=calculadora.calc_rango(2*nivel)*vc_aux
	vcoord=vcoord[0:n]
	#print(len(vcoord),  n  )
	#print("por dos", vcoord[0:n])
	return hcoord, vcoord
	 
 	
			
			
def plotear_grid(coef,radio, coord, nivel, azi):
	'''Plotea graficas de celdas hexagonales. Parametros: radio celda a celda, radio, coordenadas y el nivel. Nivel=n*n, n=celdas.'''
	labels=crear_labels(coord) 
	colors=crear_color(coord)
	
	##print("labels: ",labels )
	# Vertical cartersian coords
	#calcula el centro de los hexagonos
	hcoord, vcoord = crear_coordenadas_grilla_horizontal(coord, coef, nivel)
 
	fig, ax = plt.subplots(1)
	ax.set_aspect('equal')
	vertical_coef=1 
	
	if nivel==1:
		vcoord=hcoord
	for x, y, c, l in zip(hcoord, vcoord, colors, labels):
 
		color = c[0].lower()  # matplotlib understands lower case words for colours
		hex = RegularPolygon((x, y), numVertices=6, radius=vertical_coef*radio, #0.67
                         orientation=np.radians(30), #con 60 grados funciona perfecto, pero las coordenadas cambian. Antes 30
                         facecolor=color, alpha=0.2, edgecolor='k')
                         #cambiar radius=2. / 3. , cuando se usa coord_0
		ax.add_patch(hex)
    	# Also add a text label
		ax.text(x, y+0.2, l[0], ha='center', va='center', size=6)
	# Also add scatter points in hexagon centres
	
	
	'''hcoord, vcoord = crear_coordenadas_grilla_horizontal(coord, coef, nivel)
	for x, y, c, l in zip(hcoord, vcoord, colors, labels):
		color = c[0].lower()  # matplotlib understands lower case words for colours
		hex = RegularPolygon((x, y), numVertices=6, radius=1/2*vertical_coef*radio, #0.67
                         orientation=np.radians(30), #con 60 grados funciona perfecto, pero las coordenadas cambian. Antes 30
                         facecolor=color, alpha=0.2, edgecolor='k')
                         #cambiar radius=2. / 3. , cuando se usa coord_0
		ax.add_patch(hex)
    	# Also add a text label
		ax.text(x, y+0.2, l[0], ha='center', va='center', size=6)
	'''	
 
	if nivel ==1:
		ax.scatter(hcoord, [0.0], c=colors[0][0].lower(), alpha=0.5)
	else:
		ax.scatter(hcoord, vcoord, c=[c[0].lower() for c in colors], alpha=0.5)
		
	#plots de circulo
	cx,cy, angx,angy = hc.coordenadas_circulo(radio, azi)
	plt.plot(cx,cy)
	#calculo coordenadas de angulo de azimut
	for x,y in zip(angx, angy):
		plt.plot(radio*x,radio*y, 'r*')
		
	plt.grid(True)
	plt.show()

def graficar(radio, nivel):
	bd_coordenadas=[]
	rae=calcular_radio_externo(radio)
	coef=rae
	#calcula el azimut respecto a el angulo 0
	azi = calculadora.azimut_lista(0)
	generar_lista(nivel, rae, bd_coordenadas)	
	plotear_grid(coef, radio, bd_coordenadas, nivel, azi)

if __name__ =="__main__":
	print("How to implement hexagrid in modular ways.")
	radio=100/10 #en decamentros
	nivel=1
	graficar(radio,nivel)
	
else:
	print("Modulo hexagrid importado.")
 
 
  
