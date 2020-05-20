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
		#Distancia BS a Usuario 
		#Frecuencia portadora
		self.frecuencia=frecuencia
		self.distancia=distancia
		self.path_loss=0

	
	def perdidas_espacio_libre_ghz_1m(self):
		'''Funcion que calcula las perdidas de espacio libre en dB'''
		self.path_loss=32.4+20*math.log10(self.frecuencia)

	def perdidas_espacio_libre_ghz(self):
		'''Funcion que calcula las perdidas de espacio libre en dB'''
		self.path_loss=32.4+20*np.log10(self.frecuencia)+20*np.log10(self.distancia)

	def perdidas_umi_ci(self):
		#Este modulo recrea las perdidas con distancia [m] frecuencia [GHz] con los parametros alpha_n: 3.1 y con Sigma_Xn:8.1 dB 
		#considerados por la documentacion valores en dB para sigma y veces para alpha_n
		#articulo Simulation path loss Propagation Path Loss models for 5G urban micro and macro-cellular Scenarios
		#rango de frecuencias debajo de 30GHz
		alpha_n=3.1
		sigma_Xn=8.1
		self.perdidas_espacio_libre_ghz_1m()
		self.path_loss= self.path_loss + 10*alpha_n*np.log10(self.distancia)+sigma_Xn

	def perdidas_umi_abg(self):
		#Este modulo recrea las perdidas con distacia [m] frecuencia [GHz] con los parametros alpha_n: 3.5 gamma : 1.9 (veces)
		#consideramos alpha y gamma como la dependencia de las perdidas en  relacion a la distancia y la frecuencia
		#Beta es un factor de correccion o compensacion de optimizacion en [dB], sigma_Xn[dB]:8.0 desviacion estandar.
		#articulo Propagation Path Loss Models for 5G Urban Micro- and Macro-Cellular Scenarios✮
		#rango de frecuencias debajo de 30GHz
		alpha_n=3.5
		beta=24.4
		gamma=1.9
		Sigma_Xn=8.0
		self.path_loss=(10*alpha_n*np.log10(self.distancia))+beta+(10*gamma*math.log10(self.frecuencia))+Sigma_Xn


	def perdidas_uma_etsi(self):
		#https://www.etsi.org/deliver/etsi_tr/138900_138999/138901/15.00.00_60/tr_138901v150000p.pdf
		#Este modulo recrea las perdidas con distancia[m] y frecuencia[GHz] con los parametros 
		#distancia breakpoint: 4(Hbs-He)*(Hut-He)*fc/C 
		#rango de frecuencias para escenario UMa son por debajo de 6Ghz
		He=1.0
		Hut=1.5
		Hbs=25
		frecuenciaHz= self.frecuencia*math.pow(10,9)
		distancia3D=np.sqrt(Hbs**2+self.distancia**2)		
		distbreakpoint=(4*(Hbs-He)*(Hut-He)*frecuenciaHz)/(3*math.pow(10, 8))
		disbp=np.array(np.ones_like(self.distancia)*distbreakpoint,dtype='int32')

		print(disbp)
		print(distancia3D)
		#print(distbreakpoint)
		def parametro_uma_pl(dist,distref,dist3D):
			if (dist <= distref) and (dist>= 10):
				path_l=28.0+22*math.log10(dist3D)+20*math.log10(self.frecuencia)
			elif self.dist>disbp and dist<=5000:
				path_l=13.54+39.08*math.log10(dist3D)+20*math.log10(self.frecuencia)-0.6*(Hut-1.5)
			else:
				path_l=32.4+20*log10(self.frecuencia)+20*log10(10)
			return path_l
		pl=[ parametro_uma_pl(dist,distref,dist3D) for dist,distref,dist3D in zip(self.distancia,disbp,distancia3D)]
		self.path_loss=np.array(pl,dtype='float32')
				
def prueba_interna_path_loss():
	'''Funcion que prueba el concepto de perdidas de espacio libre con numpy'''
	freq=10 #en gigas
	distancias_km=np.array([0.1, 1, 2, 3, 4, 5, 6])
	modelo=Modelo_canal(freq, distancias_km)
	modelo.perdidas_espacio_libre_ghz()
	l_bs=modelo.path_loss
	print(l_bs)

def prueba_interna_umaetsi():

	frecu=2.6
	distancias_m=np.array([23,49,97,23,53,25,102])
	modelo=Modelo_canal(frecu,distancias_m)
	modelo.perdidas_uma_etsi()
	Pl_uma=modelo.path_loss
	print(Pl_uma)

def prueba_interna_umiagb():
	frecu=28
	distancias_m=np.array([23,49,97,23,53,25,102])
	modelo=Modelo_canal(frecu,distancias_m)
	modelo.perdidas_umi_ci()
	Pl_umiabg=modelo.path_loss
	print(Pl_umiabg)

if __name__=="__main__":
	#Prototipo:
	#import #aqui van los submodulos nuevamente para envitar errores
	
	#prueba interna 1.
	#prueba_interna_path_loss()
	#prueba_interna_umaetsi()
	prueba_interna_umiagb()

else:
	print("Modulo <escribir_nombre> importado")
