import matplotlib.pyplot as plt
from matplotlib.patches import RegularPolygon
import numpy as np
import math
import os

import time #debug
#modulos no deben importar otros modulos locales
def decorador_rastrear(func):
	'''indica el inicio y final de una funcion con su nombre'''
	def funcion_decorada(*args, **kwargs):
		print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>En la función",func.__name__+"()")
		value=func(*args, **kwargs)
		print("Ok<<<<<<<<<<<<<<<<<<<<<<<<<<")
		return value
	return funcion_decorada
#Decorador hace dos llamados. Uno cuando se ejecuta directamente y
#otro indirecto con return, por eso se usa value.

def patron_dado_ab(a,b):
	#funcion que resume las anteriores
	return -1*(a+b)

#@decorador_rastrear
def patron_circular_final(nivel):
	'''Funcion. Genera dinamicamente el conjunto de coordenadas [a,b,c] axiales,
	de acuerdo al nivel deseado. Solo genera un conjunto. Las coordenadas se obtiene siguiendo contramanecillas del reloj
	en cada nivel y siguiendo un patron reconocido en una coordenada especifica que aumenta y:0,1,2,..., la siguiente
	coordenada es el nivel negativo y se calcula la variable faltante. Luego se inserta celda:
	copia coordenada faltante, copia variable especifica en su estado final; pasa a Z y luego a X con el
	mismo patron.'''
	nivel_copy=nivel
	if nivel_copy==0:
		total_celdas=nivel_copy+1
	else:
		total_celdas=nivel_copy*6
	#print("celdas por dibujar: ",total_celdas)
	patron=[[0,0,0] for i in range(total_celdas)]
	#permite cambiar el slicing de cada for para ajustar al nivel deseado, y conformar una sola funcion

	#how to generate this dinamicaly?
	if nivel == 1:
		inicio=[0, nivel+1, 3*nivel+1]
		final =[nivel+1,	3*nivel+1, len(patron)]
	elif nivel==2:
		inicio=[0, nivel+2, 3*nivel+2]
		final =[nivel+1, 3*nivel+1, len(patron)+1]

	#output should be: [1,0,-1],[0,1,-1],[-1,1,0],[-1,0,1],[0,-1,1],[1,-1,0]
	#si el nivel es > 0, es decir {1,2}, se genera coordenada axial a coordenada axial
	# de esquina superior derecha, hacia esquina superior izquierda, en el orden contramanecillas del reloj
	if nivel > 0:
		#inicializo variables para obtener el estado final al término de cada ciclo for.
		#p corresponde al item [a,b,c] dentro de la lista de patron(total_celdas)
		#0,1,2 corresponden a: a,b,c respectivamente
		y=0
		x=0
		z=0
		ultima_variable=0
		#patron[params]: params es un slicing de la lista, se mueve por cada nivel.
		#se obtiene un par de un conjunto {h,i,j}, con el par se calcula la coordenada faltante.
		for y,p in zip(range(nivel+1), patron[inicio[0]:final[0]]):
			p[1]=y
			p[2]=-nivel
			p[0]=patron_dado_ab(p[1],p[2])
			ultima_variable=p[0]
		#se inserta una celda
		if nivel == 1:
			pass
		else:
			patron[nivel+1][1]=y
			patron[nivel+1][0]=ultima_variable-1
			patron[nivel+1][2]=patron_dado_ab(patron[nivel+1][1],patron[nivel+1][0])

		#start of
		for z,p in zip(range(nivel+1), patron[inicio[1]:final[1]]):
			p[2]=z
			p[0]=-nivel
			p[1]=patron_dado_ab(p[2],p[0])
			ultima_variable=p[1]

		if nivel == 1:
			pass
		else:
			patron[3*nivel+1][2]=z
			patron[3*nivel+1][1]=ultima_variable-1
			patron[3*nivel+1][0]=patron_dado_ab(patron[3*nivel+1][2],patron[3*nivel+1][1])

		for x,p in zip(range(nivel+1),patron[inicio[2]:final[2]]):#atencion, patron+1?
			p[0]=x
			p[1]=-nivel
			p[2]=patron_dado_ab(p[0],p[1])
			ultima_variable=p[2]

		if nivel == 1:
			pass
		else:
			patron[len(patron)-1][0]=x
			patron[len(patron)-1][2]=ultima_variable-1
			patron[len(patron)-1][1]=patron_dado_ab(patron[len(patron)-1][0],patron[len(patron)-1][2])
	elif nivel == 0:
		return [[0,0,0]]

	return(patron)


def distancia_entre_celdas(nivel, radio_ext):
	'''Funcion que genera el valor de la distancia entre el origen y las celdas por nivel. Puede ser util para calcular el
	radio de todo el sistema. Calcula la distancia con la mitad del radio que genera patron 3nr'''
	#print(radio_ext)
	r_med=radio_ext/2

	#este nivel debe ser constante cuando se llama en el mapeo, porque?
	#Rta, debido a que la distancia entre celdas, se ve afectada por 2/3*seno(60)(x-z), por esto dec
	#no debe ser ajustable porque esa distancia se ajusta en la ecuacion de arriba.
	print("[NOK] mod_cel->",distancia_entre_celdas.__name__,3*(nivel)*r_med)
	#print(r_med, nivel)
	return 3*(nivel)*r_med


