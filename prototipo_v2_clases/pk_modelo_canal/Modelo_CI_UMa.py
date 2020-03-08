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

<<<<<<< HEAD

=======
class  modelocanal(object):
	"""docstring for  modelocanal"""
	def __init__(self, frecuencia):
		super( modelocanal, self).__init__()
		self.frecuencia = frecuencia
		self.distancia= distancia
			
>>>>>>> master
#### frecuencia en  unidades de Herz
### alpha en dB valor de umi 3.5
## sigma en dB valor de 2 dB 
##distancia en metros  


def FSPL(frecuencia):
<<<<<<< HEAD
	c=3*(10^9)
	FSPL_f_1m=20*math.log((4*math.pi*frecuencia)/c)
	return FSPL_f_1m

def modeloci(alpha_n,distancia,Sigma_Xn,frecuencia):
	#FSLP_=float

	FSPL_= FSPL(frecuencia)	
	PLdB=(FSPL_)+(10*alpha_n*math.log(distancia))+Sigma_Xn
=======
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
<<<<<<< HEAD
	PLdB= (FSPL_)+(10*alpha_n*math.log10(distancia))+Sigma_Xn
>>>>>>> master
=======
	PLdB= (FSPL_)+(10*alpha_n*math.log10(self.distancia))+Sigma_Xn
>>>>>>> 4e21a1d5734b5c29357b72b70e09fc4a9133bec3
	
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
if __name__=="__main__":
	#import Modelo_CI_UMa as pmci	
	perdidasdB()
	#PL_ci= self.modeloci(alpha_n,distancia,Sigma_Xn,frecuencia)
	#print('Perdidas modelo CI:',Pl_ci)
	pass
else: 
	print("Modulo <escribir_nombre> importado")
