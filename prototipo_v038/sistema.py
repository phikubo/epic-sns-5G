#import - inicio
import matplotlib.pyplot as plt
from matplotlib.patches import RegularPolygon
import numpy as np
import pandas as pd
import math
import os
import time #for debug.
#
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon
#import - final
#
#bloque de carga de modulos - inicio
#
try:
	#from <paquete>          import <modulo>           as <nombre_preferencial_del modulo>
	from pk_red_dispositivos import celda
	from pk_red_dispositivos import modulo_coordenadas as mc
	from pk_red_dispositivos import modulo_ppp as ppp
	from pk_red_dispositivos import antenas as ant
	from pk_red_dispositivos import modulo_circulos as mcir
	#
	import pk_modelo_canal.modelo_canal as moca

except:
	print("ATENCION: Uno o mas modulos no pudo ser importado... ")
	print("...desde un archivo externo. Ignorar si la ejecucion es interna. ")
#
#bloque de carga de modulos - final
#
#bloque de funciones - inicio
#

'''Tarea: los parametros de entrada, se designan como: params_<name> y
son desempaquetados por la clases correspondiente'''
class Sistema_Celular:
	'''Clase que crea y controla clusters de celdas. Asigna e inicializa valores.
	Muestra graficas de las celdas deseadas.'''
	#def __init__(self, params_escenario, radio, distribucion, params_perdidas):
	def __init__(self, configuracion):
		'''Constructor por defecto. Inicializa las variables de las clases'''
		#----------------------------------------------------------------------
		#--------------------------ENTRADA-------------------------------------
		#----------------------------------------------------------------------


		self.cfg=configuracion['cfg_simulador']
		self.cfg_top=configuracion['cfg_simulador']['params_general']
		self.cfg_prop=configuracion['cfg_simulador']['params_propagacion']
		self.cfg_bal=configuracion['cfg_simulador']['params_balance']
		self.cfg_ant=configuracion['cfg_simulador']['params_antena']

		#self.cfg_top['debug']=cfg_top['debug']
		'''y si en lugar de tener self.cfg_top['debug'], se tiene cfg_top['debug']'''
		print("--------------------------inicio----------------------")
		#DECLARACION DE VARIABLES GLOBALES.
		self.cluster=[]
		self.origen_cel_x, self.origen_cel_y=mc.coordenadas_nceldas(self.cfg_top["n_celdas"],
			self.cfg_top["radio_cel"],
			self.cfg_top['debug'])
		#inicio de variables de usuarios (de todas las celdas)
		self.usuario_x=0
		self.usuario_y=0

		self.hiperc_modelo_canal=0 #modelo de canal de todos.
		self.hiperc_antena=0
		self.hiperc_distancias=[]
		self.hiperc_angulos=[]
		self.hiperc_ganancia_relativa=[]
		#falta las distancias totales?
		self.no_usuarios_total=0
		#variables para graficar la intensidad.
		self.params_malla_antena=0
		self.params_malla_perdidas=0
		self.hiperc_malla_modelo_canal=0
		self.malla_x=0
		self.malla_y=0
		self.hiperc_malla_distancias=[]
		self.hiperc_malla_angulos=[]
		self.hiperc_malla_antena=0
		self.hiperc_malla_ganancia_relativa=[]

		#auxiliar
		self.hiper_arreglos=[0, 0, 0, 0, 0, 0]
		self.hiper_malla_arreglos=[0, 0, 0, 0, 0, 0]

		#inicializa objetos tipo celda y las almacena en self.cluster
		self.inicializar_cluster_celdas()
		#crea las coordenadas de los usuarios segun una distribucion
		self.inicializar_distribucion() #falta implementar otras distribuciones: thomas cluster
		#self.usuario_x, self.usuario_y contiene los usuarios del cluster
		#Gestiona los usuarios en un hiper clustes, en coordendas, distancias y angulos.
		self.inicializar_hiperc_usuarios() #Depens_on(CONFIGURAR DIMENSION)
		#Crea la clase antena, outputs ganancia relativa.
		self.inicializar_antenas()
		print("\n--------------------------")
		self.inicializar_modelo_canal()
		print("\n--------------------------")

		time.sleep(50)

		#params_simulacion=params_simulacion.copy()
		#params_transmision=params_transmision.copy()
		#params_perdidas=params_perdidas.copy()
		#params_simulacion=[n_cel,radio_cel, distribucion, frecuencia, bw, fr, DEBUG]
		self.tipo_modelo=params_perdidas[0][0]
		self.frecuencia_operacion=str(params_simulacion[3][0])+params_simulacion[3][1]



		self.ber_sinr=3

		self.cfg_top["n_celdas"]=params_simulacion[0]
		#radio externo
		self.radio=params_simulacion[1]
		#
		#1.tupla con (intensidad, distribucion)
		#1.1 si la distribucion no tiene una intensidad, intensidad=0
		self.distribucion,self.intensidad, self.mapa_calor=params_simulacion[2]

		self.frequencia_operacion=params_simulacion[3]
		#
		self.params_perdidas=params_perdidas #"tipo", pot_tx,loss_tx, gan_tx, gan_rx, loss_rx,sensibilidad
		#
		self.params_antena=params_transmision

		#
		#----------------------------------------------------------------------
		#AUXILIAR
		#----------------------------------------------------------------------
		#Ruido térmico para un ancho de banda de 1 Hz a temperatura ambiente -174 dBm
		self.bw_usuario=params_simulacion[4]
		self.figura_ruido=params_simulacion[5]

		self.potencia_ruido=(-174.2855251)+10*np.log10(self.bw_usuario*10**6)

		#print(self.potencia_ruido, self.potencia_ruido_veces)


		#self.cel_fig, self.cels_ax=plt.subplots(1)

		#cordenadas centrales de celdas
		if self.cfg_top['debug']:
			print("[sistema.init.mc.coordenadas_nceldas]")
		self.origen_cel_x, self.origen_cel_y=mc.coordenadas_nceldas(self.cfg_top["n_celdas"], self.radio, self.cfg_top['debug'])
		#----------------------------------------------------------------------
		#SALIDA
		#----------------------------------------------------------------------



		# usuario_x
		self.modelo_canal=0 #modelo de canal unico *depleted
		self.distancias_celdas=[] #distancias unica celda *depleted



		#todas las perdidas
		self.perdidas_celdas=[]
		#OUTPUTS
		self.mapa_conexion_usuario=0
		self.mapa_conexion_estacion=[]
		self.mapa_conexion_desconexion=0
		self.sinr_db=0
		self.conexion_total=0
		self.medida_conexion=0
		#self.
		#self.probabilidad_degradacion=0
		#----------------------------------------------------------------------
		#---------------------------INICIALIZAR--------------------------------
		#----------------------------------------------------------------------
		#inicializa objetos tipo celda y las almacena en self.cluster
		#self.inicializar_cluster_celdas()

		#crea las coordenadas de los usuarios segun una distribucion
		##self.inicializar_distribucion() #falta implementar otras distribuciones: thomas cluster
		#self.usuario_x, self.usuario_y contiene los usuarios del cluster
		#Gestiona los usuarios en un hiper clustes, en coordendas, distancias y angulos.
		##self.inicializar_hiperc_usuarios() #CONFIGURAR DIMENSION
		#re dimensiona los arreglos de: hiper distancia, hiper angulos, []
		#Almacena usuarios en cada celda del cluster
		#################################################self.inicializar_cluster_usuarios()
		#Crea la clase antena, outputs ganancia relativa.
		##self.inicializar_antenas()
		#crea el modelo del mod_canal, frecuencia_central, distancias, ganancia relativa
		self.inicializar_modelo_canal() #depende de la frec y cluster_usuarios, cluster_ganancia
		#self.configurar_
		self.calcular_sinr()



	'''-----------------------------------------------------------------------------------------
	--------------------------------------------------------------------------------------------
	------------------------------------FUNCIONES DE CONFIGURACION------------------------------
				Para configurar la dimension o propiedades de los arreglos aplicados.
	--------------------------------------------------------------------------------------------
	--------------------------------------------------------------------------------------------'''

	def configurar_organizar_arreglos(self, target):
		'''Funcion que re dimensiona un arreglo de la forma [ [ [celda 1][celda2][celda3] ] [ [celda 1][celda2][celda3] ]]
		a una organizacion de usuarios por celda.
		'''
		if self.cfg_top['debug']:
			print("[sistema.configuracion_dimension_arreglos]")
		organizacion=[0 for i in range(self.cfg_top["n_celdas"])]
		temporal=[]
		#itero sobre el numero de celdas
		#print("[sistema.configurar] \n", type(target))
		#print("[sistema.configurar] \n", target)
		for target_users in range(self.cfg_top["n_celdas"]):
			#itero sobre el arreglo
			for ind,celda in enumerate(target):
				arreglo=celda[target_users]
				temporal.append(arreglo)
			#guardo los arrays en stack en una lista
			organizacion[target_users]=np.stack(temporal,axis=-1)
			#convierto la lista en ndarray para ejecutar operaciones numpy.
			organizacion=np.asarray(organizacion)
			#limpio la lista temporal para guardar la siguiente iteracion de la celdas
			temporal=[]
		#print("[sistema.debug.organizacion] \n", organizacion)
		return np.stack(organizacion)

	def configurar_disminuir_dim(self,target, *args):
		'''Realiza la conversion de dimensiones de un arreglo: retorna un arreglo de una dimension menor'''
		#depleted: not implemented.
		local_dim=target.shape

		if len(local_dim)==3:
			if args:
				target_dim=args
				new_dim=(args[0]*args[1], args[2])
				new_target=np.reshape(target,new_dim)
			else:
				new_dim=(local_dim[0]*local_dim[1], local_dim[2])
				new_target=np.reshape(target,new_dim)

		elif len(local_dim)==2:
			if args:
				target_dim=args
				new_dim=(args[0]*args[1])
				new_target=np.reshape(target,new_dim)
			else:
				new_dim=(local_dim[0]*local_dim[1])
				new_target=np.reshape(target,new_dim)

		return new_target

	def configurar_unidades_veces(self, target):
		'''Realiza la conversion de dB a veces'''
		return np.power(10, target/10)


	def configurar_limpieza(self):
		'''Limpia la memoria virtual, al borrar el valor del arreglo y dejandolo en 0.'''
		del self.hiperc_modelo_canal #modelo de canal de todos.
		del self.hiperc_antena
		del self.hiperc_distancias
		del self.hiperc_angulos
		del self.hiperc_ganancia_relativa
		del self.cluster
		#del self.usuario_x
		#del self.usuario_y


	def configurar_limpieza_parcial(self, target):
		'''limpia todos los objetos existentes en la memoria virtual'''
		for element in target:
			del element


	def configurar_limpieza_total(self):
		'''limpia todos los objetos existentes en la memoria virtual'''
		for elemento in dir():
			if element[0:2]!="__":
				del globals()[element]




	'''-----------------------------------------------------------------------------------------
	--------------------------------------------------------------------------------------------
	------------------------------------FUNCIONES DE INICIALIZACION-----------------------------
			Para inicializar instancias de clases y operar parcialmente los arreglos.
	--------------------------------------------------------------------------------------------
	--------------------------------------------------------------------------------------------'''
	def inicializar_cluster_celdas(self):
		'''Init. Almacena las instancias de celdas unicas en un cluster de celdas para control y gestion.'''
		if self.cfg_top["debug"]:
			print("[sistema.inicializar_cluster_celdas]")
		#creo objetos tipo celda y les asigno su coordenada central
		for x,y in zip(self.origen_cel_x, self.origen_cel_y):
			#creo celdas con cada coordenada x,y y las asigno a sus propias coordendas
			self.obj=celda.Celda(x,y, self.cfg_top["radio_cel"]) #aqui deberia generar las coordenadas de usuarios
			#agrupo las celdas creadas en una lista en las celdas para procesar despues
			self.cluster.append(self.obj)
		self.obj=0


	def inicializar_distribucion(self):
		'''Init. Crea coordenadas de usuario de acuerdo a una proceso de distribucion.'''
		if self.cfg_top['debug']:
			print("[sistema.inicializar_distribucion]")

		if self.cfg_top["distribucion"][1] != 0:
			if self.cfg_top["distribucion"][0]=="ppp":
				self.usuario_x, self.usuario_y=ppp.distribuir_en_celdas(
					self.cfg_top["radio_cel"],
				 	self.origen_cel_x,
					self.origen_cel_y,
					self.cfg_top["distribucion"][1],
					self.cfg_top['debug'])
				#shape es (n_celdas, n_usuarios en cada una)
				##print(np.shape(self.usuario_x))#displays shape of arrays
				##print(np.shape(self.usuario_y))
				#displays a number of objects-->IMPORTANTE
				##print("[sis.init.dist] 1. El cluster tiene ahora,", len(self.cluster), "celdas.")
				##print("[sis.init.dist] 2. Tipo de dato\n",type(self.usuario_x)) #muestra la estructura de los datos.
				##print("[sis.init.dist] 3. Logitud dato celda[0]:\n",len(self.usuario_x[0]))
				##print("[sis.init.dist] 4. Estructura de celdas\n",self.usuario_x)
				if self.cfg_top["graficar_intensidad"][0]: #si true, genera el mapa de calor.
					self.malla_x,self.malla_y=self.mapa_calor[1]
				else:
					pass

			elif self.cfg_top["distribucion"][0]=="random":
				pass
			elif self.cfg_top["distribucion"][0]=="prueba_unitaria":
				#si la intensidad es diferente de 0, y ademas la distribucion es esta, se asignan los valores.
				#print("prueba unitaria-parametros_", self.intensidad)
				self.usuario_x,self.usuario_y=self.intensidad
				#solucion, esto es una lista, debe ser numpy!

		else:
			pass


	def inicializar_cluster_usuarios(self):
		#DEPLETED.
		'''Init. Almacena coordenadas de usuarios a su respectiva celda.
		Depleted reason: Ya no es necesario que cada celda guarde informacion de sus usuarios, pues
		guarda la informacion de todos los usuarios.'''
		pass


	def inicializar_hiperc_usuarios(self):
		'''Init. crea la clase usuario en cada coordenada.'''
		if self.cfg_top['debug']: #self.cfg_top['debug']
			print("[sistema.inicializar_hiperc_usuarios]")
		self.no_usuarios_total=len(self.cluster)*len(self.usuario_x[0])
		counter=0
		for celda_unica in self.cluster:
			celda_unica.interf_user_x=self.usuario_x #todos los usuarios.
			celda_unica.interf_user_y=self.usuario_y ##todos los usuarios.

			if self.cfg_top["graficar_intensidad"][0]: #si true, then
				celda_unica.mapa_bandera=self.cfg_top["graficar_intensidad"][0]
				celda_unica.interf_malla_x=self.malla_x #todos los usuarios.
				celda_unica.interf_malla_y=self.malla_y

			celda_unica.distancia_all_estacion_base_usuarios()
			celda_unica.angulos_all_estacion_base_usuarios()
			#las dos variables siguientes, son las que originan los demas calculos.
			self.hiperc_distancias.append(celda_unica.interf_distancias)
			self.hiperc_angulos.append(celda_unica.interf_angulos)
			if self.cfg_top["graficar_intensidad"][0]:
				self.hiperc_malla_distancias.append(celda_unica.interf_malla_distancias)
				self.hiperc_malla_angulos.append(celda_unica.interf_malla_angulos)
			#rta, a cada celda, por es una instancia de clase.
			if self.cfg_top['debug']:
				print('[sistema] end of: hiperc_usuarios. Celda->',counter)
			counter+=1

		#convierto a numpy:
		self.hiperc_distancias=np.stack(self.hiperc_distancias, axis=0)
		self.hiperc_angulos=np.stack(self.hiperc_angulos, axis=0)

		self.hiperc_malla_distancias=np.array(self.hiperc_malla_distancias)
		#limpiar distancias en caso de que encuentre error por division por cero.
		self.hiperc_malla_distancias=np.where(self.hiperc_malla_distancias==0, 0.01, self.hiperc_malla_distancias)
		self.hiperc_malla_angulos=np.array(self.hiperc_malla_angulos)
		#reconfigurar.
		#print("[sistema.hiper.usuarios]\n",type(self.hiperc_distancias), type(self.hiperc_angulos))

		self.hiperc_distancias=self.configurar_organizar_arreglos(self.hiperc_distancias)
		self.hiperc_angulos=self.configurar_organizar_arreglos(self.hiperc_angulos)

		#print("[sistema.hiper.usuarios]:\n", test1,"\n", test2)
		#print(type(test1))
		#print(type(test1))
		#print("[sistema.debug]\n",self.hiperc_distancias)
		#self.hiperc_angulos=self.configurar_organizar_arreglos(self.hiperc_angulos)
		'''
		La funcion recibe todas las cordenadas de todos los usuarios en las celdas: [c1,c2,..,cn]
		con ci={xi,yi}, con xi,yi, i={1,2,...}
		'''


	def inicializar_antenas(self):
		'''Init. Crea un modelo de antena especificado. Calcula la ganancia relativa de
		un conjunto de angulos de usuario'''
		if self.cfg_top['debug']:
			print("[sistema.inicializar_antenas]")

		#hpbw=55
		#amin=20
		#ref="4g"
		#gtx=15
		#indica la orientacion de los lobulos.
		angulo_inicial=self.cfg_ant["apuntamiento"][0]
		angulo_particion=self.cfg_ant["apuntamiento"][1]
		apunt=mcir.calcular_angulo_v3(angulo_inicial,angulo_particion) #inicio,angulo de particion.
		#se adjunta luego: apunt, tar
		#parametros=[ref, hpbw, gtx, amin, apunt, self.hiperc_angulos]

		##self.params_antena.append(apunt)
		#tienen el mismo apuntamiento.
		##self.params_malla_antena=self.params_antena.copy()
		#print("[tracebak1]",self.hiperc_angulos.shape)
		###self.params_antena.append(self.hiperc_angulos)
		#print("[tracebak2]",self.params_antena[5].shape)
		#print("ant", self.params_antena)
		if self.cfg_top["debug"]:
			pass
			#time.sleep(15)
		#agrego una variable procesada del apuntamiento
		self.cfg_ant["params_ant"][0]=apunt
		#agrego la variable de ganancia de trasmision maxima:
		self.cfg_ant["params_ant"][1]=self.cfg_bal["gtx"]
		#print(self.cfg_ant)
		#time.sleep(15)
		self.hiperc_antena=ant.Antena(self.cfg_ant,self.hiperc_angulos)
		#self.hiperc_ganancia_relativa=self.hiperc_antena.hiper_ganancias #**considerar quitar

		if self.cfg_top["graficar_intensidad"][0]:

			#print("[tracebak1]",self.hiperc_angulos.shape)
			self.params_malla_antena.append(self.cfg_ant,self.hiperc_malla_angulos)
			self.hiperc_malla_antena=ant.Antena(self.cfg_ant,self.hiperc_malla_angulos)
			#self.hiperc_malla_ganancia_relativa=self.hiperc_malla_antena.hiper_ganancias


	def inicializar_modelo_canal(self):
		'''Init. Crea un modelo del canal aplicado a todo el sistema.
		 Calcula perdidas, dependiendo del tipo de modelo indicado.'''
		#diseno:
		#"tipo", pot_tx,loss_tx, gan_tx, gan_rx, loss_rx,sensibilidad
		#pasar parametros de perdidas:
		if self.cfg_top['debug']:
			print("[sistema.inicializar_modelo_canal]")
		#centralizo los arreglos en una sola variable.
		self.hiper_arreglos[0]=(self.hiperc_distancias, "m")
		self.hiper_arreglos[1]=self.hiperc_ganancia_relativa
		#Creo un modelo del canal con todas las distancias.

		#copio los parametros para no alterarlos.
		##self.params_malla_perdidas=self.params_perdidas.copy()
		#la ganacia de tx, ahora es la ganancia relativa de cada usuario.
		##self.params_perdidas[3]=self.hiperc_ganancia_relativa
		#otro modelo de canal, pero con las hiper distancias.
		self.hiperc_modelo_canal=moca.Modelo_Canal(self.cfg, self.hiper_arreglos)
		#calculo las perdidas del modelo del canal segun el tipo de modelo de propagacion
		if self.cfg_top["graficar_intensidad"][0]:
			self.hiper_malla_arrreglos[0]=(self.hiperc_malla_distancias, "m")
			self.hiper_malla_arrreglos[1]=self.hiperc_malla_ganancia_relativa
			#Creo un modelo del canal con todas las distancias.
			#otro modelo de canal, pero con las hiper distancias.
			self.hiperc_malla_modelo_canal=moca.Modelo_Canal(self.cfg, self.hiper_malla_arrreglos)


	'''-----------------------------------------------------------------------------------------
	--------------------------------------------------------------------------------------------
	------------------------------------FUNCIONES DE DESEMPEÑO------------------------------
	--------------------------------------------------------------------------------------------
	--------------------------------------------------------------------------------------------'''
	def calcular_sinr(self):
		'''Permite calcular el valor de sinr de un sistema celular.
		Procedimiento: sinr=pr/pint+pn, pr: potencia recibida maxima,
										pint: potencia interferente,
										pn: potencia de ruido.

		Si pr total en dB entonces convertir a veces.
			-seleccionar la pr maxima,
			-cambiar por 0 donde la pr fue maxima,
			-la potencia interferente es la suma de potencias del arreglo resultante
				(las que no fueron maximas),
			.
			-convertir la fr a veces.
			-calcular la potencia de ruido en veces: pn_v=ktb*fr, k: contante de boltzman, defecto: k
													t: temperatura en kelvin, defecto:290
													b: ancho de banda del canal en hz
													fr:constante, figura de ruido.
			-sinr_db=prmax_db-(10log10(pint+pn_v))
		'''
		if self.cfg_top['debug']:
			print("[sistema.calcular_sinr]")
		#creo la variable local de trabajo
		potencia_recibida_dB=self.hiperc_modelo_canal.resultado_balance

		#obtenengo las dimensiones del arreglo cluster, pues esta segmentado en 3D
		l,m,n=self.hiperc_modelo_canal.resultado_balance.shape
		#redimensiono la potencia recibida de un arreglo 3D a 2D.
		potencia_recibida_dB_2D=np.reshape(potencia_recibida_dB, (l*m, n))
		#convierto a veces
		#potencia_recibida_v_2D=(10**(potencia_recibida_dB_2D/10))
		potencia_recibida_v_2D=self.configurar_unidades_veces(potencia_recibida_dB_2D)
		print("potencia entregada (sin margen)\n", 10*np.log10(potencia_recibida_v_2D))
		#filtro y obtengo los valores de potencia recibida pr_maximo_vs en veces, de cada usuario.(seleccionar la pr maxima,)
		pr_maximo_v=np.nanmax(potencia_recibida_v_2D,axis=-1)
		print("potencia maxima a la que se conecta\n", 10*np.log10(pr_maximo_v))
		#por cada usuario, indica a cual celda recibio mayor potencia.
		indices=[]
		#auxiliar para iterar sobre todas las celdas (columnas)
		indx=0
		#itero sobre el pr_maximo_v y el array 2D

		for maxx, arr in zip(pr_maximo_v, potencia_recibida_v_2D):
			#print("componentes:\n",arr,maxx)
			#print("arreglo:\n",potencia_recibida_v_2D[indx])
			#
			#obtengo el lugar (indice) en el array donde esta el valor pr_maximo_v de potencia
			indice=np.where(arr==maxx)
			#cambiar por 0 donde la pr fue maxima,

			if len(indice[0])>1:
				#Algunos casos se obtiene valores repetidos, se escoge cualquiera.

				indice=(np.array([np.random.choice(indice[0])]),)

			#guardo el indice
			potencia_recibida_v_2D[indx][indice]=0
			indices.append(indice[0])
			indx+=1 #
		#convierto a una dimension el array.

		self.mapa_conexion_usuario=np.stack(indices)

		#sumo la cantidad de veces que la celda_i tuvo una potencia maxima.
		for cnt in range(self.cfg_top["n_celdas"]): #range numero de celdas
			self.mapa_conexion_estacion.append(np.count_nonzero(self.mapa_conexion_usuario==cnt))
		#sumo en el eje x, manteniendo la dimension, array con 0 en potencia maxima.
		suma_interf_v=np.sum(potencia_recibida_v_2D, axis=1, keepdims=True)
		print("inter",10*np.log10(suma_interf_v))

		#re definimos la dimension de la potencia, para propositos de compatibilidad de arrays.
		prx_veces=pr_maximo_v.reshape(suma_interf_v.shape)

		#convertimos la figura de ruido a veces:
		#fr_v=(10**(self.figura_ruido/10))
		fr_v=self.configurar_unidades_veces(self.figura_ruido)
		#calculamos potencia de ruido en veces.
		#pn_v=(10**(self.potencia_ruido/10))
		pn_v=self.configurar_unidades_veces(self.potencia_ruido)
		pn=pn_v*fr_v
		#calculo sinr de acuerdo a la ecuacion
		self.sinr_db=10*np.log10(prx_veces)-10*np.log10(suma_interf_v+pn)
		print("sinr\n", self.sinr_db)

		'''
		Diseño sinr de minima conexion.
		sensibidad=snr_min*pn*fr
		snr_min=sensibidad/pn*fr

		sensibidad=self.params_perdidas[6]
		sensibidad_dB=self.configurar_unidades_veces(sensibidad)
		sinr_min=sensibidad_dB/pn
		print("[debug.calcular_sinr]")
		print("sinr_min, en dB: ", 10*np.log10(sinr_min))
		print("--")
		print(pn, 10*np.log10(pn))

		Incorrecto.

		Requerimiento:
		reorganizar por celda y contabilizar.
		'''
		#self.mapa_conexion_desconexion
		#Reemplaza 1 donde sinr>12, 0 en caso contrario.
		
		self.mapa_conexion_desconexion=np.where(self.sinr_db>self.ber_sinr,1,0) #escribe 1 si true, 0 si false.
		#cuenta cuantos usuarios se conectaron.
		self.conexion_total=np.count_nonzero(self.mapa_conexion_desconexion==1)
		#calcula la probabilidad de conexion o probabilidad de exito de conexion.
		self.medida_conexion=self.conexion_total/self.no_usuarios_total
		#print((self.medida_conexion)*100) #a porcentaje

		limpiar=[potencia_recibida_dB,potencia_recibida_dB_2D,pr_maximo_v,suma_interf_v,prx_veces]
		self.configurar_limpieza_parcial(limpiar)


	'''-----------------------------------------------------------------------------------------
	--------------------------------------------------------------------------------------------
	------------------------------------FUNCIONES DE VISULAIZACION------------------------------
	--------------------------------------------------------------------------------------------
	--------------------------------------------------------------------------------------------'''

	def ver_estaciones_base(self):
		"""Permite ver las estaciones base de forma independiente"""
		#plt.plot(self.origen_cel_x,self.origen_cel_y, 'bv') #o b1
		#plt.plot(self.origen_cel_x,self.origen_cel_y, 'bv')
		self.cels_ax.plot(self.origen_cel_x,self.origen_cel_y, 'bv')


	def ver_celdas(self):
		'''Funcion principal que dibuja las celdas dadas las coordenadas x,y de su centro.'''
		color="green"
		for x,y in zip(self.origen_cel_x, self.origen_cel_y):
			#pinta triangulos en los origenes de las estaciones base
			#plt.plot(x,y, 'b^')
			malla_hexagonal = RegularPolygon((x, y), numVertices=6, radius=self.radio,
							orientation=np.radians(30), #con 60 grados funciona perfecto, pero las coordenadas cambian. Antes 30
							facecolor=color, alpha=0.2, edgecolor='k')
							#cambiar radius=2. / 3. , cuando se usa coord_0
			self.cels_ax.add_patch(malla_hexagonal) #si no no dibuja celdas
			#self.cels_ax.scatter(0, 0, alpha=0.1)


	def ver_sectores(self):
		"""Permite ver los sectores de forma independiente"""
		azimuts=mcir.azimut_lista(angulo_inicial=30)

		angulo_x, angulo_y =mcir.coordenadas_angulos(azimuts)
		#estos valores deben pertenecer a la clase
		apotema=math.sqrt(self.radio**2 -(0.5*self.radio)**2)
		apotema_trisec= self.radio/2 #relaciono el apotema tri con el radio celda grande
		radio_trisec =2*apotema_trisec* math.sqrt((4/3)) #radio a partir del apotema

		self.cels_ax=mcir.tri_sectorizar(angulo_x,angulo_y, radio_trisec, self.origen_cel_x,
		self.origen_cel_y, self.cels_ax)


	def ver_usuarios(self, *target):
		#*target ahora permite invocar la funcion con o sin parametros.
		"""Permite ver las estaciones base de forma independiente"""
		if target:
			self.cels_ax.plot(self.usuario_x[target],self.usuario_y[target], 'go')
		else:
			self.cels_ax.plot(self.usuario_x,self.usuario_y, 'go')


	def ver_usuarios_conectados(self):
		'''Permite ver usuarios conectados y no conectados'''
		coordendas_nuevas_x=self.configurar_disminuir_dim(self.usuario_x)
		coordendas_nuevas_y=self.configurar_disminuir_dim(self.usuario_y)
		for usuario, map in enumerate(self.mapa_conexion_usuario):
			thisx=coordendas_nuevas_x[usuario]
			thisy=coordendas_nuevas_y[usuario]
			if map==-1:
				self.cels_ax.plot(thisx,thisy,'k+')
			else:
				self.cels_ax.plot(thisx,thisy,'go')


	def ver_usuarios_colores(self):
		'''Permite ver los usuarios conectados a su estacion base, criterio de mayor potencia recibida'''
		#fin, poner en otra funcion.
		for usuario, (bandera, map) in enumerate(zip(self.mapa_conexion_desconexion, self.mapa_conexion_usuario)):
			#print(usuario, bandera, map)
			if bandera==0:
				#-1 donde se cumpla que sinr<12
				self.mapa_conexion_usuario[usuario]=-1

		coordendas_nuevas_x=self.configurar_disminuir_dim(self.usuario_x)
		coordendas_nuevas_y=self.configurar_disminuir_dim(self.usuario_y)

		self.mapa_conexion_desconexion=np.reshape(self.mapa_conexion_usuario, coordendas_nuevas_x.shape)
		data=pd.DataFrame({"X value":coordendas_nuevas_x, "Y value":coordendas_nuevas_y, "Category":self.mapa_conexion_desconexion})
		grupos=data.groupby("Category")
		for name, group in grupos:
			self.cels_ax.plot(group["X value"], group["Y value"], marker="o", linestyle="", label=name)
		self.cels_ax.legend()


	def ver_relacion_usuarios_originales(self):
		#*target ahora permite invocar la funcion con o sin parametros.
		"""Permite ver la relacion de usuarios de diferente color, aleatorio"""
		for x,y in zip(self.usuario_x, self.usuario_y):
			self.cels_ax.plot(x,y, c=np.random.rand(3,), ls='dotted')


	def ver_circulos(self):
		'''Permite observar los radios de las estaciones base en forma de circulo'''
		'''Definicion de la prueba
			1. radio de las Celdas
			2. coordenada de las celdas.
			3. usar modulo circulos y obtener coordendas
			4. guardar coordendas en un arrays
			5. plot'''
		for x,y in zip(self.origen_cel_x, self.origen_cel_y):
			#print(x,y)
			cx,cy=mcir.coordenadas_circulo(self.radio, [x,y])
			self.cels_ax.plot(cx,cy, 'b')


	def ver_todo(self, *args):
		"Funcion que retorna todaslas graficas."
		self.cel_fig, self.cels_ax=plt.subplots(1)
		#args: i, k, i:{1,0},k:{1,0}
		#0->self.ver_usuarios()
		#1->self.ver_usuarios_conectados
		#none->ver_usuarios_colores()
		#si, muchos usuarios, maximo de celda cual es?
		if args:
			if args[0]==1:
				self.ver_usuarios()
				if args[1]==True:
					self.ver_relacion_usuarios_originales()
			elif args[0]==2:
				self.ver_usuarios_conectados()
				if args[1]==True:
					self.ver_relacion_usuarios_originales()
			elif args[0]==3:
				self.ver_usuarios_colores()
				if args[1]==True:
					self.ver_relacion_usuarios_originales()
		else:
			 self.ver_usuarios_colores()


		self.ver_celdas()
		self.ver_estaciones_base()
		self.ver_sectores()
		self.ver_circulos()

		#no hay relacion entre los patchs y los plt.plots()
		titulo= "Esc:"+self.tipo_modelo+", F:"+self.frecuencia_operacion+", Ues:"+str(self.conexion_total)+"/"+str(self.no_usuarios_total)
		plt.title(titulo)
		plt.grid(True)
		plt.show()

	def info_celda_unica(self, target):
		'''Funcion para ver toda la información de una celda específica'''
		pass

	def info_sinr(self, *args):
		'''Permite observar numericamente los valores de sinr por usuario y celda'''
		print("[debug.calcular_sinr]")

		if args:
			if args:
				ind=0
				print("usuario |---|celda |---| sinr")
				for a,b in zip(self.mapa_conexion_usuario,self.sinr_db):
					print(ind,"      |---|",a, " |---|",b)
					ind+=1
			else:
				pass
		print("Mapa de conexion por estacion: ", self.mapa_conexion_estacion)
		print("Medida de conexion: ", self.medida_conexion)
		print("De {} usuarios, {} cumplen BER objetivo.".format(self.no_usuarios_total, self.conexion_total))


	'''------------------------------------------------------------------------------------------
	---------------------------------------------------------------------------------------------
	------------------------------------FUNCIONES DE EXPERIMENTALES------------------------------
	---------------------------------------------------------------------------------------------
	---------------------------------------------------------------------------------------------'''

	def monte_carlo(self):
		pass

	def montecarlo_hexagono(self):
		'''Funcion para probar logica de montecarlo e impacto en el sistema'''
		#procedimiento
		#1. calcular coordenadas cartesianas de la figura
		#1.2 definir la figura con shapely.Polygon
		#1.3 definir los puntos con shapely.point
		#2. definir funcion de conteo montecarlo::quiza sea necesario crear una libreria
		#3. los puntos de prueba son los usuarios del sistema, usar shapely.point o alternativa
		#4. Aplicar definicion montecarlo: usar polygon.contains(point) con todos los puntos
		#5. Obtener resultado
		#5.2 Obtener funcion acumulativa
		#6. Obtener conclusiones

		#...
		#1. De una figura centrada en 0. En este caso no interesa que este ubicada # -*- coding: utf-8 -*-
			#otra coordenada, desde que el area es la misma.

		angulos=mcir.calcular_angulo_v3(angulo_inicial=0, angulo_particion=60)
		angx_norm,angy_norm=mcir.angulos_2_cartesiano_norm(angulos)
		px_hex,py_hex=mcir.angulos_2_cartesiano(angx_norm,angy_norm,self.radio)

		#1.2. Se define la figura con los calculos anteriores
		pi=[]
		for pa,pb in zip(px_hex,py_hex):
			pi.append((pa,pb))
		polygon_hex = Polygon(pi)

		#1.3. Se define los puntos con la variable
		##print(self.usuario_x[0])
		##print(self.usuario_y[0])

		#point
		#punto=Point(self.usuario_x[0][0], self.usuario_y[0][0])
		#2,3, 4. Las tres se resumen en el siguiente procedimiento:
		puntos=[polygon_hex.contains(Point(a,b)) for a,b in zip(self.usuario_x[0], self.usuario_y[0])] #solo para celda de origen
		##print(puntos)
		##print(len(puntos)-sum(puntos)) #los falsos, pero solo necesito los verdaderos lol


		'''
		montecarlo=(area_hexagono/area_circulo), en terminos de radio, seria:
		P(x: x C Hexagono)=(area_hexagono/area_circulo)
		P(...) -> P(x: x esta contenido en Hexagono)
		Despejando el área del hexagono obtenemos:
		 -> area_hexagono= ( P(...) * pi*r**2)
		'''


		N_a=sum(puntos)
		N=len(puntos)
		P_a=N_a/N
		print("probabilidad de exito", P_a)
		print("area del hexagono: ", math.pi*self.radio**2*P_a)
		acomulativa=np.cumsum(puntos)
		print(acomulativa)
		eje_x=np.arange(1,len(puntos)+1)

		plt.plot(eje_x,acomulativa/eje_x)






