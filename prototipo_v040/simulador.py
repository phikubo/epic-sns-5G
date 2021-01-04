#import
import os
import sistema as ss
from utilidades import config as cfg
import matplotlib.pyplot as plt
from matplotlib.patches import RegularPolygon
import numpy as np
import os

class Simulador:
	def __init__(self, tipo):
		self.tipo=tipo
		self.graficas_disponibles=[]
		#adicion03
		#self.configuracion=cfg.cargar_variables(target_path="base_datos/")
		if self.tipo=="presimulacion":
			self.configuracion=cfg.cargar_variables(target_path="base_datos/")
			self.configurar_presimulacion()
		elif self.tipo=="simulacion":
			self.configuracion=cfg.cargar_variables(target_path="base_datos/")
			self.configurar_simulacion()
		elif self.tipo=="montecarlo":
			self.configuracion=cfg.cargar_variables(target_path="base_datos/")
			self.configurar_montecarlo()
		else:
			print("Entrada no valida.")


	def configurar_presimulacion(self):
		'''Modulo de pre-simulacion'''
		n_cel=self.configuracion["cfg_simulador"]["params_general"]["n_celdas"]
		resolucion=self.configuracion["cfg_simulador"]["params_general"]["imagen"]["resolucion"]
		radio_cel=self.configuracion["cfg_simulador"]["params_general"]["radio_cel"]
		#siempre es True por que es presimulacion.
		self.configuracion["cfg_simulador"]["params_general"]["imagen"]["display"][0]=True
		#configuracion de imagen de potencia
		display_pic=True
		if display_pic:
			if n_cel>7:
				mul=4.6
			else:
				mul=3
			#adicion01-rm
			#print("--Generando data--")
			x_prueba=np.arange(-mul*radio_cel,mul*radio_cel,resolucion) #depende del radio_cel y numero de celdas.
			y_prueba=np.arange(-mul*radio_cel,mul*radio_cel,resolucion)
			xx,yy=np.meshgrid(x_prueba,y_prueba)
			#adicion01-rm
			#print("--Escribiendo--")
			with open('base_datos/datos/test_x.npy', 'wb') as f:
				np.save(f, xx)
			with open('base_datos/datos/test_y.npy', 'wb') as f:
				np.save(f, yy)
			#adicion01-rm
			#print("Terminado [Ok]")


		#simulacion
		pre_sim=ss.Sistema_Celular(self.configuracion)


		#display de imagen potencia
		if display_pic:
			pre_sim.ver_imagen_potencia(nombre="imagen_potencia")
			self.graficas_disponibles.append("imagen_potencia.png")
			#comentar en sami
			#plt.show()
		else:
			pass

		#display de antena
		pre_sim.hiperc_antena.ver_patron_local(nombre="patron_radiacion")
		self.graficas_disponibles.append("patron_radiacion.png")
		#plt.show()
		#display de perdidas por trayectoria
		#dist_modelo=np.array([0.1, 1, 2, 3, 4, 5, 6])
		#pre_sim.hiperc_modelo_canal.distancias=dist_modelo
		#print(pre_sim.hiperc_modelo_canal.distancias)
		pre_sim.hiperc_modelo_canal.ver_perdidas_local(nombre="perdidas")
		self.graficas_disponibles.append("perdidas.png")
		#pre_sim.hiperc_modelo_canal.inicializar_tipo()
		#display de desvanecimiento custom (si desvanecimiento)
		desva=self.configuracion["cfg_simulador"]["params_propagacion"]["params_desv"]["display"]
		if desva:
			pre_sim.hiperc_modelo_canal.ver_desvanecimiento_local(nombre="desvanecimiento")
			self.graficas_disponibles.append("desvanecimiento.png")
			pre_sim.hiperc_modelo_canal.ver_relaciones_local(nombre="relaciones")
			self.graficas_disponibles.append("relaciones.png")
			pre_sim.hiperc_modelo_canal.ver_balance_local(nombre="balance")
			self.graficas_disponibles.append("balance.png")
		else:
			print("[sistema]: desvanecimiento desactivado, la grafica no se genera")
			#adicionar02
			pre_sim.hiperc_modelo_canal.ver_balance_sin_local(nombre="balance_sin")
			self.graficas_disponibles.append("balance_sin.png")

		#guardar nombres de imagenes diponibles en presimulacion
		#print(self.graficas_disponibles)
		pre_sim.ver_todo()
		self.graficas_disponibles.append("base-sim.png")

		#guardar los nombres de graficas disponibles para desplegar despues.
		#self.configuracion["cfg_gui"]["presim_graphs"]=self.graficas_disponibles
		self.configuracion["cfg_gui"]["presim_graphs"]=self.graficas_disponibles
		#desactivar la imagen de potencia para prepara el archivo para monte-carlo.
		self.configuracion["cfg_simulador"]["params_general"]["imagen"]["display"][0]=False
		#guardar el archivo.
		cfg.guardar_cfg(self.configuracion, target_path="base_datos/")

		#guardar nombres de imagenes diponibles en presimulacion
		#self.configuracion

		#eliminar todo despues de pre-simular para desocupar la memoria.
		pre_sim=0
		x_prueba=0
		y_prueba=0
		xx,yy=0,0

	#adicionar03
	def configurar_simulacion(self):
		'''Modulo de simulacion.'''
		#simulacion
		print(self.configuracion)
		pre_sim=ss.Sistema_Celular(self.configuracion)
		pre_sim.ver_todo()
		plt.show()
		print("[ok]-terminado")

	#adicionar03
	def configurar_montecarlo(self):
		'''Modulo de N iteraciones.'''
		print("[simulador]: Ejecutando montecarlo...")
		iteracion=self.configuracion["cfg_simulador"]["params_general"]["iteracion"]
		coleccion_simulacion=[]
		col_cobertura_usuarios=[] #poisson
		#margen, si supera margen
		col_cob_conexion=[]
		#si supera sinr objetivo
		col_cob_conexion_sinr=[]
		#debe calcularse como 1-cob_conexion
		col_cob_desconexion=[]
		it=0
		for n in range(iteracion):
			print("[simulador]:*******************************SIMULACION {}****************************".format(it))
			sim=ss.Sistema_Celular(self.configuracion)
			coleccion_simulacion.append(sim)
			sim.info_general("general")
			sim=0
			it+=1



		for borrar, simulacion in enumerate(coleccion_simulacion):
			print("[simulador]: Ejecutando Coleccion")
			col_cobertura_usuarios.append(simulacion.no_usuarios_total)
			col_cob_conexion.append(simulacion.medida_conexion_margen)
			col_cob_conexion_sinr.append(simulacion.medida_conexion_sinr)

			#libero memoria de los objetos recolectados.
			coleccion_simulacion[borrar]=0

		print("[simulador]: Generando Gráficas")
		#grafica de distribucion de usuarios
		plt.figure()
		plt.title("distribucion")
		plt.hist(col_cobertura_usuarios)

		#grafica porcentaje de conexion
		plt.figure()
		plt.title("usuarios conectados")
		plt.hist(col_cob_conexion, density=True, cumulative=True)

		#grafica conexion sinr
		plt.figure()
		plt.title("umbral sinr")
		plt.hist(col_cob_conexion_sinr,density=True, cumulative=True)

		#grafica porcentaje de desconexion

		plt.show()
		print("[OK] montecarlo")


if __name__=="__main__":
	#Prototipo:
	pass
else:
	print("Modulo Importado: [", os.path.basename(__file__), "]")
