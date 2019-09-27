#inmortal llega a casa 

import matplotlib.pyplot as plt
from matplotlib.patches import RegularPolygon
import numpy as np
import math
import random
import time
import calculadora
import hacerCirculo_angulo as hc
import poissonpp as ppp
#http://magomar.github.io/deludobellico//programming/java/hexagonal-maps/2013/10/10/mapas-hexagonales-2.html
#https://joseguerreroa.wordpress.com/2016/11/17/como-producir-rejillas-grid-hexagonales-mediante-pyqgis/
#https://gamedevelopment.tutsplus.com/es/tutorials/introduction-to-axial-coordinates-for-hexagonal-tile-based-games--cms-28820
#https://gamedevelopment.tutsplus.com/es/tutorials/hexagonal-character-movement-using-axial-coordinates--cms-29035
 
#modificado por: John Michael (phikubo) % ftosse.

'''La modificación consiste en que se puede escalar los hexagonos al radio que uno fije, en ese sentido
la grilla de hexagono mantiene su forma.
 
El script permite n celdas, 

En la próxima entrega se hara sectorización (por 3) y se permitirá varios niveles (vueltas respecto al origen) en la grilla.''' 

#NOTA PERSONAL: Si colocar time.sleep(time) ubicar un print() que indique su existencia.

def calcular_radio_externo(radio):
	'''calcula la distancia entre el centro de una celda al centro de otra celda, usand el radio de una celda.'''
	lado=radio*math.cos(math.radians(30))
	#radio_externo=lado #para una grilla horizontal
	radio_externo=radio#+lado/2#+lado/2 #+lado/2 +lado/2 #para una grilla vertical
	return radio_externo
	
def guardar_lista(lista,bd_coordenadas):
	'''Guarda la lista creada y adiciona la coordenada z'''
	#print("coordenadas: ",lista, "y ",lista[0],",", lista[1])
	#x+y+z=0 en coordenadas axiales, despejando z=-x-y entonces lo genero
	#en este caso x, y equivalen respectivamente a lista[0] y lista[1]
	coordenada_z = -lista[0]-lista[1]
	lista.append(coordenada_z)
	bd_coordenadas.append(lista)
	#print(bd_coordenadas)
	return bd_coordenadas
	 
def generar_lista(nivel,rae, bd_coordenadas):
	'''Crea una lista de coordenadas'''
	for j in range(nivel):
		if j==0:
			for m in range(nivel):
				if m==0:
					jm=[j,m]
					guardar_lista(jm, bd_coordenadas)
				else:
					for o in range(2):
						if o==0:
							jm=[j,-m]
						else:
							jm=[j,m]
						#print(ljm)
						guardar_lista(jm, bd_coordenadas)
		
		else:
			for p in range(2):
				if p==0:	
					for m in range(nivel):
						if m==0:
							pass
							#jm=[j,m]
								#guardar_lista(jm, bd_coordenadas)
						else:
							for o in range(2):
								if o==0:
									jm=[j,-m]
								else:
									jm=[j,m]
								ljm=jm
								#print(ljm)
								guardar_lista(jm, bd_coordenadas)
				else: 
					for m in range(nivel):
						if m==0:
							pass
							#jm=[-j,m]
							#guardar_lista(jm, bd_coordenadas)
						else:
							for o in range(2):
								if o==0:
									jm=[-j,-m]
								else:
									jm=[-j,m]
								ljm=jm
								#print(ljm)
								guardar_lista(jm, bd_coordenadas)

					
def min_hexagonos(bd_coordenadas):
	rep1=[]
	rep2=[]

	for i in bd_coordenadas:
		bd_coordenadas[i]=rep1
		for u in bd_coordenadas:
			bd_coordenadas[u]=rep2
			if i==u:
				bd_coordenadas[u]=bd_coordenadas[i]
			elif rep1[i]==rep2[u]:
				bd_coordenadas.pop(bd_coordenadas[u+1])
			else:		
				bd_coordenadas[u]=bd_coordenadas[u]

	return bd_coordenadas

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
	colores=["Green","Blue","Red","Yellow" ]
	label_aux=[]
	colors=[]
	
	#print(random.choice(colores))
	#print(coord[0])
	for i in coord:
		#print(i[0])
		#posc=coord[i]

	#	if i[1]>0 and i[1]!=i[0]:
	#		color=colores[0]
	#	elif i[1]<0 :
	#		color=colores[1]
	#	else:
	#		color=colores[2]
		color=colores[3]
		#color=random.choice(colores)
		label_aux.append(color)
		colors.append(label_aux)
		label_aux=[]
	print(colors)	
	return colors
		


