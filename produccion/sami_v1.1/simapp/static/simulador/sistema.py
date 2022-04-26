#import - inicio
import matplotlib.pyplot as plt
from matplotlib.patches import RegularPolygon
import numpy as np
import pandas as pd
import math
import os
import time #for debug.

try:
	print("From sistema.py")
	#from <paquete>          import <modulo>           as <nombre_preferencial_del modulo>
	from .pk_red_dispositivos import celda
	from .pk_red_dispositivos import modulo_coordenadas as mc
	from .pk_red_dispositivos import modulo_ppp as ppp
	from .pk_red_dispositivos import antenas as ant
	from .pk_red_dispositivos import modulo_circulos as mcir
	#
	#import pk_modelo_canal.modelo_canal as moca
	#import pk_gestion_recursos.planificador as plan
	from .pk_modelo_canal import modelo_canal as moca
	from .pk_gestion_recursos import planificador as plan
	from .pk_gestion_recursos import modulacion as modd

except Exception as EX:
	print("ATENCION: Uno o mas modulos no pudo ser importado... {}\n".format(EX))
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
		self.cfg_gen=configuracion['cfg_simulador']['params_general']
		self.cfg_prop=configuracion['cfg_simulador']['params_propagacion']
		self.cfg_bal=configuracion['cfg_simulador']['params_balance']
		self.cfg_ant=configuracion['cfg_simulador']['params_antena']
		self.cfg_plan=configuracion['cfg_simulador']['params_asignacion']

		if self.cfg_gen['debug']:
			print("[ok].debug: simulacion creada.")

		#DECLARACION DE VARIABLES GLOBALES.
		self.radio_distribucion=self.cfg_gen["radio_cel"]
		self.cfg_gen["radio_cel"]=(2/3)*self.cfg_gen["isd"]*math.sqrt(3)/2
		if self.cfg_gen["geometria"]=="autoajustable":
			self.radio_distribucion=self.cfg_gen["radio_cel"]
		else:
			#manual, se ajusta al parametro existente en radio_cel, antes de cambiar.
			pass

		self.cluster=[]
		self.origen_cel_x, self.origen_cel_y=mc.coordenadas_nceldas(self.cfg_gen["n_celdas"],
			self.cfg_gen["radio_cel"],
			self.cfg_gen['debug'])
		#inicio de variables de usuarios (de todas las celdas)
		self.usuario_x=0
		self.usuario_y=0

		#HIPERCLUSTER
		self.hiperc_modelo_canal=0 #modelo de canal de todos.
		self.hiperc_antena=0
		self.hiperc_distancias=[]
		self.hiperc_angulos=[]
		#self.hiperc_ganancia_relativa=[]
		#falta las distancias totales?
		self.no_usuarios_total=0
		self.no_usuarios_celda=0
		
		#GRAFICA DE POTENCIA RECIBIDA EN PRESIM
		#variables para graficar la intensidad.
		self.params_malla_antena=[]
		self.params_malla_perdidas=0
		self.hiperc_malla_modelo_canal=0
		self.malla_x=0
		self.malla_y=0
		self.hiperc_malla_distancias=[]
		self.hiperc_malla_angulos=[]
		self.hiperc_malla_antena=0
		self.hiperc_malla_ganancia_relativa=[]

		#auxiliar
		#guarda el modelo de asignacion de tasa y modulacion.
		self.modelo_modulacion=0 
		self.hiper_arreglos=[0, 0, 0, 0, 0, 0]
		self.hiper_malla_arreglos=[0, 0, 0, 0, 0, 0]

		self.potencia_ruido=0
		self.bw_usuario=0

		#OUTPUTS
		self.mapa_conexion_usuario=0
		self.mapa_celda_mayor_potencia=0
		self.mapa_conexion_estacion=[]
		#tiene en cuenta los usuarios no conectados
		self.mapa_conexion_usuario_no_con=0
		#tiene en cuenta los usuarios no conectados
		self.mapa_conexion_estacion_no_con=[]
		self.mapa_conexion_desconexion=0 #sinr.
		self.mapa_conexion_desconexion_margen=0
		#
		self.pr_maximo_v=0
		self.pr_maximo_dB=0
		self.margen_maximo_dB=0
		self.sinr_db=0
		self.conexion_total_sinr=0
		self.medida_conexion_sinr=0
		self.medida_conexion_margen=0

		self.matriz_interferente=0

		self.throughput_sistema=0
		self.throughput_users=0

		#inicializa objetos tipo celda y las almacena en self.cluster
		self.inicializar_cluster_celdas()
		
		#crea las coordenadas de los usuarios segun una distribucion
		self.inicializar_distribucion() #falta implementar otras distribuciones: thomas cluster. La dimension de los arreglos depende del numero de celdas, por tanto
		#el arreglo de usuarios es de:  [ [us11 us12 us13, ...] [us21 us22 us23, ...] [us31 us32 us33, ...], [...usij] ].

		#self.usuario_x, self.usuario_y contiene los usuarios del cluster
		#Gestiona los usuarios en un hiper clustes, en coordendas, distancias y angulos.
		self.inicializar_hiperc_usuarios() #Depens_on(CONFIGURAR DIMENSION)

		#Crea la clase antena, outputs ganancia relativa.
		self.inicializar_antenas()

		#crea el modelo del mod_canal, frecuencia_central, distancias, ganancia relativa
		self.inicializar_modelo_canal() #retorna pathloss
		#inicializa el efecto del ancho de banda, segun parametros fijos o procesamiento de alguna variable, eg. potencia recibida.

		#instancia de modulacion, no asigna modulacion.
		self.inicializar_modulacion()

		#calculo de celda de mayor potencia.
		self.calcular_celda_mayor_potencia_upgrade()
		
		#el margen de senbilidad se calcula en la misma funcion de asignacion de recursos
		#self.calcular_medida_margen_upgrade()
		self.inicializar_asignacion_bw_nrbs_upgrade() #se obtiene ancho de frecuencia, y matriz de potencia en veces filtrada por uso de recursos.
		
		#calcular interfencia
		self.calcular_interferencia_sinr_upgrade()
		
		#calcular throughput
		self.calcular_throughput_upgrade()





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
		if self.cfg_gen['debug']:
			print("[sistema.configuracion_dimension_arreglos]")
		organizacion=[0 for i in range(self.cfg_gen["n_celdas"])]
		temporal=[]
		#itero sobre el numero de celdas
		for target_users in range(self.cfg_gen["n_celdas"]):
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

	def configurar_unidades_dB(self,target):
		'''Realiza la conversion de veces a dB'''
		return 10*np.log10(target)


	def configurar_limpieza(self):
		'''Limpia la memoria virtual, al borrar el valor del arreglo y dejandolo en 0.'''
		del self.hiperc_modelo_canal #modelo de canal de todos.
		del self.hiperc_antena
		del self.hiperc_distancias
		del self.hiperc_angulos
		del self.hiperc_ganancia_relativa
		del self.cluster



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
		if self.cfg_gen["debug"]:
			print("[sistema.inicializar_cluster_celdas]")
		#creo objetos tipo celda y les asigno su coordenada central
		for x,y in zip(self.origen_cel_x, self.origen_cel_y):
			#creo celdas con cada coordenada x,y y las asigno a sus propias coordendas
			self.obj=celda.Celda(x,y, self.cfg_gen["radio_cel"]) #aqui deberia generar las coordenadas de usuarios
			#agrupo las celdas creadas en una lista en las celdas para procesar despues
			self.cluster.append(self.obj)
		self.obj=0





	def inicializar_distribucion(self):
		'''Init. Crea coordenadas de usuario de acuerdo a una proceso de distribucion.'''
		if self.cfg_gen['debug']:
			print("[sistema.inicializar_distribucion]")

		if self.cfg_gen["distribucion"][1] != 0:
			if self.cfg_gen["distribucion"][0]=="ppp":
				self.usuario_x, self.usuario_y=ppp.distribuir_en_celdas(
					self.radio_distribucion,
				 	self.origen_cel_x,
					self.origen_cel_y,
					self.cfg_gen["distribucion"][1],
					self.cfg_gen['debug'])
				#shape es (n_celdas, n_usuarios en cada una)
				if self.cfg_gen["imagen"]["display"][0]: #si true, genera el mapa de calor.
					#[!!!!] mapa_calor_x, mapa_calor_y se produce y se guarda en simulador.
					with open('simapp/static/simulador/base_datos/datos/mapa_calor_x.npy', 'rb') as archivo_npy:
						self.malla_x=np.load(archivo_npy)

					with open('simapp/static/simulador/base_datos/datos/mapa_calor_y.npy', 'rb') as archivo_npy:
						self.malla_y=np.load(archivo_npy)
				else:
					pass

			elif self.cfg_gen["distribucion"][0]=="random":
				pass
			elif self.cfg_gen["distribucion"][0]=="prueba_unitaria":
				#si la intensidad es diferente de 0, y ademas la distribucion es esta, se asignan los valores.
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
		if self.cfg_gen['debug']: #self.cfg_gen['debug']
			print("[sistema.inicializar_hiperc_usuarios]")
		self.no_usuarios_total=len(self.cluster)*len(self.usuario_x[0])
		self.no_usuarios_celda=len(self.usuario_x[0])
		counter=0
		for celda_unica in self.cluster:
			celda_unica.interf_user_x=self.usuario_x #todos los usuarios.
			celda_unica.interf_user_y=self.usuario_y ##todos los usuarios.

			if self.cfg_gen["imagen"]["display"][0]: #si true, then
				celda_unica.mapa_bandera=self.cfg_gen["imagen"]["display"][0]
				celda_unica.interf_malla_x=self.malla_x #todos los usuarios.
				celda_unica.interf_malla_y=self.malla_y

			celda_unica.distancia_all_estacion_base_usuarios()
			celda_unica.angulos_all_estacion_base_usuarios()
			#las dos variables siguientes, son las que originan los demas calculos.
			self.hiperc_distancias.append(celda_unica.interf_distancias)
			self.hiperc_angulos.append(celda_unica.interf_angulos)
			if self.cfg_gen["imagen"]["display"][0]:
				self.hiperc_malla_distancias.append(celda_unica.interf_malla_distancias)
				self.hiperc_malla_angulos.append(celda_unica.interf_malla_angulos)
			#rta, a cada celda, por es una instancia de clase.
			if self.cfg_gen['debug']:
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

		'''
		La funcion recibe todas las cordenadas de todos los usuarios en las celdas: [c1,c2,..,cn]
		con ci={xi,yi}, con xi,yi, i={1,2,...}
		'''


	def inicializar_antenas(self):
		'''Init. Crea un modelo de antena especificado. Calcula la ganancia relativa de
		un conjunto de angulos de usuario'''
		if self.cfg_gen['debug']:
			print("[sistema.inicializar_antenas]")

		#hpbw=55
		#amin=20
		#ref="4g"
		#gtx=15
		#indica la orientacion de los lobulos.
		angulo_inicial=self.cfg_ant["apuntamiento"][0]
		angulo_particion=self.cfg_ant["apuntamiento"][1]
		apunt=mcir.calcular_angulo_v3(angulo_inicial,angulo_particion) #inicio,angulo de particion.
		#misma version que el anterior, solo que v3 incluye el angulo de particion.
		#azimuts=mcir.azimut_lista(angulo_inicial=30)
		#se adjunta luego: apunt, tar
		#parametros=[ref, hpbw, gtx, amin, apunt, self.hiperc_angulos]

		if self.cfg_gen["debug"]:
			pass

		#agrego una variable procesada del apuntamiento, cambia el apuntamiento de la antena.
		#solo funciona para aquellas que han sido configuradas 3 sectorizadas.
		self.cfg_ant["params_ant"][0]=apunt
		#agrego la variable de ganancia de trasmision maxima:
		self.cfg_ant["params_ant"][1]=self.cfg_bal["gtx"]

		self.hiperc_antena=ant.Antena(self.cfg,self.hiperc_angulos)

		if self.cfg_gen["imagen"]["display"][0]:
			self.params_malla_antena.append(self.cfg_ant)
			self.params_malla_antena.append(self.hiperc_malla_angulos)
			self.hiperc_malla_antena=ant.Antena(self.cfg,self.hiperc_malla_angulos)
			#self.hiperc_malla_ganancia_relativa=self.hiperc_malla_antena.hiper_ganancias


	def inicializar_modelo_canal(self):
		'''Init. Crea un modelo del canal aplicado a todo el sistema.
		 Calcula perdidas, dependiendo del tipo de modelo indicado.'''
		#diseno:
		#"tipo", pot_tx,loss_tx, gan_tx, gan_rx, loss_rx,sensibilidad
		#pasar parametros de perdidas:
		if self.cfg_gen['debug']:
			print("[sistema.inicializar_modelo_canal]")

		#todas las variables en megaherz para evitar errores
		if self.cfg_gen["portadora"][1]=="ghz":
				#convierto a megaherz, por la ecuacion, si ya esta en megaherz, pass
				self.cfg_gen["portadora"][0]=self.cfg_gen["portadora"][0]*1000
				self.cfg_gen["portadora"][1]="mhz"
		else:
			pass

		#centralizo los arreglos en una sola variable.
		self.hiper_arreglos[0]=(self.hiperc_distancias, "m") #siempre en metros.
		self.hiper_arreglos[1]=self.hiperc_antena.hiper_ganancias
		
		#Creo un modelo del canal con todas las distancias.
		#la ganacia de tx, ahora es la ganancia relativa de cada usuario.
		#otro modelo de canal, pero con las hiper distancias.
		self.hiperc_modelo_canal=moca.Modelo_Canal(self.cfg, self.hiper_arreglos)
		#calculo las perdidas del modelo del canal segun el tipo de modelo de propagacion
		if self.cfg_gen["imagen"]["display"][0]:
			self.hiper_malla_arreglos[0]=(self.hiperc_malla_distancias, "m")
			self.hiper_malla_arreglos[1]=self.hiperc_malla_antena.hiper_ganancias
			#Creo un modelo del canal con todas las distancias.
			#otro modelo de canal, pero con las hiper distancias.
			self.hiperc_malla_modelo_canal=moca.Modelo_Canal(self.cfg, self.hiper_malla_arreglos)




	def inicializar_asignacion_bw_nrbs(self):
		'''Permite gestionar el recurso de ancho de banda sobre los usuarios en cada celda'''
		mapa_estaciones=self.mapa_conexion_estacion.copy()
		dim_pr_v2D=self.potencia_recibida_v_2D.shape
		mapa_usuarios=self.mapa_conexion_usuario.copy()
		mapa_margen_descon=self.mapa_conexion_desconexion_margen.copy() #check pls
		mapa_usuarios_descon=self.mapa_conexion_usuario_no_con.copy()
		mapa_estaciones_descon=self.mapa_conexion_estacion_no_con.copy()
		

		params_asignacion=[mapa_estaciones,dim_pr_v2D, mapa_usuarios, mapa_margen_descon,
			mapa_usuarios_descon, mapa_estaciones_descon]
		self.planificador=plan.Planificador(self.cfg_plan, self.cfg_gen, params_asignacion)#por sector, etc.
		#ancho de banda se convierte en variable y depende de cuantos prb obtiene.
		self.bw_usuario=self.planificador.asignacion
		#convierte la matriz de potencia recibida en matriz de interferencia.
		self.matriz_interferente=self.potencia_recibida_v_2D*self.planificador.mapa_interf_distribuida

	

	def inicializar_asignacion_bw_nrbs_upgrade(self):
		'''Asigna ancho de banda a los usuarios disponibles.
		1. Cuando la funcion se ejecuta por primera vez, todos los usuarios se asignan equitativamente.
		2. Cuando la funcion se ejecuta iterativamente, los usuarios se redistribuyen.
		
		Si el numero de celdas es impar y el numero de usuarios tambien, la distribucion rr no es equitativa 
		pues sobran recursos. Estos deben asignarse al usuario cuya potencia sea la mayor.'''
		mapa_asignacion_xcelda=self.mapa_celda_mayor_potencia.copy()
		mapa_asignacion_xpotencia=self.pr_maximo_dB.copy()
		#mapa_asignacion_mayor_potencia=
		dim_pr_v2D=self.potencia_recibida_v_2D.shape
		#estoas valores se usan para saber donde esta el usuario con mayor potencia. DEPLETED
		indices_mayor_potencia = np.where(self.pr_maximo_dB == np.amax(self.pr_maximo_dB))
		
		
		indice_mayor_pot=int(np.array([np.random.choice(indices_mayor_potencia[0])]))

		params_asignacion=[mapa_asignacion_xcelda, dim_pr_v2D, indice_mayor_pot, mapa_asignacion_xpotencia]
		self.planificador=plan.Planificador(self.cfg_plan, self.cfg_gen, params_asignacion, upgrade=True)#por sector, etc.
		#ancho de banda se convierte en variable y depende de cuantos prb obtiene.
		self.bw_usuario=self.planificador.asignacion_bw
		#convierte la matriz de potencia recibida en matriz de interferencia.
		#print("sistem.py: potencia_rec_2d",self.potencia_recibida_v_2D)
		'''En este punto se considera que todos los usuarios generan interferencia unos con otros'''
		self.matriz_interferente=self.potencia_recibida_v_2D*self.planificador.mapa_interf_distribuida
		
		self.conexion_total_margen=np.count_nonzero(self.planificador.mapa_conexion_usuario_binario==1)
		#calcula la probabilidad de conexion o probabilidad de exito de conexion.
		self.medida_conexion_margen=self.conexion_total_margen/self.no_usuarios_total


	def inicializar_modulacion(self):
		'''Crea un modelo de modulacion indicando el escenario y parametros de configuracion.'''
		self.modelo_modulacion=modd.Modulacion(0,"5G", 0)



	'''-----------------------------------------------------------------------------------------
	--------------------------------------------------------------------------------------------
	------------------------------------FUNCIONES DE DESEMPEÑO------------------------------
	--------------------------------------------------------------------------------------------
	--------------------------------------------------------------------------------------------'''

	def calcular_medida_margen(self):
		'''DEPLETED
		Permite calcular el valor de conexion del margen del balance del enlace'''

		margen_dB=self.hiperc_modelo_canal.resultado_margen
		#obtenengo las dimensiones del arreglo cluster, pues esta segmentado en 3D
		#print("test1", margen_dB)
		l,m,n=margen_dB.shape
		#redimensiono la potencia recibida de un arreglo 3D a 2D.
		margen_dB_2D=np.reshape(margen_dB, (l*m, n))
		self.margen_maximo_dB=np.nanmax(margen_dB_2D,axis=-1)
		self.mapa_conexion_desconexion_margen=np.where(self.margen_maximo_dB>0,1,0)
		
		#si multiplico lo anterior por el mapa de conexion, pero	
		#	con -1 donde esta el 0, obtengo el mapa de desconexion final.
			#para alterar el array:
				#0 donde 1
				#-1 donde 0
				#procedemos a la suma.
					#razon: donde existe 0, al multiplicar se obtiene 0
					#	si se suma, entonces convierto a numero negativo.
		#cuento las veces que los usuarios superaron el margen.
		self.conexion_total_margen=np.count_nonzero(self.mapa_conexion_desconexion_margen==1)
		#calcula la probabilidad de conexion o probabilidad de exito de conexion.
		self.medida_conexion_margen=self.conexion_total_margen/self.no_usuarios_total
		#print("\nUsuarios conectados: {} %\n ".format(self.medida_conexion_margen*100))



	def calcular_celda_mayor_potencia(self):
		'''Prepara arreglos a utilizar en funcion de calculo sinr.'''
		if self.cfg_gen['debug']:
			print("[sistema.calcular_celda_mayor_potencia]")
	
		#creo la variable local de trabajo
		potencia_recibida_dB=self.hiperc_modelo_canal.resultado_balance
		#obtenengo las dimensiones del arreglo cluster, pues esta segmentado en 3D
		#l,m,n=self.hiperc_modelo_canal.resultado_balance.shape
		#redimensiono la potencia recibida de un arreglo 3D a 2D.
		#potencia_recibida_dB_2D=np.reshape(potencia_recibida_dB, (l*m, n))
		potencia_recibida_dB_2D=np.vstack(potencia_recibida_dB)
		#convierto a veces
		#potencia_recibida_v_2D=(10**(potencia_recibida_dB_2D/10))
		self.potencia_recibida_v_2D=self.configurar_unidades_veces(potencia_recibida_dB_2D)
		#filtro y obtengo los valores de potencia recibida self.pr_maximo_vs en veces, de cada usuario.(seleccionar la pr maxima,)
		self.pr_maximo_v=np.nanmax(self.potencia_recibida_v_2D,axis=-1)
		self.pr_maximo_dB=self.configurar_unidades_dB(self.pr_maximo_v)
		#por cada usuario, indica a cual celda recibio mayor potencia.
		indices=[]
		#auxiliar para iterar sobre todas las celdas (columnas)
		indx=0
		#itero sobre el self.pr_maximo_v y el array 2D
		for maxx, arr in zip(self.pr_maximo_v, self.potencia_recibida_v_2D):
			#obtengo el lugar (indice) en el array donde esta el valor self.pr_maximo_v de potencia
			indice=np.where(arr==maxx)
			#cambiar por 0 donde la pr fue maxima,
			#si exite tupla en indice[0], varios valores son iguales en la misma columna.
			if len(indice[0])>1:
				#Algunos casos se obtiene valores repetidos, se escoge cualquiera.
				indice=(np.array([np.random.choice(indice[0])]),)
			#guardo el indice
			self.potencia_recibida_v_2D[indx][indice]=0
			indices.append(indice[0])
			indx+=1 #
		#convierto a una dimension el array.
		self.mapa_conexion_usuario=np.stack(indices)
		#redimensiono arreglo de margen
		self.mapa_conexion_desconexion_margen=self.mapa_conexion_desconexion_margen.reshape(self.mapa_conexion_usuario.shape)
		#sumo la cantidad de veces que la celda_i tuvo una potencia maxima.
		for cnt in range(self.cfg_gen["n_celdas"]): #range numero de celdas
			###print("[!1-test",self.mapa_conexion_desconexion_margen)
			self.mapa_conexion_estacion.append(np.count_nonzero(self.mapa_conexion_usuario==cnt))
		#necesario para crear cuenta de usuarios conectados por celda.
		self.mapa_conexion_usuario_no_con=np.where(self.mapa_conexion_desconexion_margen==0,-1, self.mapa_conexion_usuario)
		#self.mapa_conexion_usuario_no_con=np.where(self.mapa_conexion_desconexion_margen==0,-1, 1)

		for cnt in range(self.cfg_gen["n_celdas"]): #range numero de celdas
			#mapa de las estaciones sin contar las no conectadas.
			self.mapa_conexion_estacion_no_con.append(np.count_nonzero(self.mapa_conexion_usuario_no_con==cnt))
		#relaciono el indice con la matriz de margen, si value<0, marcar con -1, sino, pass
			#en una nuevo arreglo
		#realizr nuevamente el conteo.



	def calcular_celda_mayor_potencia_upgrade(self):
		'''Calculo de usuario conectado a una celda especifica dependiendo de su pathloos'''
		#self.distancias_2D=np.vstack(self.hiperc_distancias)
		potencia_recibida_dB=self.hiperc_modelo_canal.resultado_balance
		#obtenengo las dimensiones del arreglo cluster, pues esta segmentado en 3D>
		'''potencia_recibida_dB -> A_m_u_c. (magnitud:usuario a celda, #usuarios, #celdas)'''
		#l,m,n=self.hiperc_modelo_canal.resultado_balance.shape

		#redimensiono la potencia recibida de un arreglo 3D a 2D.
		#potencia_recibida_dB_2D=np.reshape(potencia_recibida_dB, (l*m, n)) #misma operacion que np.vstack*()
		potencia_recibida_dB_2D=np.vstack(potencia_recibida_dB)
		
		#conviersion a veces
		self.potencia_recibida_v_2D=self.configurar_unidades_veces(potencia_recibida_dB_2D)

		#filtro y obtengo los valores de potencia recibida self.pr_maximo_vs en veces, de cada usuario.(seleccionar la pr maxima,)
		self.pr_maximo_v=np.nanmax(self.potencia_recibida_v_2D,axis=-1)

		#conversion a dB.
		self.pr_maximo_dB=self.configurar_unidades_dB(self.pr_maximo_v)
		#por cada usuario, indica a cual celda recibio mayor potencia.
		indices_map=[]
		#auxiliar para iterar sobre todas las celdas (columnas)
		indx=0
		#itero sobre el self.pr_maximo_v y el array 2D
		for maxx, arr in zip(self.pr_maximo_v, self.potencia_recibida_v_2D):
			#obtengo el lugar (indice) en el array donde esta el valor self.pr_maximo_v de potencia
			indice=np.where(arr==maxx)
			#cambiar por 0 donde la pr fue maxima,
			#si exite tupla en indice[0], es decir existen dos valores iguales de un usuario a diferentes celdas, varios valores son iguales en la misma columna.
			if len(indice[0])>1:
				#Algunos casos se obtiene valores repetidos, se escoge cualquiera.
				indice=(np.array([np.random.choice(indice[0])]),)
			#limpio el arreglo de potencia de recibida para el calculo de interferencias.
			self.potencia_recibida_v_2D[indx][indice]=0
			#guardo el indice
			indices_map.append(indice[0])
			indx+=1 #
		#conversion tipo de indices a numpy stack.
		self.mapa_celda_mayor_potencia=np.stack(indices_map)

		#todos los usuarios son asigandos a una celda.
		#sin embargo, aun no es posible determinar si los usuarios asignados, no tienen servicio.



	def calcular_mapas_conexion(self):
		#DEPLETED
		'''Permite calcular un mapa que indica cuales usuarios han sido desconectados'''
		#self.mapa_conexion_usuario_no_con=np.where(self.mapa_conexion_desconexion_margen==0,-1, 1)
		pass


	def calcular_interferencia_sinr_upgrade(self):
		'''Calcula la interferencia producida por la distribucion de prbs e SINR.
		Permite calcular el valor de sinr de un sistema celular.
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
		#falta inicializar asignacion
		#de acuerdo a los resultados de asignacion, valores de potencia se cancelan
		#sumar las potencias interferentes en cada columna.
		suma_interf_v=np.sum(self.matriz_interferente, axis=1, keepdims=True)
		#re definimos la dimension de la potencia, para propositos de compatibilidad de arrays.
		prx_veces=self.pr_maximo_v.reshape(suma_interf_v.shape)
		#convertimos la figura de ruido a veces:
		fr_v=self.configurar_unidades_veces(self.cfg_gen["nf"][0])

		#bw en que unidades debe estar?
		#self.potencia_ruido=(-174.2855251)+10*np.log10(self.bw_usuario*10**6)

		#debe estar en hz
		self.potencia_ruido=(-174.2855251)+10*np.log10(self.bw_usuario)
		#calculamos potencia de ruido en veces.
		pn_v=self.configurar_unidades_veces(self.potencia_ruido)
		pn=pn_v*fr_v
		#calculo sinr de acuerdo a la ecuacion
		self.sinr_db=10*np.log10(prx_veces)-10*np.log10(suma_interf_v+pn)
		#limpio los valores de sinr de los  usuarios sin conexion.
		#self.sinr_db=np.where(self.mapa_conexion_desconexion_margen==0,-100, self.sinr_db)
		#Reemplaza 1 donde sinr>,self.cfg_gen["ber_sinr"] 0 en caso contrario.
		self.mapa_conexion_desconexion=np.where(self.sinr_db>self.cfg_gen["ber_sinr"],1,0) #escribe 1 si true, 0 si false.

		#cuenta cuantos usuarios se conectaron.
		self.conexion_total_sinr=np.count_nonzero(self.mapa_conexion_desconexion==1)
		#calcula la probabilidad de conexion o probabilidad de exito de conexion.
		self.medida_conexion_sinr=self.conexion_total_sinr/self.no_usuarios_total

		limpiar=[suma_interf_v,prx_veces,fr_v,pn,pn_v]
		self.configurar_limpieza_parcial(limpiar)

		#https://www.rfwireless-world.com/calculators/5G-NR-TBS-Calculation.html

		#EL RADIO DE LA CELDA CREA ESPACIOS NO LINEALES.
		#COREGIR POR ISD. Corregido
	


	def calcular_throughput_upgrade(self):
		'''Dado un sinr calcula el throughput de un arreglo, usando un modulo externo y no una clase.'''
		#calcular tasa y modulacion.
		self.modelo_modulacion.arreglos_tasa_modulacion(self.sinr_db)
		tasa=np.vstack(np.array(self.modelo_modulacion.arr_tasa))
		modulacion=np.vstack(np.array(self.modelo_modulacion.arr_modulacion))
		#
		#print(tasa[:10], modulacion[:10])
		constant_dmrs=13
		constant_oh=[0.14,0.18]
		#OPCION MODIFICABLE SOLO EN MODO DESARROLLADOR.
		arreglo_mimo=1
		factor_escala=[1,0.8,0.75,0.4]

		#
		constant_simbolos_ofdm=14
		unidades_megabits=10**(-3)
		#["params_asignacion"]
		trama_segundos=unidades_megabits/(constant_simbolos_ofdm*2**self.planificador.numerologia)
		completo_oh=(1-constant_oh[1])
		#n_ofdm=12
		#n_rb=100 #map
		#sinr_in=10 #
		#sym_ofdm=12 #map
		#scs_ofdm=12 #map
		
		check_list=[arreglo_mimo,modulacion,factor_escala[0], tasa, self.planificador.nrb_usuario, self.cfg_plan["sub_ofdm"], trama_segundos,completo_oh]
		
		#limpiar modulacion para quitar negativos. El resultado final solo tiene en cuenta los valores contribuyentes
		modulacion_0=np.vstack(np.where(modulacion<0,0, modulacion))

		#de lo contrario, cuando tasa<0, modulacion<0; throughput>0 para cuando el valor no debe contribuir.
		#para evitar este error, se fija la modulacion siempre positiva independientemente de la contribuci[on] puesto que tasa ya contiene la informacion que representa los valores no contribuyentes
		throughput_users=10**(-6)*arreglo_mimo*modulacion_0*factor_escala[0]*(tasa/1024)*(self.planificador.nrb_usuario.copy()*self.cfg_plan["sub_ofdm"]/trama_segundos)*completo_oh
		self.throughput_users=np.absolute(throughput_users)	
		#promedio por sistema []
		self.throughput_sistema=np.mean(self.throughput_users)
		



	def calcular_throughput(self):
		'''Dado un sinr calcula el throughput de un arreglo, usando un modulo externo y no una clase.'''
		#calcular tasa y modulacion.
		self.modelo_modulacion.arreglos_tasa_modulacion(self.sinr_db)
		tasa=np.array(self.modelo_modulacion.arr_tasa)
		modulacion=np.array(self.modelo_modulacion.arr_modulacion)
		#
		constant_dmrs=13
		constant_oh=[0.14,0.18]
		#OPCION MODIFICABLE SOLO EN MODO DESARROLLADOR.
		arreglo_mimo=1
		factor_escala=[1,0.8,0.75,0.4]

		#
		constant_simbolos_ofdm=14
		unidades_megabits=10**(-3)
		trama_segundos=unidades_megabits/(constant_simbolos_ofdm*2**self.cfg_plan["numerologia"])
		completo_oh=(1-constant_oh[1])
		#n_ofdm=12
		#n_rb=100 #map
		#sinr_in=10 #
		#sym_ofdm=12 #map
		#scs_ofdm=12 #map
		
		check_list=[arreglo_mimo,modulacion,factor_escala[0], tasa, self.planificador.nrb_usuario, self.cfg_plan["sub_ofdm"], trama_segundos,completo_oh]

		#limpiar modulacion para quitar negativos. El resultado final solo tiene en cuenta los valores contribuyentes
		modulacion_0=np.where(modulacion<0,0, modulacion)
		#de lo contrario, cuando tasa<0, modulacion<0; throughput>0 para cuando el valor no debe contribuir.
		#para evitar este error, se fija la modulacion siempre positiva independientemente de la contribuci[on] puesto que tasa ya contiene la informacion que representa los valores no contribuyentes
		throughput_users=10**(-6)*arreglo_mimo*modulacion_0*factor_escala[0]*(tasa/1024)*(self.planificador.nrb_usuario*self.cfg_plan["sub_ofdm"]/trama_segundos)*completo_oh
		self.throughput_users=np.absolute(throughput_users)	
		#promedio por sistema []
		self.throughput_sistema=np.mean(self.throughput_users)
		
		#promedio por celdas [a,b,c, ..., N]
		#build a dictionary like this
		'''
		{
			"1":[usr1, usr 4, usrs6]
			"2":[usr2, usr3, usr5]
		}
		so, for each cel number, we have mean data.
		'''

		#imprimer los primers 10 valores de tp y mapa de usuarios desconectados.
		#for a,b in zip(self.throughput_users[:10], self.mapa_conexion_usuario_no_con[:10]):
		#	print("{}	{} {} {} {}".format(b, a, a*-1, abs(a), int(a)))
		
			
		
		#info_data tiene la respuesta de la siguiente manera.
		#listo los valores de througput de cada usuario
		#1 obtener mapa binario de no conexion
		#2 multiplicar mapa binario no con con throput users.
		#3 sumar resultado para obtener mean
		#4 sumar resultados por celda.
		#5 con el mapa de no con, obtener porcentaje

		


	'''-----------------------------------------------------------------------------------------
	--------------------------------------------------------------------------------------------
	------------------------------------FUNCIONES DE VISULAIZACION------------------------------
	--------------------------------------------------------------------------------------------
	--------------------------------------------------------------------------------------------'''


	def ver_imagen_potencia(self, nombre):
		'''Permite ver la imagen creada a partir de una malla de puntos'''
		#el primer valor
		pr_max=self.hiperc_malla_modelo_canal.resultado_balance.copy()
		#prmax no fue re configurado por que el procedimiento de calculo es diferente, los usuarios no pertenecen a una celda.
		#en cambio se hace como si todos los usuarios pertenecieran a cada celda de manera independiente:
		"""
		arr=[
			[usuario 1, u2, ...,un] #celda 1
			 
			[usuario 1, u2, ...,un] #celda 2

			[usuario 1, u2, ...,un] #celda 3
		]"""
		pr_max=np.vstack(np.transpose(np.reshape(pr_max, self.hiperc_malla_distancias.shape)))
		final_pr_max=[]
		for line in pr_max:
			final_pr_max.append(np.max(line))
		final_pr_max=np.transpose(np.reshape(final_pr_max, self.malla_x.shape))		
		final_pr_max=np.reshape(final_pr_max,self.malla_x.shape)
		z_min,z_max=-np.abs(pr_max).max(), np.abs(pr_max).max()
		fig,ax=plt.subplots()

		c=ax.pcolormesh(np.vstack(self.malla_x),np.vstack(self.malla_y),final_pr_max, cmap='plasma', vmin=z_min, vmax=-42)
		fig.colorbar(c,ax=ax, label="Potencia Recibida [dBm]")
		titulo="{}, Ptx:{}, Desvanecimiento:{}.".format(str(self.cfg_prop["modelo_perdidas"]), self.cfg_bal["ptx"], self.cfg_prop["params_desv"]["tipo"])
		plt.title(titulo)
		plt.xlabel("Distancia [m]")
		plt.ylabel("Distancia [m]")
		 
		plt.grid(True)
		ruta="simapp/static/simulador/base_datos/imagenes/presim/{}.png".format(nombre)
		plt.savefig(ruta)
		#plt.savefig("simapp/static/simulador/base_datos/imagenes/mapa_calor.png")

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
			malla_hexagonal = RegularPolygon((x, y), numVertices=6, radius=self.cfg_gen["radio_cel"],
							orientation=np.radians(30), #con 60 grados funciona perfecto, pero las coordenadas cambian. Antes 30
							facecolor=color, alpha=0.2, edgecolor='k')
							#cambiar radius=2. / 3. , cuando se usa coord_0
			self.cels_ax.add_patch(malla_hexagonal) #si no no dibuja celdas
			#self.cels_ax.scatter(0, 0, alpha=0.1)


	def ver_sectores(self):
		"""Permite ver los sectores de forma independiente"""
		azimuts=mcir.azimut_lista(angulo_inicial=30)

		angulo_x, angulo_y=mcir.coordenadas_angulos(azimuts)
		#estos valores deben pertenecer a la clase
		apotema=math.sqrt(self.cfg_gen["radio_cel"]**2 -(0.5*self.cfg_gen["radio_cel"])**2)
		apotema_trisec= self.cfg_gen["radio_cel"]/2 #relaciono el apotema tri con el radio celda grande
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
		#[ 0 0 0 1 1 1 2 2 2]
		self.mapa_conexion_estacion=self.planificador.mapa_conexion_celda
		#[1,2,3]
		self.mapa_conexion_usuario=self.mapa_celda_mayor_potencia
		#for usuario, (bandera, mapa_conexion_usuario) in enumerate(zip(self.mapa_conexion_desconexion, self.mapa_conexion_usuario)):
		for usuario, (bandera, mapa_conexion_usuario) in enumerate(zip(self.mapa_conexion_estacion, self.mapa_conexion_usuario)):
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
			cx,cy=mcir.coordenadas_circulo(self.radio_distribucion, [x,y])
			self.cels_ax.plot(cx,cy, 'b')


	def ver_todo(self, *args):
		"Funcion que retorna todas las graficas."
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
		titulo= "Esc:"+str(self.cfg_prop["modelo_perdidas"])+", F:"+str(self.cfg_gen["portadora"][0])+", Ues:"+str(self.conexion_total_sinr)+"/"+str(self.no_usuarios_total)
		plt.title(titulo)
		plt.xlabel("Distancia [m]")
		plt.ylabel("Distancia [m]")
		plt.grid(True)
		#plt.savefig("simapp/static/simulador/base_datos/imagenes/simulacion.png")
		#plt.show()
		#plt.grid(True)
		nombre="base-sim"
		ruta="simapp/static/simulador/base_datos/imagenes/presim/{}.png".format(nombre)
		plt.savefig(ruta)


	def info_celda_unica(self, target):
		'''Funcion para ver toda la información de una celda específica'''
		pass

	def info_data(self, *args):
		'''Permite observar numericamente los valores de sinr por usuario y celda.
		Usage: info_data(True/False, 10)->args[0]:True/False, args[1]:10 is the limit of displaying tabl'''
		#CORREGIR
		

		self.mapa_conexion_usuario=self.mapa_celda_mayor_potencia.copy()
		self.mapa_conexion_usuario_no_con=self.planificador.mapa_conexion_usuario_binario.copy()
		self.margen_maximo_dB=self.planificador.margen_dB.copy()

		#self.sinr_db=np.zeros(self.mapa_conexion_usuario.shape)
		#self.throughput_users=np.zeros(self.mapa_conexion_usuario.shape)
		print("-----------")
		#print("[info_data] {}".format(args))
		if self.cfg_gen['debug']:
			print("\n-----[debug.calcular_sinr]:")
		print("\n------------------------------------------[info_data]:")
		#is args==True

		#calculo de distancia, donde el usuario se ha conectado finalmente. Revisar si es consistente.
		self.distancias_2D=np.vstack(self.hiperc_distancias)
		self.distancias_2D=np.array([ar[ids] for ar, ids in zip(self.distancias_2D,self.mapa_conexion_usuario)])
		if args:
			if args:
				ind=0
				titulos_display=["celda","conexion", "distancias", "pr_max","margen","sinr","througput"]
				arreglos_display=np.column_stack((self.mapa_conexion_usuario, self.mapa_conexion_usuario_no_con,self.distancias_2D,
						self.pr_maximo_dB,self.margen_maximo_dB,self.sinr_db, self.throughput_users))
				df_display = pd.DataFrame(arreglos_display, columns=titulos_display)
				print(df_display.head(), "\n...\n",df_display.tail())
			else:
				pass
		
		print("\n------------------------------------------[info_data].\n")


	def info_distancia(self,*args):
		'''Permite observar la potencia recibida por usuario, y de diferentes fuentes.'''
		print("[info_distancia]")
		#print(self.hiperc_distancias)
		print("**************************************************\n")


	def info_angulos(self,*args):
		'''Permite observar la potencia recibida por usuario, y de diferentes fuentes.'''
		print("[info_angulos]")
		#print(self.hiperc_angulos)
		print("**************************************************\n")

	def info_ganancia(self,*args):
		'''Permite observar la potencia recibida por usuario, y de diferentes fuentes.'''
		print("[info_ganancia]")
		#print(self.hiperc_ganancia_relativa)
		print("**************************************************\n")

	def info_potencia(self,*args):
		'''Permite observar la potencia recibida por usuario, y de diferentes fuentes.'''
		print("[info_potencia_con_desv]")
		#print(self.hiperc_modelo_canal.balance_simplificado)
		print("**************************************************\n")

	def info_potencia_sin(self,*args):
		'''Permite observar la potencia recibida por usuario, y de diferentes fuentes.'''
		print("[info_potencia_sin_desv]")
		#print(self.hiperc_modelo_canal.balance_simplificado_antes)
		print("**************************************************\n")

	def info_balance(self,*args):
		'''Permite observar la potencia recibida por usuario, y de diferentes fuentes.'''
		print("[info_balance]")
		#print(self.hiperc_modelo_canal.resultado_balance)
		print("**************************************************\n")

	def info_planificador(self,*args):
		'''Permite observar las informacion contenida en el planificador.'''
		print("[info_planificador]")
		print("indice	descon	cel_descon	celda	contador	estado		nrb")
		for contenido in self.planificador.info_variables:
			print(contenido)
		print("**************************************************\n")

	def info_general(self, *target):
		'''Permite observar parametros generales de cada simulacion.'''
		print("------------")
		#print("info_general: {}".format(target))
		target=target[0]
		if target =="potencia":
			print("[info_potencia]")
			#print(self.hiperc_modelo_canal.resultado_balance)
		elif target=="distancia":
			print("[info_distancia]")
			#print(self.hiperc_distancias)
		elif target=="angulos":
			print("[info_angulos]")
			#print(self.hiperc_angulos)
		elif target=="ganancia":
			print("[info_ganancia]")
			#print(self.hiperc_ganancia_relativa)
		elif target=="general":
			#print("\n------------------------------------------[info_general]:")
			#print("Celdas:",self.cfg_gen["n_celdas"])
			#print("Usuarios por Conexion Sinr, supera {} dB un {}% celda".format(self.cfg_gen['ber_sinr'],self.no_usuarios_celda))
			#print("Semilla inicial de usuarios por celda: {}". format(self.no_usuarios_celda))
			#print("Usuarios totales por sistema",self.no_usuarios_total)
			#print("Ancho de banda por usuario:",self.bw_usuario, "[Hz]")
			#print("Margen de conexion (Usuarios: Pr-Sensibilidad>0): {}%".format(np.round(self.medida_conexion_margen*100,4)))
			#print("Porcentaje de usuaios cuya SINR supera {} dB, {} %".format(self.cfg_gen["ber_sinr"] ,np.round(self.medida_conexion_sinr*100,4)))
			#print("De {} usuarios, {} cumplen BER objetivo.".format(self.no_usuarios_total, self.conexion_total_sinr))
			#print("Distribucion Celular, original: ", self.planificador.mapa_conexion_celda)
			#print("Distribucion Celular, con desconexion: ", self.planificador.mapa_estacion_descon)
			#print("Probabilidad de desconexión: {}%".format(np.round(self.no_usuarios_total/np.sum(self.planificador.mapa_estacion_descon),4)))
			'''
			Las siguientes variables se repiten, averiguar por que!

			'''
			#print("Mapa de conexion por estacion inicial: ", self.mapa_conexion_estacion)
			#print("Mapa de conexion por estacion final: ", self.mapa_conexion_estacion_no_con)

			
			#print("El sistema en promedio ha alcanzado {} Mbps".format(np.round(self.throughput_sistema,4)))
			'''
			if self.planificador.mapa_conexion==self.planificador.mapa_estacion_descon:
				print("-->No hubo desconexión")
			else:
				print("-->[!!!] Desconexion de usuarios")
			#print(self.sinr_db)
			'''
			print("------------------------------------------[info_general]\n")
		else:
			print("\n-----[info_arreglos]:")

			print("\n[info_distancia]")
			#print(self.hiperc_distancias)

			print("\n[info_angulos]")
			#print(self.hiperc_angulos)

			print("\n[info_ganancia]")
			#print(self.hiperc_antena.hiper_ganancias)

			if self.cfg_prop["params_desv"]["display"]:
				print("\n[info_balance_simplificado_antes]")
				#print(self.hiperc_modelo_canal.balance_simplificado_antes)
				print("\n[info_balance_simplificado]")
				#print(self.hiperc_modelo_canal.balance_simplificado)
			else:
				pass

			print("\n[info_perdidas]")
			#print(self.hiperc_modelo_canal.resultado_path_loss)

			print("\n[info_potencia]")
			#print(self.hiperc_modelo_canal.resultado_balance)

			#print("\n[info_margen]")
			#print(self.hiperc_modelo_canal.resultado_margen) #DEPLETED
			print("-----[info_arreglos]:")

			#todos


	'''------------------------------------------------------------------------------------------
	---------------------------------------------------------------------------------------------
	------------------------------------FUNCIONES DE EXPERIMENTALES------------------------------
	---------------------------------------------------------------------------------------------
	---------------------------------------------------------------------------------------------'''
	#pass

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
