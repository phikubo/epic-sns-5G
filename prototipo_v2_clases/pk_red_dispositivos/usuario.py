#import

class usuario:
	
	def __init__(self, pos_x, pos_y):
		self.x=pos_x #posicion de un unico usuario
		self.y=pos_y


class usuarios:

	def __init__(self, pos_x, pos_y, radio):
		#posicion de la celda
		self.x=pos_x
		self.y=pos_y

	def mover_usuarios(self):
		pass


if __name__=="__main__":
	#Prototipo:
	pass
else:
	print("Modulo usuario.py importado")
