import numpy as np
import math
#import pk_modelo_canal as pmodel
#import Modelo_CI_UMa as MCI

#OFDMA ayuda a capacidad del sistema pero aumenta ICI interferencia entre canales.


def OFDM():
	#definimos una banda 


	#c=3*(10^9)
	#FSPL_f_1m=20*math.log((4*math.pi*frecuencia)/c)
	#return FSPL_f_1m
def Ncanales_tx(Anchocanal,AnchoEspectro)
	
	Ncanales=AnchoEspectro/Anchocanal
	return Ncanales

def Parametros_OFDM():
	#FSLP_=float
	#Definimos banda de frecuencia a usar teniendo en cuenta el ancho del espectro asignado para estas bandas.
	# Utilizando como referencia Fc=28GHz
	#Ancho del espectro de 2.5GHz
	#
	fc="28GHz"
	if fc=="28GHz":
	GHz=1000000000
	AnchoEspectro=25*GHz
	Anchocanal=0.1*GHz
	TSimbolo=1/(2*Anchocanal)
	Tcanal=1/2()
	Bw=1/(2*Tsimbolo)
	
	Esp_portadoras_OFDM=1/Tsimbolo


	Ncanales=Ncanales_tx(Anchocanal,AnchoEspectro)
	
	Tslot()


def Tslot():







	#FSPL_= FSPL(frecuencia)	
	#PLdB=(FSPL_)+(10*alpha_n*math.log(distancia))+Sigma_Xn
	
	#return PLdB
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
	Ghz=1000000
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
