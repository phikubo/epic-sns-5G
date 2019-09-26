#
import matplotlib.pyplot as plt
from matplotlib.patches import RegularPolygon
import numpy as np
import math
import patron_hexagonal_circular as phc
#
def guardar_lista(lista,bd_coordenadas):
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
	'''Crea una lista de coordenadas axiales en malla'''
	pass


def mapear_coordenadas_cartesianas():
	'''Funcion para crear coordenadas x,y,z en el plano cartesiando'''
	pass

def generar_patron_circular(nivel, patron):
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



def dibujar_celdas():
	'''Funcion principal'''
	pass

def variables():
	numero_celdas=1	#requerimiento: funciona como una ventana, un slicing es util para graficar el número deseado
	nivel=1 #nivel corresponde al nivel de coordenada hexagonal, (1.0.1) nivel 1, (2.0.1) nivel 2, etc.
	radio_ext=100/10 #radio de la celda hexagonal, igual en magnitud al lado.
	apotema=math.sqrt(radio_ext**2 -(0.5*radio_ext)**2) #apotema
	coordenada_patron=[] #inicialización de coordn

	return numero_celdas,nivel, radio_ext, apotema, coordenada_patron
	
def test_coordenadas(nivel, coordenada_patron):
	g=generar_lista(nivel, coordenada_patron)


if __name__=="__main__":
	#Prototipo: palabras claves: mapear, generar, dibuajar
	#variables
	numero_celdas,nivel,radio_ext, apotema, coordenada_patron =variables()

	'''Task 1. generar patron circular-terminado'''
	#coordenada_patron = generar_patron_circular(nivel, coordenada_patron)
	coordenadas = phc.ensamblar(nivel)
	'''Task 2. generar patron en malla'''
	#test_coordenadas(nivel, coordenada_patron)
	'''Task 3. generar numero de celdas deseadas'''
	numero_celdas=3
	
else:
	print("Modulo <escribir_nombre> importado")
