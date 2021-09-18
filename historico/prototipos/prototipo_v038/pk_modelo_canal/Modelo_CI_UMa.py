import numpy as np
import math
#import pk_modelo_canal as pmodel
#import Modelo_CI_UMa as MCI

#El modelo del canal tiene como parametros de entrada como frecuencia distancia, desviacon estandar
# del modelo y factores que ayudan a corregir las curvas pronosticadas por las perdidas sin tener encuenta
#un factor de desviacion, basados en las estadisticas que arrojan los modelos, estandarizamos una cierta propagacion
# concentrandonos en adquiriri los mismos resultados en perdidas, mas precisas. Para el modelo CI es menos preciso que
# el modelo ABG  por la razon de que solo tiene un parametro en correccion de distancia  el cual es llamado como la decada
# para las distancias corregidas en dB con un valor de 2.0 para Entornos UMa y 3.5 para entornos UMi.
#

class  modelocanal(object):
	"""docstring for  modelocanal"""
	def __init__(self, frecuencia):
		super( modelocanal, self).__init__()
		self.frecuencia = frecuencia
		self.distancia= distancia

#### frecuencia en  unidades de Herz
### alpha en dB valor de umi 3.5
## sigma en dB valor de 2 dB
##distancia en metros


def FSPL(frecuencia):
#frecuencia en Hz ej: 2800000000
#este modulo calcula las perdidas para una distancia de 1m para la frecuencias
	c=300000000
	res=4*math.pi/300000000
	FSPL_f_1m=20*math.log10(res*frecuencia)
	FSPL_f_1mb= -147 + 20*math.log10(frecuencia)
	#print(res)
	return FSPL_f_1m


##los valores obtimos para
def modeloci(alpha_n,distancia,Sigma_Xn,frecuencia):
	#FSLP_=float
	#Este modulo recrea las perdidas con distancia en metros con los parametros alpha_n: 3.1 y con Sigma_Xn:4
	#considerados por la documentacion valores en dB para sigma y veces para alpha_n
	FSPL_= FSPL(frecuencia)
	print(FSPL_)
	PLdB= (FSPL_)+(10*alpha_n*math.log10(self.distancia))+Sigma_Xn

	return PLdB
	#CIdB= 10*locals()

def perdidasCI(alpha_n,distancia,Sigma_Xn,frecuencia):
	PL_ci= float
	modelci=float
	modelci= FSPL(frecuencia)
	print("perdidas espacio libre :", modelci)
	PL_ci= modeloci(alpha_n,distancia,Sigma_Xn,frecuencia)
	print('Perdidas modelo CI:',PL_ci)
	pass

def perdidasdB():
	alpha_n=2
	distancia=100
	Sigma_Xn=4
	Ghz=1000000000
	frecuencia= 28*Ghz
	PL_ci= float
	modelci=float

	modelci= FSPL(frecuencia)
	print("perdidas espacio libre :", modelci)
	PL_ci= modeloci(alpha_n,distancia,Sigma_Xn,frecuencia)
	print('Perdidas modelo CI:',PL_ci)
	pass

def perdidas_okumura_hata_mhz(self):
		#outs dB
		#http://catarina.udlap.mx/u_dl_a/tales/documentos/lem/soriano_m_jc/capitulo2.pdf
		'''Funcion que calcula las perdidasd de espacio con el modelo hata 1980.
		Fuente:Empirical Formula for Propagation Loss in Land Mobile Radio Services'''
		#rangos
		#fc:150,1500 MHz
		#hb=30,200 m
		#R:1, 200 km #no es el radio, es la distancia.
		#hb=30 #m
		#alfa=0
		#hm=1.5
		hb=self.cfg_prop["params_modelo"][0]
		alfa=self.cfg_prop["params_modelo"][1] #0 si hm=1.5m
		hm=self.cfg_prop["params_modelo"][2]

		#de la forma: Lp=A+Blog10(R)

		A=69.55+(26.16*np.log10(self.portadora))-13.82*np.log10(hb)-alfa*(hm)
		B=44.9-6.55*np.log10(hb)
		E=3.2*(np.log10(11.75*hm))**2 -4.97 #[dB] para ciudades grandes y fc>300 MHz
		#E=8.29*(np.log10(1.54*hm))**2 -1.1 #[dB] para ciudades grandes y fc<300 MHz
		#print("okumura_hata, says->A,B:",A,B)
		#se guarda en un valor aparte, no es necesario, pero sirve de debug.

		if self.cfg_prop["params_desv"]["display"]:
			self.resultado_path_loss_antes=A+B*np.log10(self.distancias)-E
		self.resultado_path_loss=A+(B*np.log10(self.distancias))-E #+ self.desvanecimiento

def perdidas_umi_ci(self):
		'''Este modulo recrea las perdidas con distancia [m] frecuencia [GHz] con los parametros alpha_n: 3.1 y con Sigma_Xn:8.1 dB
		considerados por la documentacion valores en dB para sigma y veces para alpha_n
		***articulo Simulation path loss Propagation Path Loss models for 5G urban micro and macro-cellular Scenarios
		-rango de frecuencias debajo de 30GHz'''
		
		
		alpha_n=cfg_prop[3.1]
		sigma_xn=8.1
		correcion_freq_ghz=32.4+20*math.log10(self.portadora)
		correccion_dist_m=10*alpha_n*np.log10(self.distancias)
		self.resultado_path_loss=correcion_freq_ghz+correccion_dist_m+sigma_xn


	def perdidas_umi_abg(self):
		'''Este modulo recrea las perdidas con distacia [m] frecuencia [GHz] con los parametros alpha_n: 3.5 gamma : 1.9 (veces)
		-consideramos alpha y gamma como la dependencia de las perdidas en  relacion a la distancia y la frecuencia
		-Beta es un factor de correccion o compensacion de optimizacion en [dB],
		-sigma_Xn[dB]:8.0 desviacion estandar.
		***articulo Propagation Path Loss Models for 5G Urban Micro- and Macro-Cellular Scenarios✮
		-rango de frecuencias debajo de 30GHz'''
		alpha_n=3.5
		beta=24.4
		gamma=1.9
		sigma_xn=8.0
		correccion_freq_ghz=(10*gamma*math.log10(self.portadora))
		correcion_dist_m=(10*alpha_n*np.log10(self.distancias))
		self.resultado_path_loss=correccion_freq_ghz+correcion_dist_m+beta+sigma_xn


	def parametro_uma_pl(self, dist ,dist_ref,dist_3d):
		'''Falta documentar, falta corregir variables locales y globales (self.dist?)'''
		if (dist <= dist_ref) and (dist>= 10):
			path_l=28.0+22*math.log10(dist_3d)+20*math.log10(self.portadora)
		elif self.dist>disbp and dist<=5000:
			path_l=13.54+39.08*math.log10(dist_3d)+20*math.log10(self.portadora)-0.6*(Hut-1.5)
		else:
			path_l=32.4+20*log10(self.portadora)+20*log10(10)
		return path_l

if __name__=="__main__":
	#import Modelo_CI_UMa as pmci
	perdidasdB()
	#PL_ci= self.modeloci(alpha_n,distancia,Sigma_Xn,frecuencia)
	#print('Perdidas modelo CI:',Pl_ci)
	pass
else:
	print("Modulo <escribir_nombre> importado")