#bloque de funciones - final

def prueba_interna_v3_1():
	'''Funcion de prueba para comprobar estado del sistema'''
	celdas=3
	radio=20
	intensidad=10
	distribucion=(intensidad/radio**2,"ppp") #0 en el primer valor si es otra distribucion (no necesario)
	mod_canal=None
	sc=Sistema_Celular(celdas,radio, distribucion, mod_canal)
	#print(sc.cluster[0].radio) #[ok], inicializar_cluster_celdas
	#print(sc.usuario_x) #[ok], inicializar_distribucion
	sc.ver_todo() #[ok],
	plt.axis("equal")
	plt.grid(True)
	plt.show()
	##print(sc.cluster[0].user_x) #[ok], inicializar_cluster_usuarios
	##print(sc.cluster[0].distancias) #[ok] funcion interna, distancias

def prueba_interna_v3_montecarlo():
	'''Esta funcion comprueba el funcionamiento de una simulacion sencilla de montecarlo.'''
	celdas=3
	radio=20
	intensidad=20000
	distribucion=(intensidad/radio**2,"ppp") #0 en el primer valor si es otra distribucion (no necesario)
	mod_canal=None

	sc=Sistema_Celular(celdas,radio, distribucion, mod_canal)
	#sc.ver_celdas()
	#sc.ver_usuarios()
	#sc.ver_usuarios(0) # La funcion puede definirse con o sin parametros
	#angulos=mcir.calcular_angulo_v3(angulo_inicial=0, angulo_particion=60)
	#angx_norm,angy_norm=mcir.angulos_2_cartesiano_norm(angulos)
	#x,y=mcir.angulos_2_cartesiano(angx_norm,angy_norm,radio)
	sc.montecarlo_hexagono()

	#ok.
	#plt.axis("equal")
	plt.grid(True)
	plt.show()


