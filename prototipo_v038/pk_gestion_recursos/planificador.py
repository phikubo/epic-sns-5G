#import
import numpy as np
import os

class Planificador:
	def __init__(self, params, no_usuarios):
		self.cfg_plan=params
		#numero de usuarios por celda
		self.no_usuarios=no_usuarios
		#output:
		self.asignacion=0 #por usuario
		self.inicializar_tipo()
		self.numerologia=[0,1,2,3]
		self.cp_ofdm=['Normal','Extendido']
		self.format_slot=['D','U','F']
		self.case_use=['mMTC','eBMM','URLLC']
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


			
	def asignar_100mhz():
		#asiganar ancho de banda en Megaherz y frecuencia portadora  con el fin de asignar la numerologia necesaria.
		#Se tiene conciencia de que para cumplir con los 264 canales es necesario elevar la frecuencia portadora.
		#el hecho es tener 264 canales maximos y eso se lleva acabo con tanto el espaciamiento entre portadoras.
		#y la cantidad de subportadoras  (15KHz*2^numerologia)*12subportadoras = 720KHz Ahora el ancho de banda del sistema 
		# se divide entre la el ancho del canal, dandonos el numero maxiño de 264 canales, teniendo en cuenta la banda de guarda
		#
		#
		#
		# canal compartido entre 6OKhHz para hace parte del canal compartido donde se puede apreciar que puede transmitir.
		# datos con prefijo ciclico normal, se puede pensar en colocar el canal de sincronizacion con CP Extendido 
		#• Temporal structure:
		#• 10 ms frame = 10 sub-frames of 1 ms
		#• 1 sub-frame = 2 slots of 0.5 ms

		#• 1 slot = 7 symbols OFDM (6 symbols if extended CP) 
		#numero de bloques de recursos salen de 38.104, banda de guarda 38.104
		#Considerar la cantidad de bloques de recursos utilizados por el PBCH el cual se transmite cada 
		#OFDM_CP="Extendido"
		OFDM_CP='Normal'
		bwmhz=100#Parametro fijo para el ancho de banda del sistema 
		frportadoraGHz= 3.5
		num=1
		g_bw_khz=845
		n_rb_sin_gbw=273
		sub_ofdm=12
		case_use_100mhz= ['URLLC','mMTC']
		trama_tol=14
		simb_ofdm_dl=10
		frame=10
		bw_con_gbw=(bwmhz*1000) - (2*g_bw_khz) 
		bw_usuario=(2**num)*15*sub_ofdm
		no_rb=bw_con_gbw/bw_usuario
		rb_conPBCH= no_rb-22
		
		return no_rb, bw_usuario 
		


	def asignar_200Mhz():
		#asiganar ancho de banda en Megaherz y frecuencia portadora  con el fin de asignar la numerologia necesaria.
		#Se tiene conciencia de que para cumplir con los 264 canales es necesario elevar la frecuencia portadora.
		#el hecho es tener 264 canales maximos y eso se lleva acabo con tanto el espaciamiento entre portadoras.
		#y la cantidad de subportadoras  (15KHz*2^numerologia)*12subportadoras = 720KHz Ahora el ancho  
		OFDM_CP='Normal'
		bwmhz=200#Parametro fijo para el ancho de banda del sistema 
		frportadoraGHz= 24
		num=2
		g_bw_khz= 4930
		n_rb_sin_gbw=264
		sub_ofdm=12
		case_use_200mhz= ['URLLC','mMTC','eBMM']
		trama_tol=14
		simb_ofdm_dl=10
		frame=10
		bw_con_gbw=(bwmhz*1000) - (2*g_bw_khz) 
		bw_usuario=(2**num)*15*sub_ofdm
		no_rb=bw_con_gbw/bw_usuario
		
		return no_rb, bw_usuario 
	
	def asignar_400mhz():
		#
		OFDM_CP='Normal'
		bwmhz=400#Parametro fijo para el ancho de banda del sistema 
		frportadoraGHz= 73
		num=3
		g_bw_khz= 9860
		n_rb_sin_gbw=264
		sub_ofdm=12
		case_use_400mhz= ['URLLC','mMTC','eBMM']
		trama_tol=14
		simb_ofdm_dl=10
		frame=10
		bw_con_gbw=(bwmhz*1000) - (2*g_bw_khz) 
		bw_usuario=(2**num)*15*sub_ofdm
		no_rb=bw_con_gbw/bw_usuario
		
		return no_rb, bw_usuario 


def prueba_asignar100():

	#prueba=Planificador(param, 17)
	prueba=Planificador.asignar_100mhz()
	prueba2=Planificador.asignar_200Mhz()
	prueba3=Planificador.asignar_400mhz()
	print("-----------------------------------------------Numero de bloques de recursos 100MHz ---------------")
	print("-----------------------------------------------(Cantidad de bloques de recuros , ancho de banda por RB) ---------------")
	print(prueba)
	print("-----------------------------------------------Numero de bloques de recursos 200MHz ---------------")
	print("-----------------------------------------------(Cantidad de bloques de recuros , ancho de banda por RB) ---------------")
	print(prueba2)
	print("-----------------------------------------------Numero de bloques de recursos 400MHz ---------------")
	print("-----------------------------------------------(Cantidad de bloques de recuros , ancho de banda por RB) ---------------")
	print(prueba3)


def lista_rb():
	#lista=append
	no_usuarios=[1,2,3,4,5,6,7,8]
	size_usuarios=len(no_usuarios)
	dt_usuarios=Planificador.asignar_100mhz()
	no_rb_usuarios=dt_usuarios[0]/size_usuarios


	print("-----------------------------------------------pruebas estructura de la trama para 100MHz---------------")
	print("Numero de usuarios",size_usuarios)
	print('Numero de bloques de recursos por usuario',no_rb_usuarios)

	m_rb=np.array(range(1,int(dt_usuarios[0]))).reshape(int(size_usuarios),int(no_rb_usuarios))
	m_usuarios=np.array(range(1,8))
	print("-----------------------------------------------(distribucion bloques de recursos por numero de usuario) ---------------")
	print(m_rb)
	#
	

	pass


if __name__=="__main__":
	#Prototipo:
	print("planificador")

	#plan=Planificador(params, 17)
	#Planificador.asignar_100mhz()
	#REALIZAR PRUEBA DE F1,F2,F3
	prueba_asignar100()
	lista_rb()
else:
	print("Modulo Importado: [", os.path.basename(__file__), "]")
