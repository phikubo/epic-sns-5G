import matplotlib.pyplot as plt
from matplotlib.patches import RegularPolygon
import numpy as np
import math
#
try:
	from . import modulo_coordenadas as mc
	from . import modulo_circulos as mcir
	from . import usuario as ues
	from . import modulo_ppp as ppp
except:
	print("ATENCION: Uno o mas modulos no pudo ser importado... ")
	print("...desde un archivo externo. Ignorar si la ejecucion es interna. ")

class Celda:

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
		self.usuarios=[]

	def distancia_celda_usuario(params):
		pass

	def trisectorizar():
		pass


class Celdas:
	
	def __init__(self, num_celdas, radio, distribucion):
		#radio debe conocerse desde el pricipio desde que todas las celdas son simetricas
		#y si por el numero de cedas, calculo el nivel
		#self.nivel=nivel
		self.distribucion, self.intensidad=distribucion
		self.cel_fig, self.cels_ax=plt.subplots(1)
		self.num_celdas=num_celdas
		self.celdas=[]
		self.radio=radio #radio externo
		self.x, self.y=mc.coordenadas_nceldas(self.num_celdas, self.radio) #cordenadas celdas internas
		#asigno coordenadas a cada objeto
		for x,y in zip(self.x, self.y):
			self.obj=Celda(self.x, self.y, self.radio) #aqui deberia generar las coordenadas de usuarios
			self.celdas.append(self.obj)
		#
		#
		self.us_x=0
		self.us_y=0
		#
		if self.distribucion=="ppp":
			self.us_x, self.us_y=ppp.distribuir_en_celdas(self.radio, self.x, self.y, self.intensidad)


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
		#estos valores deben pertenecer a la clase
		apotema=math.sqrt(self.radio**2 -(0.5*self.radio)**2)
		apotema_trisec= self.radio/2 #relaciono el apotema tri con el radio celda grande
		radio_trisec =2*apotema_trisec* math.sqrt((4/3)) #radio a partir del apotema
		
		mcir.tri_sectorizar(angulo_x,angulo_y, radio_trisec, self.x, self.y, self.cels_ax)
		

	def ver_usuarios(self):
		"""Permite ver las estaciones base de forma independiente"""
		plt.plot(self.us_x,self.us_y, 'go')
	

	def ver_todo(self):
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
	numero_celdas=1
	radio=100
	intensidad=5
	colmena=Celdas(numero_celdas, radio, distribucion=("ppp",intensidad/radio**2))
	colmena.ver_celdas()
	colmena.ver_sectores()
	colmena.ver_estaciones_base()
	colmena.ver_usuarios()
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
	import usuario as ues
	import modulo_ppp as ppp
	prueba2()
else:
	print("Modulo celda.py importado")
