import matplotlib.pyplot as plt
from matplotlib.patches import RegularPolygon
import numpy as np
import math
#
#import modulo_coordenadas as mc
from . import modulo_coordenadas as mc
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
		#import modulo_coordenadas as mc
		#from . import modulo_coordenadas as mc
		self.num_celdas=num_celdas
		self.celdas=[]
		self.radio=radio
		self.x, self.y=mc.coordenadas_nceldas(self.num_celdas, self.radio)
		for x,y in zip(self.x, self.y):
			self.obj=Celda(self.x, self.y, self.radio)
			self.celdas.append(self.obj)


	def dibujar_celdas(self):
		'''Funcion principal que dibuja las celdas dadas las coordenadas x,y de su centro.'''
		color="green"
		fig, ax = plt.subplots(1)
		ax.set_aspect('equal') 

		for x,y in zip(self.x, self.y):
			#pinta triangulos en los origenes de las estaciones base
			plt.plot(x,y, 'b^')
			
			malla_hexagonal = RegularPolygon((x, y), numVertices=6, radius=self.radio,
							orientation=np.radians(30), #con 60 grados funciona perfecto, pero las coordenadas cambian. Antes 30
							facecolor=color, alpha=0.2, edgecolor='k')
							#cambiar radius=2. / 3. , cuando se usa coord_0
			ax.add_patch(malla_hexagonal) #si no no dibuja celdas
			ax.scatter(0, 0, alpha=0.1)
		

		return ax

	def tri_sectorizar(angulo_x,angulo_y, radio_ext, ax, cartesian_x, cartesian_y):
		#ax = plt.subplots(1)
		apotema_trisec= radio_ext/2 #relaciono el apotema tri con el radio celda grande
		radio_trisec =2*apotema_trisec* math.sqrt((4/3)) #radio a partir del apotema
		radio_circular=radio_trisec #paso extra, no necesario
		colores=["Red","Red","Red"]
		for cartx,carty in zip(cartesian_x, cartesian_y):
			for x,y in zip(angulo_x, angulo_y):
				color = colores[0].lower()
				hexagonal_trisec = RegularPolygon((0.5*radio_ext*x+cartx, 0.5*radio_ext*y+carty), numVertices=6, radius=radio_ext*0.5*1,
								orientation=np.radians(60), facecolor=color, alpha=0.2, edgecolor='k')
				ax.add_patch(hexagonal_trisec)
		return ax	


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
	ax=colmena.dibujar_celdas()
	#plt.savefig("dibujar19.png") #para guardar en base de datos, llamar en un nivel de archivo superior y guardar.
	#plt.show()
if __name__=="__main__":
	#Prototipo:
	print("------------")
	print("Prueba Local")
	print("------------")
	#crear objeto celda
	#clase celdas crea crea celdas internas
	prueba2()
else:
	print("Modulo celda.py importado")
