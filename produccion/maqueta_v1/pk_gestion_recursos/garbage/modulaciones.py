import numpy as np
import os

class Modulacion:
	'''Clase: asigna prb por usuario, calcula matriz de interferencia.'''
	def __init__(self, params_cfg, params_cfg_gen, params):
		self.cfg_plan=params_cfg
		self.cfg_gen=params_cfg_gen
		#numero de usuarios por celda
		self.mapa_conexion=params[0]
		#self.dim_pot_r=params[1]
		#self.aux_ones_interf=np.ones(params[1])

		#output:
		self.asignacion=0 #por usuario

		#self.inicializar_tipo()

		#self.numerologia=[0,1,2,3]
		#self.cp_ofdm=['Normal','Extendido']
		#self.format_slot=['D','U','F']
		#self.case_use=['mMTC','eBMM','URLLC']

		#self.configurar_tipo_asignacion()
		#self.calcular_tipo_asignacion()
 

def modulacion_16qam():
    #Las modulaciones dependen de la SINR y la BER objetivo que se hace presente en el tipo de caso de uso a utilizar
    #cada caso de uso este especificado para soportar cierta cantidad de errores debido al tipo de servicio que se espera
    
    
    # eMBB requiere tasas de datos altas pero no especifica la confiabilidad de los datos recibidos, el tipo de informacion
    # que es enviada es considerada como datos o audio, para este caso la BER objetivo es considerada de 10**-3.
    ber_ebmm=10**(-3)
    #URLLC requiere de latencias muy bajas y control de la informacion, sopotando baja eficiencia espectral, y tiempos 
    #transmision mas cortos, razon por la cual la BER objetivo que se espera de estos servicios es mas alta, 
    #el tipo de infomacion que se espera enviar es video live stream, paquetes de datos con confiabilidad y sin retardo
    #la BER objetivo para este caso de uso considerada es de 10**-5
    ber_urllc=10**(-5)
    #mMTC es el caso de uso con menor exigencia encuanto a recursos de la red y confiabilidad de los datos, lo mas importante
    #para este caso de uso es el uso eficiente de bloques de recursos para conectar la mayor cantidad de dispositivos a la red
    #de esta manera no es necesario usar numerologias altas, la informacion que es enviada es considerada como datos  tipo texto
    #y la informacion no tiene que tener un tiempo corto de transmision corto a menos que sean datos en tiempo real, que 
    # de igual manera la latencia permitida es alta y la confiabilidad de que la informacion llegue es media, la codificacion
    # de canal y de linea darian en soporte necesario para la transmision de esta informacion, la BER objetivo considerada 
    # para este tipo de servicios tipo IoT seria de 10**-1 para servicios como M2M y D2D la BER objetivo aumenta hasta 
    #10**-3
    ber_mmtc= 10**(-1)
    '''La varianza de interferencia es considerada como el aumento de la SNR segun los bloques de recursos usados en otras 
    estaciones base, con el fin de tener una interferencia mas real a la hora de implementar el simulador, evitando el numero
    de desconexiones debido baja SINR'''
    varintf=2
    snr=8
    sinr=snr-varintf


    
    pass
def modulacion_64qam():
    pass
def modulacion_256qam():
    pass


if __name__=="__main__":
	#Prototipo:
	print("Modulacion")

	#plan=Planificador(params_cfg, 17)
	#Planificador.asignar_100mhz()
	#REALIZAR PRUEBA DE F1,F2,F3
	#lista_rb()
	#prueba_asignar()
else:
	print("Modulo Importado: [", os.path.basename(__file__), "]")


    
    
    

