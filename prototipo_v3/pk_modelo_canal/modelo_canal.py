#import
import numpy as np
import math
#como esto no usa submodulos, no necesito hacer try catch en esos modulos.
#en el futuro si puede ocurrir, asi que:

#try:
	#aqui van los submodulos.
#except:
	#pass


class Modelo_canal:
	"""Clase que define el modelo del canal, calcula las perdidas del sistema"""
	def __init__(self, frecuencia, distancia):
		self.frecuencia=frecuencia
		self.distancia=distancia
		self.path_loss=0


	def perdidas_espacio_libre_ghz(self):
		'''Funcion que calcula las perdidas de espacio libre en dB'''
		self.path_loss=32.4+20*np.log10(self.frecuencia)+20*np.log10(self.distancia)

	def perdidas_umi_ci(self):
		#Este modulo recrea las perdidas con distancia en metros con los parametros alpha_n: 3.1 y con Sigma_Xn:8.1 dB 
		#considerados por la documentacion valores en dB para sigma y veces para alpha_n
		#articulo Simulation path loss Propagation Path Loss models for 5G urban micro and macro-cellular Scenarios
		alpha_n=3.1
		sigma_Xn=8.1
		fspl=perdidas_espacio_libre_ghz()
		self.path_loss= fspl + 10*alpha_n*math.log10(self.distancia)+sigma_Xn
def prueba_interna_path_loss():
	'''Funcion que prueba el concepto de perdidas de espacio libre con numpy'''
	freq=10 #en gigas
	distancias_m=np.array([0.1, 1, 2, 3, 4, 5, 6])
	modelo=Modelo_canal(freq, distancias_km)
	modelo.perdidas_espacio_libre_ghz()
	l_bs=modelo.path_loss
	print(l_bs)



if __name__=="__main__":
	#Prototipo:
	#import #aqui van los submodulos nuevamente para envitar errores
	
	#prueba interna 1.
	prueba_interna_path_loss()
else:
	print("Modulo <escribir_nombre> importado")
