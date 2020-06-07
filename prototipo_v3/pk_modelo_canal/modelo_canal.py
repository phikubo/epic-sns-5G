#import
import numpy as np
import math
#como esto no usa submodulos, no necesito hacer try catch en esos modulos.
#en el futuro si puede ocurrir, asi que:

#try:
	#aqui van los submodulos.
#except:
	#pass

#modelo del canal incluye perdidas AWGN y RUIDO. Crear modulos awgn y ruido.
class Modelo_Canal:
	"""Clase que define el modelo del canal, calcula las perdidas del sistema. No adiciona AWGN ni Ruido."""
	def __init__(self, params_perdidas,frecuencia, params_distancia): #usar args and kwards, recibir tipo de primero, y sus parametros.
		#params_perdidas[0]:tipo de perdidas
		#params_perdidas[1]:potencia de tx
		#params_perdidas[2]:perdidas en tx
		#params_perdidas[3]:ganancia en tx
		#params_perdidas[4]:ganancia en rx
		#params_perdidas[5]:perdidas en rx
		#params_perdidas[6]:sensibilidad de todos los usuarios #en el futuro, sensibidad variable
		
		self.frecuencia=frecuencia #en gigaherz
		self.distancias, self.unidades=params_distancia
		self.params_perdidas=params_perdidas
		self.distancia_km=0
		self.tipo_perdidas=params_perdidas[0]

		self.path_loss=0
		self.resultado_balance=0
		self.resultado_margen=0
		self.inicializar_distancias_km()
		#self.inicializar_tipo()

	def inicializar_distancias_km(self):
		if self.unidades=="m" and self.tipo_perdidas=="espacio_libre":
			self.distancia_km=self.distancias/1000
		elif self.unidades=="km":
			pass

	def perdidas_espacio_libre_ghz(self):
		'''Funcion que calcula las perdidas de espacio libre en dB'''
		self.path_loss=92.4+20*np.log10(self.frecuencia)+20*np.log10(self.distancia_km)

	def balance_del_enlace_simple(self):
		'''Funcion que calcula un balance del enlace sencillo'''
		#segemento=ptx-perdidas+ganancia
		#ATENCION, DOCUMENTAR UNIDADES
		#"espacio_libre", pot_tx,loss_tx, gan_tx, gan_rx, loss_rx,sensibilidad
		#params_perdidas[0]:tipo de perdidas
		#params_perdidas[1]:potencia de tx
		#params_perdidas[2]:perdidas en tx
		#params_perdidas[3]:ganancia en tx
		#params_perdidas[4]:ganancia en rx
		#params_perdidas[5]:perdidas en rx
		#params_perdidas[6]:sensibilidad de todos los usuarios #en el futuro, sensibidad variable
		segmento_tx=self.params_perdidas[1]-self.params_perdidas[2]+self.params_perdidas[3]
		segmento_rx=self.params_perdidas[4]-self.params_perdidas[5]
		self.resultado_balance=segmento_tx-self.path_loss+segmento_rx
		#print("[mod canal] margen")
		self.resultado_margen=self.resultado_balance+self.params_perdidas[6]


	def balance_del_enlace_UMa(self):
		pass

	def balance_del_enlace_UMi(self):
		pass




def prueba_interna_path_loss():
	'''Funcion que prueba el concepto de perdidas de espacio libre con numpy'''
	freq=10 #en gigas
	distancias_km=np.array([0.1, 1, 2, 3, 4, 5, 6])
	modelo_simple=Modelo_Canal(freq, distancias_km)
	modelo_simple.perdidas_espacio_libre_ghz()
	l_bs=modelo_simple.path_loss
	print(l_bs)



if __name__=="__main__":
	#Prototipo:
	#import #aqui van los submodulos nuevamente para envitar errores

	#prueba interna 1.
	prueba_interna_path_loss()
else:
	print("Modulo <escribir_nombre> importado")
