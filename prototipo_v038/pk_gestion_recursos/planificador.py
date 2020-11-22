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
		self.max_mapa=max(self.mapa_conexion)
		#self.dim_pot_r=params[1]
		#self.aux_ones_interf=np.ones(params[1])
		#output:
		self.asignacion=0 #por usuario
		self.nrb_total=0
		self.nrb_total=24
		self.nrb_con_PBCH=0
		#self.calcular_tipo_asignacion()
		self.calcular_nrbs_celda()
		self.calcular_nrbs_usuarios()



	def to_khz(self,target):
		'''return variable in khz'''
		return target*10**3

	def to_mhz(self,target):
		'''return variable in Mhz'''
		return target*10**6

	def calcular_nrbs_celda(self):
		'''Calcula el numero de prbs por cada celda, de acuerdo a numerologia y ancho de banda'''
		#http://www.techplayon.com/nr-resource-block-definition-and-rbs-calculation/
		#https://www.rfwireless-world.com/calculators/5G-NR-maximum-throughput-calculator.html
		#https://5g-tools.com/5g-nr-throughput-calculator/
		#https://apkpure.com/nr-5g-prb-and-data-rate-calculator/com.instinctcoder.nr5gthecal
		delta_bw=(2*self.cfg_plan["numerologia"]*self.to_khz(15))
		#15khz es lo minimo.
		one_resource_block=self.cfg_plan["sub_ofdm"]*delta_bw
		nrb_sin_gbw=self.to_mhz(self.cfg_plan["bw"][0])-2*self.to_khz(self.cfg_plan["bw_guarda"][0])
		nrb=np.floor(nrb_sin_gbw/one_resource_block)

		if self.cfg_plan["pbch"]:
			self.nrb_con_PBCH=nrb-22
			self.nrb_total=self.nrb_con_PBCH*self.cfg_plan["trama_total"]
		else:
			self.nrb_total=nrb*self.cfg_plan["trama_total"]



	def calcular_nrbs_usuarios(self):
		'''Funcion que asigna ancho de banda representado en prb, a partir de la
		frecuencia portadora y otros parametros adicionales'''
		if self.cfg_plan["tipo"]=="rr":
			ress=self.nrb_total%self.max_mapa
			if ress!=0:
				self.nrb_total=self.nrb_total-ress
			else:
				pass
			self.asignacion=self.nrb_total/self.max_mapa
			print("self.asignacion",self.asignacion)
			print("mapa", self.mapa_conexion, self.max_mapa)


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
