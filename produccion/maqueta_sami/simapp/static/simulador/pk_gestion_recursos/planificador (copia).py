#import
import numpy as np
import os

class Planificador:
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

	'''
	def inicializar_tipo(self):
		if self.cfg_plan["tipo"]=="rr":
			self.asignacion=self.cfg_plan["bw"][0]/self.no_usuarios
		elif self.cfg_plan["tipo"]=="estatico":
			self.asignacion=self.cfg_plan["bw"][0]
		elif self.cfg_plan["tipo"]=="arreglo":
			#procesa arreglos, gestiona pesos.
			#this
			pass
		elif self.cfg_plan["tipo"]=="futuro":
			pass
		else:
			pass

	def configurar_tipo_asignacion(self):
		#ATENCION, ESTO DEBERIA SER EN OTRA PARTE, EN TOP, O EN MODELO DE CANAL.
		#O EN GUI.
		'''Configura variables estaticas de acuerdo a la frecuencia portadora
		en el archivo de configuracion.'''

		self.cfg_plan["trama_tol"]=14
		self.cfg_plan["simb_ofdm_dl"]=10
		self.cfg_plan["frame"]=10
		self.cfg_plan["sub_ofdm"]=12

		if self.cfg_gen["portadora"][0]>150 and self.cfg_gen["portadora"][0]<=1500:
			print("frecuencia banda 900, okumura_hata")
			self.cfg_plan["bw"][0]=10 #megaherz, SELECCION 10,20,40 MHZ.
			self.cfg_plan["numerologia"]=1
			self.cfg_plan["g_bw_khz"]=845
			self.cfg_plan["n_rb_sin_gbw"]=273

			self.cfg_plan["caso_de_uso"]=['mMTC']
			#CORREGIR LOS DATOS DE ARRIBA. OK CASO DE USO.
		elif self.cfg_gen["portadora"][0]>1500 and self.cfg_gen["portadora"][0]<=3500:
			print("frecuencia banda 3.5")
			#OFDM_CP='Normal'
			#Parametro fijo para el ancho de banda del sistema
			self.cfg_plan["bw"][0]=100
			#frportadoraGHz= 3.5
			self.cfg_plan["numerologia"]=1
			self.cfg_plan["g_bw_khz"]=845
			self.cfg_plan["n_rb_sin_gbw"]=273

			self.cfg_plan["caso_de_uso"]=['URLLC','mMTC']

		elif self.cfg_gen["portadora"][0]>20000 and self.cfg_gen["portadora"][0]<=24000:
			print("frecuencia banda 20-24")
			self.cfg_plan["bw"][0]=200
			self.cfg_plan["numerologia"]=2
			self.cfg_plan["g_bw_khz"]=4930
			self.cfg_plan["n_rb_sin_gbw"]=264

			self.cfg_plan["caso_de_uso"]=['URLLC','mMTC','eBMM']


		elif self.cfg_gen["portadora"][0]>70000 and self.cfg_gen["portadora"][0]<=73000:
			print("frecuencia banda 70-73")
			self.cfg_plan["bw"][0]=400
			self.cfg_plan["numerologia"]=3
			self.cfg_plan["g_bw_khz"]=9860
			self.cfg_plan["n_rb_sin_gbw"]=264

			self.cfg_plan["caso_de_uso"]=['URLLC','mMTC','eBMM']

		else:
			try:
				raise Exception("PORTADORA NO SOPORTADA")
			except Exception as error:
				print("-----------------------------------------ERROR: {}".format(error))
		print("self.cfg_plan",self.cfg_plan)

	def calcular_tipo_asignacion(self):
		#asiganar ancho de banda en Megaherz y frecuencia portadora  con el fin de asignar la numerologia necesaria.
		#Se tiene conciencia de que para cumplir con los 264 canales es necesario elevar la frecuencia portadora.
		#el hecho es tener 264 canales maximos y eso se lleva acabo con tanto el espaciamiento entre portadoras.
		#y la cantidad de subportadoras  (15KHz*2^numerologia)*12subportadoras = 720KHz Ahora el ancho de banda del sistema
		# se divide entre la el ancho del canal, dandonos el numero maxiño de 264 canales, teniendo en cuenta la banda de guarda
		#
		# canal compartido entre 6OKhHz para hace parte del canal compartido donde se puede apreciar que puede transmitir.
		# datos con prefijo ciclico normal, se puede pensar en colocar el canal de sincronizacion con CP Extendido
		#• Temporal structure:
		#• 10 ms frame = 10 sub-frames of 1 ms
		#• 1 sub-frame = 2 slots of 0.5 ms
		#
		#• 1 slot = 7 symbols OFDM (6 symbols if extended CP)
		#numero de bloques de recursos salen de 38.104, banda de guarda 38.104
		#Considerar la cantidad de bloques de recursos utilizados por el PBCH el cual se transmite cada
		#OFDM_CP="Extendido"
		'''Asigna porcion de prbs segun parametros configurados en cfg tipo asignacion'''
		bw_con_gbw=(self.cfg_plan["bw"][0]*1000)-(2*self.cfg_plan["g_bw_khz"])
		bw_usuario=(2**self.cfg_plan["numerologia"])*15*self.cfg_plan["sub_ofdm"]
		#implementar esto de otra forma.
		no_rb=bw_con_gbw/bw_usuario
		rb_conPBCH= no_rb-22
		print("test",bw_con_gbw)
		print("planificador.asignador",no_rb, bw_usuario)


	def asignar_100mhz():

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
		#
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
	'''
	def asignar_recursos(self):
		'''Funcion que asigna ancho de banda representado en prb, a partir de la
		frecuencia portadora y otros parametros adicionales'''
		#no es posible realizar prueba debido a los parametros extra.
		pass


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
	print("test3",prueba3)

def prueba_asignar():
	"""Comprueba implementacion de funciones asignar 100,200,400 segun parametros"""
	prueba=Planificador.asignar_100mhz()


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



if __name__=="__main__":
	#Prototipo:
	print("planificador")

	#plan=Planificador(params_cfg, 17)
	#Planificador.asignar_100mhz()
	#REALIZAR PRUEBA DE F1,F2,F3
	prueba_asignar100()
	#lista_rb()
	#prueba_asignar()
else:
	print("Modulo Importado: [", os.path.basename(__file__), "]")
