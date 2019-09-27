import matplotlib.pyplot as plt
from matplotlib.patches import RegularPolygon
import numpy as np
import math
import prot_patron_hexagonal_circular as phc
import time #debug
#https://realpython.com/python-modules-packages/
#https://realpython.com/python-testing/
#https://realpython.com/python-pep8/
def guardar_lista(lista,bd_coordenadas):
	#no implementado
	print(3)
	'''Guarda la lista creada y adiciona la coordenada z'''
	#print("coordenadas: ",lista, "y ",lista[0],",", lista[1])
	#x+y+z=0 en coordenadas axiales, despejando z=-x-y entonces lo genero
	#en este caso x, y equivalen respectivamente a lista[0] y lista[1]
	coordenada_z = -lista[0]-lista[1]
	
	lista.append(coordenada_z)
	print(4, lista)
	print(bd_coordenadas)
	bd_coordenadas.append(lista)
	print(5)
	print(bd_coordenadas)
	return bd_coordenadas

def generar_coordenada_axial_malla(num_cel, bd_coordenadas):
	#no implementado
	'''Crea una lista de coordenadas axiales en malla'''
	pass

def generar_patron_circular(nivel, patron):
	#no implementado
	'''Funcion para generar coordenadas (x,y,z) unitaria en un patrón circular'''
	#last task: validar nivel ={1,2,3,4,5,...n}, n E enteros.
	if nivel > 1:
		print("n>1")
	elif nivel == 1:
		print("n=1")
		patron.append([0,0,0])
		print(patron[0]) #this print [0.0.0], patron print [[0.0.0],[]]
	else:
		print("Nivel invalido, fijando nivel a 1")
		nivel=1
		generar_patron_circular(nivel, patron)
	return patron

def test_coordenadas(nivel, coordenada_patron):
	#no implementado
	g=generar_lista(nivel, coordenada_patron)

def distancia_entre_celdas(nivel, radio_ext):
	'''Funcion que genera el valor de la distancia entre el origen y las celdas por nivel. Puede ser util para calcular el 
	radio de todo el sistema'''
	#print(radio_ext)
	r_med=radio_ext/2
	
	#este nivel debe ser constante cuando se llama en el mapeo, porque?
	#Rta, debido a que la distancia entre celdas, se ve afectada por 2/3*seno(60)(x-z), por esto dec
	#no debe ser ajustable porque esa distancia se ajusta en la ecuacion de arriba.
	print("distancia_entre_celdas",3*(nivel)*r_med)
	#print(r_med, nivel)
	return 3*(nivel)*r_med

def mapear_coordenadas_cartesianas(coordenadas_axiales, radio_ext):
	'''Funcion para crear coordenadas x,y en el plano cartesiano a partir de coordenadas axiales'''
	#task 1: crear x,y #terminado x
	#task 2: dibjar puntos
	coordenadas_cartesianas_horizontal = []
	coordenadas_cartesianas_vertical = []
	for i in range(len(coordenadas_axiales)):
		print(i)
	for lista, nvl in zip(coordenadas_axiales, range(nivel+1)):
		print("axiales totales ", lista, "numero de celdas ", len(lista))
		print("nivel: ",nvl)
		dec = distancia_entre_celdas(1, radio_ext)
		print("distancia ", dec)
		print("---------------------")

		for axial in lista:
			print("coordenada axial ") 
			print(axial)
			time.sleep(0.5)
				
			coord_y= 2. * np.sin(np.radians(60)) * (dec*axial[1] - dec*axial[2]) /3.
				
			print("x final: ", axial[0]*dec , "---","y final: ", coord_y)

			coordenadas_cartesianas_horizontal.append(axial[0]*dec)
			coordenadas_cartesianas_vertical.append(coord_y)
		print("---------------------")
		print("---------------------")
		print("---------------------")
			#		print(coord)
			#	coordenadas_cartesianas_horizontal.append(coord*dec)
				#time.sleep(0.4)
	#bug: dec no cambia dinámicamente cuando deberia de acuerdo al nivel
	#print("x", coordenadas_cartesianas_horizontal)
	#print("y", coordenadas_cartesianas_vertical)
	#hcoord = [coef*cord[0] for cord in coordenadas_axiales]
	#vcoord = [2. * np.sin(np.radians(60)) * (coef*c[1] - coef*c[2]) /3. for c in coord]
	return coordenadas_cartesianas_horizontal, coordenadas_cartesianas_vertical

def dibujar_celdas(cartesian_x, cartesian_y, radio_ext):
	'''Funcion principal que dibuja las celdas dadas las coordenadas x,y de su centro.'''
	color="green"
	fig, ax = plt.subplots(1)
	ax.set_aspect('equal')
	for x,y in zip(cartesian_x, cartesian_y):
		plt.plot(x,y, '*')
		malla_hexagonal = RegularPolygon((x, y), numVertices=6, radius=radio_ext,
                         orientation=np.radians(30), #con 60 grados funciona perfecto, pero las coordenadas cambian. Antes 30
                         facecolor=color, alpha=0.2, edgecolor='k')
                         #cambiar radius=2. / 3. , cuando se usa coord_0
		ax.add_patch(malla_hexagonal) #si no no dibuja celdas
		ax.scatter(0, 0, alpha=0.5)
	
def variables():
	numero_celdas=1	#requerimiento: funciona como una ventana, un slicing es util para graficar el número deseado
	nivel=1 #nivel corresponde al nivel de coordenada hexagonal, (1.0.1) nivel 1, (2.0.1) nivel 2, etc.
	radio_ext=100/10 #radio de la celda hexagonal, igual en magnitud al lado.
	apotema=math.sqrt(radio_ext**2 -(0.5*radio_ext)**2) #apotema
	coordenada_patron=[] #inicialización de coordn
	return numero_celdas,nivel, radio_ext, apotema, coordenada_patron

if __name__=="__main__":
	#Prototipo: palabras claves: mapear, generar, dibuajar
	#variables
	
	numero_celdas,nivel,radio_ext, apotema, coordenada_patron =variables()

	#Task 1. generar patron circular-terminado
	#coordenada_patron = generar_patron_circular(nivel, coordenada_patron)
	coordenadas_axiales = phc.ensamblar(nivel)
	##print(len(coordenadas_axiales))
	#Task 2. generar patron en malla-terminado
	#dec = distancia_entre_celdas(nivel, radio_ext)
	cartesian_x, cartesian_y = mapear_coordenadas_cartesianas(coordenadas_axiales, radio_ext)
	print(len(cartesian_x), len(cartesian_y))
	dibujar_celdas(cartesian_x,cartesian_y, radio_ext)
	#test_coordenadas(nivel, coordenada_patron)
	#Task 3. generar numero de celdas deseadas-hint:slicing
	numero_celdas=3
	plt.grid(True)
	#plt.savefig("protipo2.png")
	#print(phc)
	#print(dir(phc))
	#plt.show()
	
	
else:
	print("Modulo <prot_celda> importado")
