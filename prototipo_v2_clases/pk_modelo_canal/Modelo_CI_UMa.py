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


#### frecuencia en  unidades de Herz
### alpha en dB valor de umi 3.5
## sigma en dB valor de 2 dB 
##distancia en metros  


def FSPL(frecuencia):
	c=3*(10^9)
	FSPL_f_1m=20*math.log((4*math.pi*frecuencia)/c)
	return FSPL_f_1m

def modeloci(alpha_n,distancia,Sigma_Xn,frecuencia):
	#FSLP_=float

	FSPL_= FSPL(frecuencia)	
	PLdB=(FSPL_)+(10*alpha_n*math.log(distancia))+Sigma_Xn
	
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