def mapear_coordenadas_cartesianas(coordenadas_axiales, nivel,radio_ext):
	'''Funcion para crear coordenadas x,y en el plano cartesiano a partir de coordenadas axiales'''
	#task 1: crear x,y #terminado x
	#task 2: dibjar puntos
	print("---------------------")
	coordenadas_cartesianas_horizontal = []
	coordenadas_cartesianas_vertical = []

	for lista, nvl in zip(coordenadas_axiales, range(nivel+1)):
		#print("axiales totales ", lista, "numero de celdas ", len(lista))
		#print("nivel: ",nvl)
		dec = distancia_entre_celdas(nvl, radio_ext) ####################################checkear
		#print("distancia ", dec)

		for axial in lista:
			#print("coordenada axial ")
			#print(axial)

			coord_y= 2. * np.sin(np.radians(60)) * (dec*axial[1] - dec*axial[2]) /3.

			#print("x final: ", axial[0]*dec , "---","y final: ", coord_y)

			coordenadas_cartesianas_horizontal.append(axial[0]*dec)
			coordenadas_cartesianas_vertical.append(coord_y)
		#print("---------------------")
		#print("---------------------")
		#print("---------------------")
	for i in range(len(coordenadas_axiales)):
		print("Proceso en Celda #", i, "[OK]")

	print("---------------------")
	return coordenadas_cartesianas_horizontal, coordenadas_cartesianas_vertical


#@decorador_rastrear
def ensamblar(nivel, radio):
	'''Funcion. Genera una sola lista que junta los n niveles, n={0,1,2,3,..}'''
	if nivel > 2:
		print("Nivel n>=3 aun no implementado")
	else:
		pat_cir=[]
		for nvl in range(nivel+1):
			pat_cir.append(patron_circular_final(nvl))
		#return pat_cir
		#mapeo a coordenadas cartesianas.
		#estos son los puntos de cada bs
		#cord_x,cord_y=mapear_coordenadas_cartesianas(pat_cir, radio, nivel)
		#return cord_x,cord_y
		return pat_cir


def coordenadas_nceldas(num,radio):
	"""
	Determina el nivel de celdas e imprime solo el numero de coordenadas cartesianas deseadas.
	Tambien puedo programar logica adentro
	>>> lista=[0,1,2,3,6,7,8,9,18,19,20]
	>>> for i in lista:
	... 	coordenadas_nceldas(i),i
	(-1, 0)
	(0, 1)
	(1, 2)
	(1, 3)
	(1, 6)
	(1, 7)
	(2, 8)
	(2, 9)
	(2, 18)
	(2, 19)
	(-1, 20)
	>>> coordenadas_nceldas(20)
	-1
	"""
	#segun el numero determinar el nivel
	#con el nivel ejectuar ensamblar
	#con las cordenadas axiales, aquí ejecutar coordenadas_cartesianas
	try:
		if num<=0 or num >19:
			raise Exception(str(num)+" no es una cantidad de celdas aceptable. Ejecución terminada.")
	except Exception as e:
		print(e)
	nivel=-1
	if num==1:
		nivel=0
	elif num>1 and num < 8:
		nivel=1
	elif num>7 and num <= 19:
		nivel=2
	else:
		pass
	#return nivel
	pat_cir=ensamblar(nivel,radio)
	cord_x,cord_y=mapear_coordenadas_cartesianas(pat_cir, nivel, radio)
	cord_x=cord_x[0:num]
	cord_y=cord_y[0:num]
	return cord_x,cord_y

def prueba_interna1():
	print("-----------------------------")
	print("inicio")
	#prueba obsolote, ya no funciona
	print("-----------------------------")
	coordx,coordy=ensamblar(2,10)
	print(len(coordx))
	print(coordx)
	print(len(coordy))
	print(coordy)
	#el numero de coordenadas debe ser igual
	coordx,coordy=ensamblar(1,10)
	plt.plot(coordx,coordy, "r*")
	plt.grid(True)
	coordx,coordy=ensamblar(0,10)
	plt.plot(coordx,coordy, "go")
	plt.show()
def prueba_interna2():
	print("-----------------------------")
	print("inicio")
	print("-----------------------------")
	#solo modificar las celdas deseadas y
	#el radio.
	numero_de_coordenadas_nceldas=14
	radio=10
	coordx,coordy=coordenadas_nceldas(numero_de_coordenadas_nceldas,radio)
	print("interna")
	print(coordx)
	print(coordy)
	plt.plot(coordx,coordy, "r*")
	plt.grid(True)
	plt.show()

if __name__=="__main__":
	#Prototipo:v2
	import doctest
	#doctest.testmod()
	prueba_interna2()

	##coordx,coordy=ensamblar(nivel=2,radio=10)


else:
	print("Modulo Importado: [", os.path.basename(__file__), "]")
