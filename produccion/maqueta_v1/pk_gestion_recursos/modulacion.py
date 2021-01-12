import numpy as np
import math
import os

class Modulacion:
	'''Clase: asigna prb por usuario, calcula matriz de interferencia.'''
	def __init__(self, params_cfg, params):
		self.cfg_plan=params_cfg
	def funcion(self):
		'''copiar'''
		pass

def asignar_tasa_modulacion(sinr_in):
    '''obtiene limites de sinr, tasa de codificaion y orden de modulacion'''
    lista_sinr_objetivo_original=[-9.533495583,-5.248540551,-0.7750688964,2.511321215,4.422894404,6.335825987,7.510369502,9.543669017,11.44647253,13.42371711,15.27114189,16.62792018,18.68554795,20.777354,22.26950728]
    lista_tasa_codificion_original=[78,193,449,378,490,616,466,567,666,772,873,711,797,885,948]
    lista_modulacion_original=[2,2,2,4,4,4,6,6,6,6,6,6,8,8,8]
	#2-qpsk
	#4-16qam
	#6-32qam
	#8-64qam

    #sinr_tar=lista_sinr_objetivo_original[3:]
    #tasa_tar=lista_tasa_codificion_original[3:]
	
    sinr_tar=lista_sinr_objetivo_original[:]
    tasa_tar=lista_tasa_codificion_original[:]
    mod_tar=lista_modulacion_original[:]
    verificar_superior=False
    for ind,sinr_ in enumerate(sinr_tar):

        if sinr_in>=22.26950728:
            print("{debug}:subir")
            verificar_superior=True
            sinr_in=22.26950727
        elif sinr_in<-9.533495583:
            sinr_in=-9.533495583
        else:
            pass

        res=sinr_-sinr_in
        if res>0:
            print("comparar",sinr_)
            print("con ", sinr_in)
            print("resta",sinr_-sinr_in)
            print("---")
            inferior=ind-1
            superior=ind
            sinr_inferior=sinr_tar[inferior]
            sinr_superior=sinr_tar[superior]
            print("indice down {}, up {}".format(inferior, superior))
            print("valores: ",sinr_inferior, sinr_superior)
            break
    #verificamos que se encuentra en el limite superior de la tabla, por tanto obtiene el mayor valor de tasa.
    if verificar_superior:
        tasa_inferior=tasa_tar[superior]
    else:
        tasa_inferior=tasa_tar[inferior]
    mod_inferior=mod_tar[inferior]
    return sinr_inferior, sinr_superior,tasa_inferior,mod_inferior

if __name__=="__main__":
	#Prototipo:
	sinr_down,sinr_up,tasa,modulacion=asignar_tasa_modulacion(sinr_in=10)
else: print("Modulo Importado: [", os.path.basename(__file__), "]")
