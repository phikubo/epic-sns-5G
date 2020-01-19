import matplotlib.pyplot as plt
from matplotlib.patches import RegularPolygon
import numpy as np
import math
#
try:
	from . import modulo_coordenadas as mc
	from . import modulo_circulos as mcir
except:
	print("ATENCION: Uno o mas modulos no pudo ser importado... ")
	print("...desde un archivo externo. Ignorar si la ejecucion es interna. ")

class Celda:

	def __init__(self, pos_x, pos_y, radio):
		#self.id=identificacion
		self.pos_x=pos_x
		self.pos_y=pos_y
		self.radio=radio
		self.sector_x1=0
		self.sector_x2=0
		self.sector_x3=0
		self.sector_y1=0
		self.sector_y2=0
		self.sector_y3=0
		self.usuarios=[]

	def distancia_celda_usuario(params):
		pass

	def trisectorizar():
		pass


class Celdas:
	
	def __init__(self, num_celdas, radio):
		#radio debe conocerse desde el pricipio desde que todas las celdas son simetricas
		#y si por el numero de cedas, calculo el nivel
		#self.nivel=nivel
		self.cel_fig, self.cels_ax=plt.subplots(1)
		self.num_celdas=num_celdas
		self.celdas=[]
		self.radio=radio #radio externo
		self.x, self.y=mc.coordenadas_nceldas(self.num_celdas, self.radio) #cordenadas celdas internas
		for x,y in zip(self.x, self.y):
			self.obj=Celda(self.x, self.y, self.radio)
			self.celdas.append(self.obj)


	def ver_estaciones_base(self):
		"""Permite ver las estaciones base de forma independiente"""
		plt.plot(self.x,self.y, 'b^')


	def ver_celdas(self):
		'''Funcion principal que dibuja las celdas dadas las coordenadas x,y de su centro.'''
		color="green"
		for x,y in zip(self.x, self.y):
			#pinta triangulos en los origenes de las estaciones base
			#plt.plot(x,y, 'b^')
			
			malla_hexagonal = RegularPolygon((x, y), numVertices=6, radius=self.radio,
							orientation=np.radians(30), #con 60 grados funciona perfecto, pero las coordenadas cambian. Antes 30
							facecolor=color, alpha=0.2, edgecolor='k')
							#cambiar radius=2. / 3. , cuando se usa coord_0
			self.cels_ax.add_patch(malla_hexagonal) #si no no dibuja celdas
			#self.cels_ax.scatter(0, 0, alpha=0.1) 


	def ver_sectores(self):
		"""Permite ver los sectores de forma independiente"""
		azimuts=mcir.azimut_lista(angulo_inicial=30)

		angulo_x, angulo_y =mcir.coordenadas_angulos(azimuts)

		apotema=math.sqrt(self.radio**2 -(0.5*self.radio)**2)
		apotema_trisec= self.radio/2 #relaciono el apotema tri con el radio celda grande
		radio_trisec =2*apotema_trisec* math.sqrt((4/3)) #radio a partir del apotema
		
		mcir.tri_sectorizar(angulo_x,angulo_y, radio_trisec, self.x, self.y, self.cels_ax)
		

	def ver_usuario(self):
		pass


def crear_n_objetos_lista(clase_madre, n):
	lista=[]
	for i in range(n):
		lista.append(clase_madre(id=i))


def crear_n_objetos_dict(clase_madre,n):
	celdas={}
	for i in range(n):
		nombre="celda"+str(n)
		celdas[nombre]=clase_madre(id=n)

def prueba1():
	obj_cel=Celda(0,0,5) #ok
	print("id ", id(obj_cel))
	#clase celdas crea crea celdas internas
	celulas=Celdas(0,5)
	#genera error por que 0 no es una cantidad aceptable de celdas.
def prueba2():
	#crea una colmena con 4 macroceldas.
	colmena=Celdas(19,10)
	colmena.ver_celdas()
	colmena.ver_sectores()
	#plt.savefig("dibujar19.png") #para guardar en base de datos, llamar en un nivel de archivo superior y guardar.
	plt.axis("equal")
	plt.grid(True)
	plt.show()
if __name__=="__main__":
	#Prototipo:
	print("------------")
	print("Prueba Local")
	print("------------")
	#crear objeto celda
	#clase celdas crea crea celdas internas
	import modulo_coordenadas as mc
	#import modulo_operaciones as mo
	import modulo_circulos as mcir
	prueba2()
else:
	print("Modulo celda.py importado")
