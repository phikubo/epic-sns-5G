import matplotlib.pyplot as plt
from matplotlib.patches import RegularPolygon
import numpy as np
import math
import os

try:
	pass
except:
	print("ATENCION: Uno o mas modulos no pudo ser importado... ")
	print("...desde un archivo externo. Ignorar si la ejecucion es interna. ")

class Celda:
	'''Clase que modela una unica celda'''
	def __init__(self, pos_x, pos_y, radio):
		#self.id=identificacion
		#posicion de la celda
		self.pos_x=pos_x
		self.pos_y=pos_y
		#
		self.radio=radio
		#
		#coordenadas de los sectores
		self.sector_x1=0
		self.sector_x2=0
		self.sector_x3=0
		self.sector_y1=0
		self.sector_y2=0
		self.sector_y3=0
		#
		#cordenadas de los usuarios...considerar si pertenecen a la celda
		self.user_x=0
		self.user_y=0##################
		#
		#array de distancias del centro a todos los usuarios
		self.distancias=0
		#Array de perdidas de propagaion hacia cada usuario
		self.basic_path_loss=0
		#
		self.frecuencia=0


	def distancia_gnodeb_ue(self):
		'''Funcion que calcula la distancia entre la posicion del gnodeb hasta cada ue.'''
		#Procedimiento
		#0 al ejecutar esta funcion, la celda ya debe tener la informacion
		# de posicion de su centro y usuarios
		#1 preparar variables pos_x,pos_y y user_x, user_y
		#distancia=vector numpy
		self.distancias=np.sqrt((self.pos_x-self.user_x)**2+(self.pos_y-self.user_y)**2)

	def asignar_perdidas_espacio_libre(self, perdidas):
		'''Funcion que asigna las perdidas basicas, con un parametro externo'''
		self.basic_path_loss=perdidas


	def trisectorizar():
		pass


def prueba_interna_v3_1():
	pass


if __name__=="__main__":
	#Prototipo:
	print("------------")
	print("Prueba Local")
	print("------------")
else:
	print("Modulo Importado: [", os.path.basename(__file__), "]")