def crear_coordenadas_grilla_horizontal(coord, coef, nivel,radio):
	'''Calcula las coordenadas horizontales y verticales. En el caso de las coordenadas verticales se usa las primeras dos
	elementos de la lista para expandir la grilla'''
	#proceo 1 completado
	#coordin=[]
	#for c in coord:
	#	coordin=[coord[0],coord[1],coord[2]]

	print(coord)
	hcoord = [coef*c[0] for c in coord ] #para grilla horizontal
	#hcoord = [1/3*coef*c[0] for c in coord]
	#print(hcoord)
	vcoord =[]
	vc_aux=[]
	coordenadas_pares=[]
	coordenadas_impares=[]
	coordenadas=[]
	n=nivel*nivel
	#proceso vertical
	
	#if nivel==1:
	#	pass
	#else:
		
	#	for i in coord:
	#		coordenadas.append(coord[i])
	#		print(coordenadas)

	for c in coord:
		#print(coef*c[1])
		if c[0]==0:
			resultado= c[1]*radio
		elif c[1]==0:
			resultado= c[1]*radio*3/2
		else:
			resultado= c[1]*radio/2.
		#print(resultado)
		vc_aux.append(resultado)
	#print(vc_aux)
	#vcoord=calculadora.calc_rango((nivel-1)*7)*vc_aux
	vcoord=vc_aux
	print(vcoord)
	#vcoord=vcoord[0:n]
	#print(len(vcoord),  n  )
	#print("por dos", vcoord)
	return hcoord, vcoord
	 
 	
def crear_trisec(radio,agx,agy,ax):
#funcion para plotear las celdas trisectorizadas parametros : radio celda trisector, cordenada X, coordenada Y, figure AX
	colorpos=["Green","Blue","Red"]
	for x,y,c in zip(agx, agy, colorpos):
		
		color = c.lower()  # matplotlib understands lower case words for colours
		'''this radius fix the separation between the polygons.phikubo'''
		hex = RegularPolygon((0.5*radio*x, 0.5*radio*y), numVertices=6, radius=radio*0.5*1, #0.67, 0.95
                         orientation=np.radians(30), #con 60 grados funciona perfecto, pero las coordenadas cambian. Antes 30
                         facecolor=color, alpha=0.2, edgecolor='k')
                         #cambiar radius=2. / 3. , cuando se usa coord_0
		ax.add_patch(hex)
		intensity=0.4

		#si quiero el mismo numero de puntos en todas las celdas debo usar un funcion extra del script ppp que genere primero ese numero ppp segun la intensidad, y luego con el numero, se calcula el area de ploteo.
		#función de coordenadas ppp
		xx,yy=ppp.maint(0.5*radio,0.5*radio*x, 0.5*radio*y, intensity)

		#puntos x,y de ues, ya esta afectados por el 0.5*radio.
		plt.plot(xx,yy, "r.")
		#puntos rojos, centro de las celdas
		plt.plot(0.5*radio*x,0.5*radio*y, 'r*')
		plt.savefig("falta_pulir.png")
	
			
def plotear_grid(coef,radio, coord, nivel, azi):
	'''Plotea graficas de celdas hexagonales. Parametros: radio celda a celda, radio, coordenadas y el nivel. Nivel=n*n, n=celdas.'''
	#print(coord)
	labels=crear_labels(coord) 
	colors=crear_color(coord)
	print("r",radio)
	rcir=radio*math.sin(math.radians(30))
	aPOTEMA=(0.5*radio)/1.15
	print("ap ",aPOTEMA, "rcir ", rcir)
	dif_rcir_aP=rcir-aPOTEMA
	
	##print("labels: ",labels )
	# Vertical cartersian coords
	#calcula el centro de los hexagonos
	hcoord, vcoord = crear_coordenadas_grilla_horizontal(coord, coef, nivel,radio)
	fig, ax = plt.subplots(1)
	ax.set_aspect('equal')
	vertical_coef=1 
	print(vcoord)
	if nivel==1:
		vcoord=hcoord
	for x, y, c, l in zip(hcoord, vcoord, colors, labels):
 
		color = c[0].lower()  # matplotlib understands lower case words for colours
		#radius: aumentar, aumenta el radio de la celda central interna.
		hex = RegularPolygon((2*x, 2*y), numVertices=6, radius=-1.054*dif_rcir_aP+aPOTEMA+radio*math.sin(math.radians(30)), #0.67
                         orientation=np.radians(60), #con 60 grados funciona perfecto, pero las coordenadas cambian. Antes 30
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
	print(c)
	if nivel ==1:
		ax.scatter(hcoord, [0.0], c=colors[0][0].lower(), alpha=0.5)
	else:
		ax.scatter(hcoord, vcoord, c=[c[0].lower() for c in colors], alpha=0.5)
		print(ax)	

	#plots de circulo
	'''Radio/2, engloba el hexagono central. Radio, engloba los puntos centrales de los sectores'''
	cx,cy, angx,angy = hc.coordenadas_circulo(radio/2, azi)
	plt.plot(cx,cy, 'g')

	#calculo coordenadas de angulo de azimutto
	'''Aqui edito tosse: CAMBIO DE COORDENADAS, DE HEXAGONALES 3D A CORDENADAS ANGULARES. Siguiente paso, aislar el código que hace la tri-sectorizacion y  ajustar para que el angulo coincida y sea proporcional'''	
	crear_trisec(radio,angx,angy,ax)		



	plt.grid(True)
	plt.show()

def graficar(radio, nivel):
	bd_coordenadas=[]
	rae=calcular_radio_externo(radio)
	coef=rae
	#calcula el azimut respecto a el angulo 0
	azi = calculadora.azimut_lista(angulo_inicial=0)
	generar_lista(nivel, rae, bd_coordenadas)
	
	plotear_grid(coef, radio, bd_coordenadas, nivel, azi)

if __name__ =="__main__":
	print("How to implement hexagrid in modular ways.")
	radio=100/10 #en decamentros, 10 u.
	nivel=1
	graficar(radio,nivel)
	
else:
	print("Modulo hexagrid importado.")
 
 
  
