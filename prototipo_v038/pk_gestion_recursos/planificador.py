#import
import os

class Planificador:
	def __init__(self, params, no_usuarios):
		self.cfg_plan=params
		#numero de usuarios por celda
		self.no_usuarios=no_usuarios
		#output:
		self.asignacion=0 #por usuario
		self.inicializar_tipo()

	def inicializar_tipo(self):
		if self.cfg_plan["tipo"]=="rr":
			self.asignacion=self.cfg_plan["bw"][0]/self.no_usuarios
		elif self.cfg_plan["tipo"]=="estatico":
			self.asignacion=self.cfg_plan["bw"][0]
		elif self.cfg_plan["tipo"]=="arreglo":
			#procesa arreglos, gestiona pesos.
			pass
		elif self.cfg_plan["tipo"]=="futuro":
			pass
		else:
			pass

	def asignar(self):
		pass

if __name__=="__main__":
	#Prototipo:
	print("planificador")

	plan=Planificador(params, 17)
else:
	print("Modulo Importado: [", os.path.basename(__file__), "]")
