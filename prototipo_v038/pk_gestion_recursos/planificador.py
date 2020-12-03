import numpy as np
import os

class Planificador:
	'''Clase: asigna prb por usuario, calcula matriz de interferencia.'''
	def __init__(self, params_cfg, params_cfg_gen, params):
		self.cfg_plan=params_cfg
		self.cfg_gen=params_cfg_gen
		self.mapa_conexion=params[0]
		self.dim_mapa=params[1]
		self.mapa_usuarios=params[2]
		self.max_usuario=max(self.mapa_conexion)
		#self.dim_pot_r=params[1]
		self.mapa_interf_distribuida=np.ones(params[1])
		#output:
		self.asignacion=0 #por usuario
		self.nrb_total=0
		self.nrb_total=24
		self.nrb_con_PBCH=0
		self.contador=0
		self.mapa_nrb=[]
		self.lista_distribucion=[]
		self.mapa_estado=[]
		self.mapa_interferencia=[]
		self.estado=0
		#self.calcular_tipo_asignacion()
		self.calcular_nrbs_celda()
		self.calcular_nrbs_usuarios()
		self.configurar_mapa_nrb()


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
			ress=self.nrb_total%self.max_usuario
			if ress!=0:
				self.nrb_total=self.nrb_total-ress
			else:
				pass
			self.asignacion=self.nrb_total/self.max_usuario


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

	def configurar_mapa_nrb(self):
		'''Reparte recursos C_{i}, de acuerdo al mapa de conexion de celdas.
		C_{i}, i={1,2,3,...,n_cel}, representa cada bloque de nrb entregado a cada
		usuario, de esta forma si se entrega a cada usuario 364 nrbs, C1 representa
		el bloque nrb 0-363, C2 representa el bloque nrb 364-2*363 y asi sucesivamente.'''
		#print("self.asignacion",self.asignacion)
		print("mapa", self.mapa_conexion, self.max_usuario)
		#print("usuarios",self.mapa_usuarios)
		#el estado debe cambiar solo cuando el indice cambia.
		self.contador=[0 for i in range(len(self.mapa_conexion))]
		self.contador=np.array(self.contador)
		self.estado=[0 for i in range(len(self.mapa_conexion))]
		self.estado=np.array(self.estado)

		for indd, celda in enumerate(self.mapa_usuarios):
			self.contador[celda[0]]=self.contador[celda[0]]+1
			self.estado[celda[0]]=1
			#cambio de indice.
			print(indd,self.mapa_usuarios[indd],self.contador, self.estado, "nrb_{}".format(sum(self.contador*self.estado)))
			self.mapa_estado.append(self.estado.copy())
			self.mapa_nrb.append(sum(self.contador*self.estado))
			self.estado[celda[0]]=0
			#print("nrb",mapa, " repetidos:",arreglo[0])
		#convertir a numpy
		self.mapa_nrb=np.array(self.mapa_nrb)
		self.mapa_estado=np.stack(self.mapa_estado).reshape(self.dim_mapa)

		#si piensas que esto es dificil, prueba computacion cuantica.
		for indx, mapa in enumerate(range(1,self.max_usuario+1)):
			arreglo=np.where(self.mapa_nrb==mapa)
			self.lista_distribucion.append(arreglo[0])
			##print("nrb",mapa, " repetidos:",arreglo[0])
			mapa_semilla=[0 for i in range(len(self.mapa_conexion))]

			for indxx in arreglo[0]:
				#############################print(indxx, self.mapa_estado[indxx])
				mapa_semilla=self.mapa_estado[indxx] + mapa_semilla
			#print("------>semilla",mapa_semilla)
			self.mapa_interferencia.append(mapa_semilla)
		self.mapa_interferencia=np.stack(self.mapa_interferencia)
		#self.lista_distribucion=np.stack(self.lista_distribucion)
		##print("mapa interferencia\n",self.mapa_interferencia)
		##print("mapa estados\n",self.mapa_estado)
		#print("aux\n",self.mapa_interf_distribuida)
		#print("mapa_distribucion\n", self.lista_distribucion)
		for lista, mapa_dist in zip(self.lista_distribucion, self.mapa_interferencia):
			#print(lista, mapa_dist)
			for indx_interf in lista:
				self.mapa_interf_distribuida[indx_interf]=mapa_dist
				#print(indx_interf)
		#print("mapa de usuarios iterfentes\n",self.lista_distribucion)
		#print("mapa de estados iterfentes\n",self.mapa_interferencia)
		#print("mapa distribucion\n",self.mapa_interf_distribuida)



def prueba_asignar100():
	#@@ -163,11 +124,7 @@
	print(prueba2)
	print("-----------------------------------------------Numero de bloques de recursos 400MHz ---------------")
	print("-----------------------------------------------(Cantidad de bloques de recuros , ancho de banda por RB) ---------------")
	print("test3",prueba3)

def prueba_asignar():
	"""Comprueba implementacion de funciones asignar 100,200,400 segun parametros"""
	prueba=Planificador.asignar_100mhz()


def lista_rb():
	#lista=append
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