if __name__=="__main__":
	#Prototipo:
	#1
	prueba_interna_v3_1()
	#2
	#prueba_interna_v3_montecarlo()
	#
	#3
	#prueba_modelo_canal()
	#pass
else:
	print("Modulo Importado: [", os.path.basename(__file__), "]")

	'''Definicion de la implementacion:
	COBERTURA:
	A. Usuario como entidad principal.

	0. Definir el número de usuarios en cada celda.
	1. Obtener posicion de usuarios del cluster: self.usuario_x, self.usuario_y [[cel1], [cel2],...,[celn]]
	2. Relacionar posicion cluster celdas, con posicion cluster usuarios:
		a. En cada celda iterar en cada usuario
		b. En cada usuario calcular el balance del enlace (potencia recibida)
			1. Reutilizar inicializar_modelo_canal()
		c. En variable: mejor celda servida, seleccionar id de celda con mejor potencia recibida.
		d. Reorganizar de acuerdo al id de mejor celda servida * requerimiento para +++ capacidad.
			1. Reutilizar inicializar_cluster_usuarios() para este proposito
	3. Dimensionar el número de usuarios en cada celda. ****Ejemplo 5-10-15.
		1. Contar cuantos usuarios se han asignado
		2. Rellenar usuarios faltantes con parametros nulos.

	4. CAPACIDAD:
		B. Celdas como elemento principal.
			a. Iterar sobre los valores de las celdas.
	nota: crear cuando instancia de usuario al generar las coordenadas de distribucion o luego
	de este evento, crear los usuarios'''
