#import ppp
import matplotlib.pyplot as plt
from matplotlib.patches import RegularPolygon
import numpy as np
import math
'''Grid
El script grid permite generar los datos de salida de unas celdas hexagonales con patron circular con los siguientes parámetros:
1. radio (radio de celda)
2. circulos (circulos al rededor de la celda original)
3.

El script debe retornar las gráficas asociadas, sin plotearlas

Enlaces:

Hexagonos: 
-https://www.ditutor.com/geometria/hexagono.html
-https://es.wikipedia.org/wiki/Hex%C3%A1gono
'''

class celda():
	def __init__(self,):
		#variables fijas
		pass
	def func():
		pass
	def func2():
		pass

def main(re):
	pass
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

def generar_lista(numero_celdas, bd_coordenadas):
	'''Crea una lista de coordenadas'''
	for j in range(numero_celdas):
		if j==0:
			for m in range(numero_celdas):
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
					for m in range(numero_celdas):
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
					for m in range(numero_celdas):
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
								'''Como el ultimo uso de la funcion es llamar a guardar, teniendo en cuenta que esta retorna bd_coordenadas, entonces no es necerio repetir el proceso'''
								guardar_lista(jm, bd_coordenadas)
	return bd_coordenadas #corregido, ahora el ultio uso es return, es neceario guardar la variable. Solo con propositos estticos


def distancia_entre_celdas(apotema):
	"Calcula la distancia entre celdas dado el apotema de una celda."
	distancia=2*apotema
	return distancia

def crear_etiquetas(bd_coordenadas):
	'''Asocia las coordenadas axiales con el numero de la celda, de ese modo crea en el orden una lista de coordenadas'''
	label=[]
	label_aux=[]
	coma="."
	str_aux=""
	conta=0
	for i in bd_coordenadas:
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

def crear_colores(bd_coordenadas):
	'''Crea una lista random de colores a partir de una lista core'''
	colores=["Green","Blue","Red","Yellow" ]
	label_aux=[]
	colors=[]
	
	#print(random.choice(colores))
	#print(coord[0])
	for i in bd_coordenadas:
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
		
def crear_coordenadas(numero_celdas,radio_ext, bd_coordenadas, distancia_entre_celda):
	'''Calcula las coordenadas horizontales y verticales. En el caso de las coordenadas verticales se usa las primeras dos
	elementos de la lista para expandir la grilla'''
	#Funcionamiento de listas
	#coordin=[]
	#for c in coord:
	#	coordin=[coord[0],coord[1],coord[2]]
	print(distancia_entre_celda)
	
	hcoord = [2*radio_ext*c[0] for c in bd_coordenadas ] #para grilla horizontal
	#hcoord = [1/3*distancia_entre_celda*c[0] for c in bd_coordenadas]
	vc_aux=[]
	coordenadas_pares=[]
	coordenadas_impares=[]
	coordenadas=[]
	n=numero_celdas*numero_celdas

	#proceso vertical
	#if numero_celdas==1:
	#	pass
	#else:
	#	for i in coord:
	#		coordenadas.append(coord[i])
	#		print(coordenadas)
	'''
	for c in bd_coordenadas:
		#print(distancia_entre_celdas*c[1])
		if c[0]==0:
			resultado= c[1]*distancia_entre_celda
		elif c[1]==0:
			resultado= c[1]*2*distancia_entre_celda*3/2
		else:
			resultado= c[1]*2*distancia_entre_celda/2.
		#print(resultado)
		vc_aux.append(resultado)
	'''
	#print(vc_aux)
	#vcoord=calculadora.calc_rango((numero_celdas-1)*7)*vc_aux
	vcoord = [1. * np.sin(np.radians(60)) * (distancia_entre_celda*c[1] - distancia_entre_celda*c[2]) /1.0 for c in bd_coordenadas]
	#vcoord=vc_aux
	return hcoord, vcoord

def dibujar_celdas(numero_celdas, distancia_entre_celda, radio_ext, bd_coordenadas):
	'''Dibuja patrones de celdas hexagonales'''
	etiquetas=crear_etiquetas(bd_coordenadas) 
	colores=crear_colores(bd_coordenadas)
	hcoord, vcoord = crear_coordenadas(numero_celdas,radio_ext, bd_coordenadas, distancia_entre_celda)
	print(len(hcoord), len(vcoord))
	fig, ax = plt.subplots(1)
	ax.set_aspect('equal')
	vertical_coef=1 
	print(vcoord)

	if numero_celdas==1:
		vcoord=hcoord
	for x, y, c, et in zip(hcoord, vcoord, colores, etiquetas):
		color = c[0].lower()  # matplotlib understands lower case words for colours
		#radius: aumentar, aumenta el radio de la celda central interna.
		hex = RegularPolygon((x, y), numVertices=6, radius=radio_ext,
                         orientation=np.radians(30), #con 60 grados funciona perfecto, pero las coordenadas cambian. Antes 30
                         facecolor=color, alpha=0.2, edgecolor='k')
                         #cambiar radius=2. / 3. , cuando se usa coord_0
		ax.add_patch(hex)
    	# Also add a text label
		ax.text(x, y+0.2, et[0], ha='center', va='center', size=6)

	if numero_celdas ==1:
		ax.scatter(hcoord, [0.0], c=colores[0][0].lower(), alpha=0.5)
	else:
		ax.scatter(hcoord, vcoord, c=[c[0].lower() for c in colores], alpha=0.5)
		print(ax)	

	plt.grid(True)
	plt.show()

if __name__=="__main__":
	#Prototipo:
	numero_celdas=1
	radio_ext=100/10 #en decametros
	lado=2*radio_ext*math.cos(math.radians(60)) #radio=lado
	print(radio_ext, "lado", lado)
	apotema=math.sqrt(radio_ext**2 -(0.5*radio_ext)**2)
	apotema2=radio_ext*math.cos(math.radians(30))
	print("ap", apotema, apotema2)
	#main(radio_ext)
	bd_coordenadas=[]
	bd_coordenadas = generar_lista(3, bd_coordenadas)
	print("coordenadas hex: ", bd_coordenadas)
	#
	distancia_entre_celda=distancia_entre_celdas(apotema)
	dibujar_celdas(numero_celdas, distancia_entre_celda, radio_ext, bd_coordenadas)

else:
	print("Modulo <escribir_nombre> importado")
