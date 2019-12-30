#import
import modulo_coordenadas as mc

class Celda:

	def __init__(self, pos_x, pos_y, radio):
		#self.id=identificacion
		self.pos_x=pos_x
		self.pos_y=pos_y
		self.radio=radio
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
		self.num_celdas=num_celdas
		self.celdas=[]
		self.radio=radio
		self.x, self.y=mc.coordenadas_nceldas(self.num_celdas, self.radio)
		for x,y in zip(self.x, self.y):
			self.obj=Celda(self.x, self.y, self.radio)
			self.celdas.append(self.obj)

	def crear_coordenadas():
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
	colmena=Celdas(4,10)
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
