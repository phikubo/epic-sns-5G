#import - inicio
import matplotlib.pyplot as plt
from matplotlib.patches import RegularPolygon
import numpy as np
import math
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
	print("...desde un archivo externo.Ignorar si la ejecucion es interna. ")
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
	def __init__(self, params_simulacion, params_transmision, params_perdidas):
		'''Constructor por defecto. Inicializa las variables de las clases'''
		#----------------------------------------------------------------------
		#--------------------------ENTRADA-------------------------------------
		#----------------------------------------------------------------------
		#params_simulacion=[n_cel,radio_cel, distribucion, frecuencia, bw]
		self.num_celdas=params_simulacion[0]
		#radio externo
		self.radio=params_simulacion[1]
		#
		#1.tupla con (intensidad, distribucion)
		#1.1 si la distribucion no tiene una intensidad, intensidad=0
		self.distribucion,self.intensidad=params_simulacion[2]

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
		self.bw_usuario=params_simulacion[0]
		self.potencia_ruido=(-174.2855251)+10*np.log10(self.bw_usuario*10**6)
		self.potencia_ruido_veces=(10**(self.potencia_ruido/10))
		#print(self.potencia_ruido, self.potencia_ruido_veces)


		self.cel_fig, self.cels_ax=plt.subplots(1)
		#cordenadas centrales de celdas
		print("[sistema.init.mc.coordenadas_nceldas]")
		self.origen_cel_x, self.origen_cel_y=mc.coordenadas_nceldas(self.num_celdas, self.radio)
		#----------------------------------------------------------------------
		#SALIDA
		#----------------------------------------------------------------------
		self.cluster=[]
		#inicio de variables de usuarios (de todas las celdas)
		self.ue_x=0
		self.ue_y=0
		#
		self.modelo_canal=0 #modelo de canal unico
		self.distancias_celdas=[] #distancias unica celda

		self.hiperc_modelo_canal=0 #modelo de canal de todos.
		self.hiperc_antena=0
		self.hiperc_distancias=[]
		self.hiperc_angulos=[]
		self.hiperc_ganancia_relativa=[]
		#falta las distancias totales?
		self.no_usuarios_total=0

		#todas las perdidas
		self.perdidas_celdas=[]
		#OUTPUTS
		 ###############***********************por usar
		#----------------------------------------------------------------------
		#---------------------------INICIALIZAR--------------------------------
		#----------------------------------------------------------------------
		#inicializa objetos tipo celda y las almacena en self.cluster
		self.inicializar_cluster_celdas()
		#crea las coordenadas de los usuarios segun una distribucion
		self.inicializar_distribucion() #falta implementar otras distribuciones: thomas cluster
		#self.ue_x, self.ue_y contiene los usuarios del cluster
		#Gestiona los usuarios en un hiper clustes, en coordendas, distancias y angulos.
		self.inicializar_hiperc_usuarios() #CONFIGURAR DIMENSION
		#re dimensiona los arreglos de: hiper distancia, hiper angulos, []
		#Almacena usuarios en cada celda del cluster
		#################################################self.inicializar_cluster_usuarios()
		#Crea la clase antena, outputs ganancia relativa.
		self.inicializar_antenas()
		#crea el modelo del mod_canal, frecuencia_central, distancias, ganancia relativa
		self.inicializar_modelo_canal() #depende de la frec y cluster_usuarios, cluster_ganancia

	'''-----------------------------------------------------------------------------------------
	--------------------------------------------------------------------------------------------
	------------------------------------FUNCIONES DE INICIALIZACION-----------------------------
	--------------------------------------------------------------------------------------------
	--------------------------------------------------------------------------------------------'''

	def configurar_dimension_arreglos(self, target):
		'''Funcion que re dimensiona un arreglo de la forma [ [ [celda 1][celda2][celda3] ] [ [celda 1][celda2][celda3] ]]
		a una organizacion de usuarios por celda.
		'''
		print("[sistema.configuracion_dimension_arreglos]")
		organizacion=[0 for i in range(self.num_celdas)]
		temporal=[]
		#itero sobre el numero de celdas
		#print("[sistema.configurar] \n", type(target))
		#print("[sistema.configurar] \n", target)
		for target_users in range(self.num_celdas):
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

	def inicializar_cluster_celdas(self):
		'''Init. Almacena las celdas unicas en un cluster de celdas para control y gestion.'''
		print("[sistema.inicializar_cluster_celdas]")
		#creo objetos tipo celda y les asigno su coordenada central
		for x,y in zip(self.origen_cel_x, self.origen_cel_y):
			#creo celdas con cada coordenada x,y y las asigno a sus propias coordendas
			self.obj=celda.Celda(x,y, self.radio) #aqui deberia generar las coordenadas de usuarios
			#agrupo las celdas creadas en una lista en las celdas para procesar despues
			self.cluster.append(self.obj)


	def inicializar_distribucion(self):
		'''Init. Crea coordenadas de usuario de acuerdo a una proceso de distribucion.'''
		print("[sistema.inicializar_distribucion]")
		if self.intensidad != 0:
			if self.distribucion=="ppp":
				self.ue_x, self.ue_y=ppp.distribuir_en_celdas(self.radio, self.origen_cel_x,
					self.origen_cel_y, self.intensidad)
				#shape es (n_celdas, n_usuarios en cada una)
				##print(np.shape(self.ue_x))#displays shape of arrays
				##print(np.shape(self.ue_y))
				#displays a number of objects-->IMPORTANTE
				##print("[sis.init.dist] 1. El cluster tiene ahora,", len(self.cluster), "celdas.")
				##print("[sis.init.dist] 2. Tipo de dato\n",type(self.ue_x)) #muestra la estructura de los datos.
				##print("[sis.init.dist] 3. Logitud dato celda[0]:\n",len(self.ue_x[0]))
				##print("[sis.init.dist] 4. Estructura de celdas\n",self.ue_x)

			elif self.distribucion=="random":
				pass
			elif self.distribucion=="prueba_unitaria":
				#print("prueba unitaria-parametros_", self.intensidad)
				self.ue_x,self.ue_y=self.intensidad
				#solucion, esto es una lista, debe ser numpy!
		else:
			pass


	def inicializar_cluster_usuarios(self):
		#depleted.
		'''Init. Almacena coordenadas de usuarios a su respectiva celda.
		Depleted reason: Ya no es necesario que cada celda guarde informacion de sus usuarios, pues
		guarda la informacion de todos los usuarios.'''
		#append distancias
		#self.distancias_celdas
		for celda_unica, su_x, su_y in zip(self.cluster, self.ue_x, self.ue_y):
			#print(celda_unica, su_x, su_y)
			celda_unica.user_x=su_x
			celda_unica.user_y=su_y
			#celda_unica.distancia_gnodeb_ue()
			self.distancias_celdas.append(celda_unica.distancias)
			#print("---inicializar_cluster",celda_unica.distancias)
		#self.distancias_celdas=np.array(self.distancias_celdas)
		#print(len(self.cluster),len(self.ue_x), "********usuarios")
		self.no_usuarios_total=len(self.cluster)*len(self.ue_x[0]) #todos las celdas=#usuarios
		#print("---aki2",self.distancias_celdas)
		#print("---tipo:",type(self.distancias_celdas


	def inicializar_hiperc_usuarios(self):
		'''Init. crea la clase usuario en cada coordenada.'''
		print("[sistema.inicializar_hiperc_usuarios]")
		self.no_usuarios_total=len(self.cluster)*len(self.ue_x[0])
		counter=0
		for celda_unica in self.cluster:
			celda_unica.interf_user_x=self.ue_x #todos los usuarios.
			celda_unica.interf_user_y=self.ue_y ##todos los usuarios.
			celda_unica.distancia_all_estacion_base_usuarios()#a cual celda hace esto?
			celda_unica.angulos_all_estacion_base_usuarios()
			#las dos variables siguientes, son las que originan los demas calculos.
			self.hiperc_distancias.append(celda_unica.interf_distancias)
			self.hiperc_angulos.append(celda_unica.interf_angulos)
			#rta, a cada celda, por es una instancia de clase.
			print('[sistema] end of: hiperc_usuarios. Celda->',counter)
			counter+=1

		#convierto a numpy:
		self.hiperc_distancias=np.stack(self.hiperc_distancias, axis=0)
		self.hiperc_angulos=np.stack(self.hiperc_angulos, axis=0)
		#reconfigurar.
		#print("[sistema.hiper.usuarios]\n",type(self.hiperc_distancias), type(self.hiperc_angulos))
		self.hiperc_distancias=self.configurar_dimension_arreglos(self.hiperc_distancias)
		self.hiperc_angulos=self.configurar_dimension_arreglos(self.hiperc_angulos)
		#print("[sistema.hiper.usuarios]:\n", test1,"\n", test2)
		#print(type(test1))
		#print(type(test1))
		#print("[sistema.debug]\n",self.hiperc_distancias)
		#self.hiperc_angulos=self.configurar_dimension_arreglos(self.hiperc_angulos)
		'''
		La funcion recibe todas las cordenadas de todos los usuarios en las celdas: [c1,c2,..,cn]
		con ci={xi,yi}, con xi,yi, i={1,2,...}
		'''


	def inicializar_antenas(self):
		'''Init. Crea un modelo de antena especificado. Calcula la ganancia relativa de
		un conjunto de angulos de usuario'''
		print("[sistema.inicializar_antenas]")
		#hpbw=55
		#amin=20
		#ref="4g"
		#gtx=15
		#indica la orientacion de los lobulos.
		apunt=mcir.calcular_angulo_v3(45,120) #inicio,angulo de particion.
		#se adjunta luego: apunt, tar
		#parametros=[ref, hpbw, gtx, amin, apunt, self.hiperc_angulos]
		self.params_antena.append(apunt)
		self.params_antena.append(self.hiperc_angulos)
		#print("ant", self.params_antena)
		self.hiperc_antena=ant.Antena(self.params_antena)
		self.hiperc_ganancia_relativa=self.hiperc_antena.hiper_ganancias #**considerar quitar

	def inicializar_modelo_canal(self):
		'''Init. Crea un modelo del canal aplicado a todo el sistema.
		 Calcula perdidas, dependiendo del tipo de modelo indicado.'''
		#diseno:
		#"tipo", pot_tx,loss_tx, gan_tx, gan_rx, loss_rx,sensibilidad
		#pasar parametros de perdidas:
		print("[sistema.inicializar_modelo_canal]")

		#self.modelo_canal=moca.Modelo_Canal(self.params_perdidas,params_sim, params_desv)

		#ya incluye unididades.
		params_sim=[self.frequencia_operacion, (self.hiperc_distancias, "m")] #distancia siempre en metros.
		params_desv=self.params_perdidas[0][2]
		#Creo un modelo del canal con todas las distancias.
		#
		#la ganacia de tx, ahora es la ganancia relativa de cada usuario.
		self.params_perdidas[3]=self.hiperc_ganancia_relativa
		#otro modelo de canal, pero con las hiper distancias.
		self.hiperc_modelo_canal=moca.Modelo_Canal(self.params_perdidas,params_sim, params_desv)
		#calculo las perdidas del modelo del canal segun el tipo de modelo de propagacion

		#IMPLEMENTACION DE PERDIDAS, NO DEBERIA ESTAR EN EL MODULO?. Cambiado.
		'''
		if self.params_perdidas[0]=="espacio_libre":
			self.modelo_canal.perdidas_espacio_libre_ghz()

		elif self.params_perdidas[0]=="okumura_hata":
			self.modelo_canal.perdidas_okumura_hata_mhz()
			#################
			self.hiperc_modelo_canal.perdidas_okumura_hata_mhz()
		'''
		#con los calculos anteriores, calculo el balance del enlace.
		#self.modelo_canal.balance_del_enlace_simple()
		#self.hiperc_modelo_canal.balance_del_enlace_simple()->implementado en modelo del canal





	'''-----------------------------------------------------------------------------------------
	--------------------------------------------------------------------------------------------
	------------------------------------FUNCIONES DE VISULAIZACION------------------------------
	--------------------------------------------------------------------------------------------
	--------------------------------------------------------------------------------------------'''

	def ver_estaciones_base(self):
		"""Permite ver las estaciones base de forma independiente"""
		plt.plot(self.origen_cel_x,self.origen_cel_y, 'b^')


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

		mcir.tri_sectorizar(angulo_x,angulo_y, radio_trisec, self.origen_cel_x,
		self.origen_cel_y, self.cels_ax)


	def ver_usuarios(self, *target):
		#*target ahora permite invocar la funcion con o sin parametros.
		"""Permite ver las estaciones base de forma independiente"""
		if target:
			plt.plot(self.ue_x[target],self.ue_y[target], 'go')
		else:
			plt.plot(self.ue_x,self.ue_y, 'go')


	def ver_usuarios_colores(self):
		#*target ahora permite invocar la funcion con o sin parametros.
		"""Permite ver los usuarios de diferente color, aleatorio"""
		for x,y in zip(self.ue_x, self.ue_y):
			plt.plot(x,y, c=np.random.rand(3,), ls='dotted')


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
			plt.plot(cx,cy, 'b')


	def ver_todo(self):
		"Funcion que retorna todaslas graficas."
		self.ver_usuarios()
		self.ver_celdas()
		self.ver_estaciones_base()
		self.ver_sectores()
		self.ver_circulos()
		self.ver_usuarios_colores()

	def info_celda_unica(self, target):
		'''Funcion para ver toda la información de una celda específica'''
		pass

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
		##print(self.ue_x[0])
		##print(self.ue_y[0])

		#point
		#punto=Point(self.ue_x[0][0], self.ue_y[0][0])
		#2,3, 4. Las tres se resumen en el siguiente procedimiento:
		puntos=[polygon_hex.contains(Point(a,b)) for a,b in zip(self.ue_x[0], self.ue_y[0])] #solo para celda de origen
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
	#print(sc.ue_x) #[ok], inicializar_distribucion
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
	print("Modulo Sistema importado")

	'''Definicion de la implementacion:
	COBERTURA:
	A. Usuario como entidad principal.

	0. Definir el número de usuarios en cada celda.
	1. Obtener posicion de usuarios del cluster: self.ue_x, self.ue_y [[cel1], [cel2],...,[celn]]
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
