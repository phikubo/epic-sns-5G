#import - inicio
import matplotlib.pyplot as plt
from matplotlib.patches import RegularPolygon
import numpy as np
import math
#
#import - final
#
#bloque de carga de modulos - inicio
#
try:
	#from <paquete>          import <modulo>           as <nombre_preferencial_del modulo>
	from pk_red_dispositivos import celda
	from pk_red_dispositivos import modulo_coordenadas as mc
	from pk_red_dispositivos import modulo_ppp as ppp
	from pk_red_dispositivos import modulo_circulos as mcir

except:
	print("ATENCION: Uno o mas modulos no pudo ser importado... ")
	print("...desde un archivo externo. Ignorar si la ejecucion es interna. ")
#
#bloque de carga de modulos - final
#
#bloque de funciones - inicio
#
class Sistema_Celular:
	'''Clase que crea y controla clusters de celdas. Asigna e inicializa valores.
	Muestra graficas de las celdas deseadas.'''
	def __init__(self, num_celdas, radio, distribucion, Modelo_Canal):
		'''Constructor por defecto. Inicializa las variables de las clases'''
		#1.tupla con (intensidad, distribucion)
		#1.1 si la distribucion no tiene una intensidad, intensidad=0
		self.intensidad, self.distribucion=distribucion
		self.cel_fig, self.cels_ax=plt.subplots(1)
		self.num_celdas=num_celdas
		self.cluster=[]
		#radio externo
		self.radio=radio
		#cordenadas centrales de celdas
		self.origen_cel_x, self.origen_cel_y=mc.coordenadas_nceldas(self.num_celdas, self.radio)
		#inicio de variables de usuarios
		self.ue_x=0
		self.ue_y=0
		#inicializa objetos tipo celda y las almacena en self.cluster
		self.inicializar_cluster_celdas()
		#crea las coordenadas de los usuarios segun una distribucion
		self.inicializar_distribucion() #falta implementar otras distribuciones
		#Almacena usuarios en cada celda del cluster
		self.inicializar_cluster_usuarios()


	def inicializar_cluster_celdas(self):
		'''Init. Almacena las celdas unicas en un cluster de celdas para control y gestion.'''
		#creo objetos tipo celda y les asigno su coordenada central
		for x,y in zip(self.origen_cel_x, self.origen_cel_y):
			#creo celdas con cada coordenada x,y y las asigno a sus propias coordendas
			self.obj=celda.Celda(x,y, self.radio) #aqui deberia generar las coordenadas de usuarios
			#agrupo las celdas creadas en una lista en las celdas para procesar despues
			self.cluster.append(self.obj)


	def inicializar_distribucion(self):
		'''Init. Crea coordenadas de usuario de acuerdo a una distribucion.'''
		if self.intensidad != 0:
			if self.distribucion=="ppp":
				self.ue_x, self.ue_y=ppp.distribuir_en_celdas(self.radio, self.origen_cel_x, self.origen_cel_y, self.intensidad)
				#shape es (n_celdas, n_usuarios en cada una)
				##print(np.shape(self.ue_x))#displays shape of arrays
				##print(np.shape(self.ue_y))
				#displays a number of objects-->IMPORTANTE
				print("El cluster tiene ahora, ", len(self.cluster), "celdas.")

			elif self.distribucion=="random":
				pass
		else:
			pass


	def inicializar_cluster_usuarios(self):
		'''Init. Almacena coordenadas de usuarios a su respectiva celda.'''
		for celda_unica, su_x, su_y in zip(self.cluster, self.ue_x, self.ue_y):
			celda_unica.user_x=su_x
			celda_unica.user_y=su_y
			celda_unica.distancia_gnodeb_ue()


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

		mcir.tri_sectorizar(angulo_x,angulo_y, radio_trisec, self.origen_cel_x, self.origen_cel_y, self.cels_ax)


	def ver_usuarios(self):
		"""Permite ver las estaciones base de forma independiente"""
		plt.plot(self.ue_x,self.ue_y, 'go')


	def ver_todo(self):
		"Funcion que retorna todaslas graficas."
		self.ver_usuarios()
		self.ver_celdas()
		self.ver_estaciones_base()
		self.ver_sectores()

	def info_celda_unica(self, target):
		'''Funcion para ver toda la información de una celda específica'''
		pass
#bloque de funciones - final

def prueba_interna_v3_1():
	celdas=3
	radio=20
	intensidad=10
	distribucion=(intensidad/radio**2,"ppp") #0 en el primer valor si es otra distribucion (no necesario)
	mod_canal=None
	sc=Sistema_Celular(celdas,radio, distribucion, mod_canal)
	#print(sc.cluster[0].radio) #[ok], inicializar_cluster_celdas
	#print(sc.ue_x) #[ok], inicializar_distribucion
	#sc.ver_todo() #[ok],
	#plt.axis("equal")
	#plt.grid(True)
	#plt.show()
	print(sc.cluster[0].user_x) #[ok], inicializar_cluster_usuarios
	print(sc.cluster[0].distancias) #[ok] funcion interna, distancias
if __name__=="__main__":
	#Prototipo:
	prueba_interna_v3_1()
else:
	print("Modulo Sistema importado")
