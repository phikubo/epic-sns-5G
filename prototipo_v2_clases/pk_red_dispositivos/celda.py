#import
import modulo_coordenadas as mc

class Celda:

	def __init__(self, pos_x, pos_y, radio):
		#self.id=identificacion
		self.pos_x=pos_x
		self.pos_y=pos_y
		self.radio=radio

	def distancia_celda_usuario(params):
		pass


class Celdas:
	
	def __init__(self, nivel, num_celdas):
		#y si por el numero de cedas, calculo el nivel
		self.nivel=nivel
		self.num_celdas=num_celdas
		self.celdas=[]
		self.co=mc.ensamblar(self.nivel)
		for i in range(self.num_celdas):
			pass
			#self.obj=Celda()
			#self.celdas.append(self.obj)
			#self.individuos[i].crearGenes()
	def crear_coordenadas():
		coordenadas=[0,1,2,3,4]
		return coordenadas
	


def crear_n_objetos_lista(clase_madre, n):
	lista=[]
	for i in range(n):
		lista.append(clase_madre(id=i))


def crear_n_objetos_dict(clase_madre,n):
	celdas={}
	for i in range(n):
		nombre="celda"+str(n)
		celdas[nombre]=clase_madre(id=n)


if __name__=="__main__":
	#Prototipo:
	print("------------")
	print("Prueba Local")
	print("------------")
	#crear objeto celda
	obj_cel=Celda(0,0,5) #ok
	print("id ", id(obj_cel))
	#clase celdas crea crea celdas internas
	celulas=Celdas(0,5)
else:
	print("Modulo <escribir_nombre> importado")
