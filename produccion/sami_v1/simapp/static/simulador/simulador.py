#librerias internas
try:
	print("From simulador.py")
	from . import sistema as ss
	from .utilidades import config as cfg
	from .pk_estadistica_desempeno import modulo_estadisticas as estats
except Exception as EX:
	print("ATENCION: Uno o mas modulos no pudo ser importado...\n", EX)


#librerias  computacion
from matplotlib.patches import RegularPolygon
import matplotlib.pyplot as plt
import numpy as np
import math
import os
import pyfiglet
#logger
import logging
#libreria estadisticas
#from scipy.special import factorial
#import scipy.stats as stats



class Simulador:
	def __init__(self, tipo):
		ascii_banner = pyfiglet.figlet_format("SAMI-5G")
		print(ascii_banner)
		#
		self.tipo=tipo
		self.graficas_disponibles_dic={}
		self.configuracion=cfg.cargar_variables(target_path="simapp/static/simulador/base_datos/")
		self.configuracion_gui=cfg.cargar_json(target_path="simapp/static/simulador/base_datos/config_gui")
		if self.tipo=="presimulacion":
			#una sola simulacion.
			print("[simulador]: Ejecutando presimulación...")
			self.configurar_presimulacion()
		elif self.tipo=="simulacion":
			#si iteracion ==1.
			print("[simulador]: Ejecutando simulación...")
			self.configuracion=cfg.cargar_variables(target_path="simapp/static/simulador/base_datos/")
			self.configurar_simulacion()
		elif self.tipo=="montecarlo":
			print("[simulador]: Ejecutando montecarlo...")
			self.configuracion=cfg.cargar_variables(target_path="simapp/static/simulador/base_datos/")
			print(self.configuracion["cfg_simulador"]["params_general"]["imagen"]["display"][0])
			self.configurar_montecarlo()
		else:
			print("Parametro Simulador no válido.")
		
		


	def configurar_presimulacion(self):
		'''Modulo de pre-simulacion'''
		#
		ruta_img_presim="simulador/base_datos/imagenes/presim/"
		#
		n_cel=self.configuracion["cfg_simulador"]["params_general"]["n_celdas"]
		resolucion=self.configuracion["cfg_simulador"]["params_general"]["imagen"]["resolucion"]
		radio_cel=self.configuracion["cfg_simulador"]["params_general"]["isd"]
		#radio de la celda fijo.
		radio_cel=(2/3)*radio_cel*math.sqrt(3)/2
		#reactivo la generacion de imagenes, asi se haya desactivado antes.
		self.configuracion["cfg_simulador"]["params_general"]["imagen"]["display"][0]=True
		#siempre es True por que es presimulacion.

		#configuracion de imagen de potencia
		display_pic=True
		if display_pic:
			if n_cel>7:
				#tamaño del canvas
				mul=4.6
			else:
				#tamaño del canvas
				mul=3
			#adicion01-rm
			#print("--Generando data:CANVAS--")
			x_prueba=np.arange(-mul*radio_cel,mul*radio_cel,resolucion) #depende del radio_cel y numero de celdas.
			y_prueba=np.arange(-mul*radio_cel,mul*radio_cel,resolucion)
			xx,yy=np.meshgrid(x_prueba,y_prueba)
			#adicion01-rm
			#print("--Escribiendo--")
			with open('simapp/static/simulador/base_datos/datos/test_x.npy', 'wb') as f:
				np.save(f, xx)
			with open('simapp/static/simulador/base_datos/datos/test_y.npy', 'wb') as f:
				np.save(f, yy)
			#adicion01-rm
			#print("Terminado [Ok]")


		#simulacion
		#APAGAR LA IMAGEN SIN ESTA ENCEIDA.
		pre_sim=ss.Sistema_Celular(self.configuracion)
		'''
		***OPTIMIZACION***
		En este punto ya se ha completado esta simulacion hasta el final'''

		#display de imagen potencia
		if display_pic:
			nombre="imagen_potencia"
			pre_sim.ver_imagen_potencia(nombre=nombre)
			titulo="Escenario: Potencia Recibida"
			#ruta_img="simulador/base_datos/imagenes/presim/imagen_potencia.png"
			#self.graficas_disponibles.append(ruta_img)
			ruta=ruta_img_presim+nombre+".png"
			self.graficas_disponibles_dic.update({titulo.upper():ruta})
			#comentar en sami
			#plt.show()
		else:
			pass

		#display de antena
		nombre="patron_radiacion"
		pre_sim.hiperc_antena.ver_patron_local(nombre="patron_radiacion")
		titulo="Escenario: Patrón de Radiación Trisectorizado"
		#ruta_img="simulador/base_datos/imagenes/presim/patron_radiacion.png"
		#self.graficas_disponibles.append(ruta_img)
		ruta=ruta_img_presim+nombre+".png"
		self.graficas_disponibles_dic.update({titulo.upper():ruta})
		 

		'''
		***OPTIMIZACION***
			se vuelve a calcular los valores del modelo del canal llamando
			las funciones custom destinadas a ese proposito.
			
			
			Aqui se puede guardar las estadisticas de 1 sola simulacion,
			antes del cambio de variables en presim.
			
			
			
			
			'''
		#sim=pre_sim

		#display de perdidas por trayectoria
			#ver_perdidas_local -> referencia a perdidas con muestra 20km.
		nombre="perdidas"
		pre_sim.hiperc_modelo_canal.ver_perdidas_local(nombre="perdidas")
		titulo="Pérdidas de Propagación"
		#ruta_img="simulador/base_datos/imagenes/presim/perdidas.png"
		#self.graficas_disponibles.append(ruta_img)
		ruta=ruta_img_presim+nombre+".png"
		self.graficas_disponibles_dic.update({titulo.upper():ruta})
		 
		#display de desvanecimiento custom (si desvanecimiento)
		desva=self.configuracion["cfg_simulador"]["params_propagacion"]["params_desv"]["display"]
		if desva:
			nombre="desvanecimiento"
			pre_sim.hiperc_modelo_canal.ver_desvanecimiento_local(nombre="desvanecimiento")
			titulo="Desvanecimiento"
			#ruta_img="simulador/base_datos/imagenes/presim/desvanecimiento.png"
			#self.graficas_disponibles.append(ruta_img)
			ruta=ruta_img_presim+nombre+".png"
			self.graficas_disponibles_dic.update({titulo.upper():ruta})
			#
			nombre="relaciones"
			pre_sim.hiperc_modelo_canal.ver_relaciones_local(nombre="relaciones")
			titulo="Relación de Gráficas"
			#ruta_img="simulador/base_datos/imagenes/presim/relaciones.png"
			#self.graficas_disponibles.append(ruta_img)
			ruta=ruta_img_presim+nombre+".png"
			self.graficas_disponibles_dic.update({titulo.upper():ruta})
			#
			nombre="balance"
			pre_sim.hiperc_modelo_canal.ver_balance_local(nombre="balance")
			titulo="Balance del Enlace"
			#ruta_img="simulador/base_datos/imagenes/presim/balance.png"
			#self.graficas_disponibles.append(ruta_img)
			ruta=ruta_img_presim+nombre+".png"
			self.graficas_disponibles_dic.update({titulo.upper():ruta})
		else:
			print("[simulador]: desvanecimiento desactivado, la grafica no se genera")
			nombre="balance_sin"
			pre_sim.hiperc_modelo_canal.ver_balance_sin_local(nombre="balance_sin")
			titulo="Balance del Enlace (Sin desvanecimiento)"
			#ruta_img="simulador/base_datos/imagenes/presim/balance_sin.png"
			#self.graficas_disponibles.append(ruta_img)
			ruta=ruta_img_presim+nombre+".png"
			self.graficas_disponibles_dic.update({titulo.upper():ruta})
		
		pre_sim.ver_todo()
		nombre="base-sim"
		titulo="Escenario de Simulación"
		#ruta_img="simulador/base_datos/imagenes/presim/base-sim.png"
		#self.graficas_disponibles.append(ruta_img)
		ruta=ruta_img_presim+nombre+".png"
		self.graficas_disponibles_dic.update({titulo.upper():ruta})
		print(self.graficas_disponibles_dic)
		#guardar los nombres de graficas disponibles para desplegar despues.
		#self.configuracion["cfg_gui"]["presim_graphs"]=self.graficas_disponibles
		
		#depleted to delete
		#self.configuracion["cfg_gui"]["presim_graphs"]=self.graficas_disponibles_dic

		#desactivar la imagen de potencia para prepara el archivo para monte-carlo.
		self.configuracion["cfg_simulador"]["params_general"]["imagen"]["display"][0]=False
		#guardar el archivo.
		cfg.guardar_cfg(self.configuracion, target_path="simapp/static/simulador/base_datos/")
		#print("django-diccionario: \n",self.graficas_disponibles_dic)
		
		#cambio de ruta en el path
		self.configuracion_gui["presim_graphs"]=self.graficas_disponibles_dic
		cfg.guardar_json(self.configuracion_gui, target_path="simapp/static/simulador/base_datos/config_gui")
		#eliminar todo despues de pre-simular para desocupar la memoria.
		pre_sim=0
		x_prueba=0
		y_prueba=0
		xx,yy=0,0
		#para reutilzar en simulacion y montecarlo, se limpia diccionario
		#self.graficas_disponibles_dic={}
		print("[simulador]: presimulacion terminado")
	

	def configurar_simulacion(self):
		'''Modulo de simulacion.'''
		#simulacion
		print("[simulador]: Ejecutando simulacion...")
		print(self.configuracion)
		pre_sim=ss.Sistema_Celular(self.configuracion)
		pre_sim.ver_todo()
		plt.show()
		print("[ok]-terminado")


	def configurar_montecarlo(self):
		'''Modulo de N iteraciones.'''
		print("[simulador]: Ejecutando montecarlo...")
		#
		ruta_img_montecarlo="simulador/base_datos/imagenes/montecarlo/"
		#
		iteracion=self.configuracion["cfg_simulador"]["params_general"]["iteracion"]
		coleccion_simulacion=[]
		#poisson
		col_cobertura_usuarios=[]
		#poisson celdas
		col_cobertura_usuarios_celda=[] 
		#margen, si supera margen
		col_cob_conexion=[]
		#si supera sinr objetivo
		col_cob_conexion_sinr=[]
		#debe calcularse como 1-cob_conexion
		col_cob_desconexion=[]

		#
		#colecion de throughput
		col_tp_mean=[]
		#contador de iteracion
		it=0
		print("[simulador]: Generando simulaciones...")
		for n in range(iteracion):
			#print("[simulador]:*******************************SIMULACION {}****************************".format(it))
			sim=ss.Sistema_Celular(self.configuracion)
			#se recolecta la informacion de cada simulacion en una lista de objetos tipo simulacion.
			coleccion_simulacion.append(sim)
			#se imprime la informacion de cada simulacion.
			##################################################################sim.info_general("general")
			#primeros datos (10)
			##################################################################sim.info_data(True)
			#libero memoria
			sim=0
			it+=1
		print("[simulador]:Terminado simulaciones...")
		print("[simulador]: Ejecutando Coleccion...")
		for borrar, simulacion in enumerate(coleccion_simulacion):
			
			#no es un numero valido de poisson.
			#col_cobertura_usuarios.append(simulacion.no_usuarios_total)
			col_cobertura_usuarios.append(simulacion.no_usuarios_celda)
			col_cob_conexion.append(simulacion.medida_conexion_margen)
			col_cob_conexion_sinr.append(simulacion.medida_conexion_sinr)
			col_tp_mean.append(simulacion.throughput_sistema)
			#libero memoria de los objetos recolectados.
			coleccion_simulacion[borrar]=0
		print("[simulador]: Terminado Coleccion...")

		##################################################################print("[simulador]: Generando Gráficas")
		##################################################################logging.info("[simulador]: Generando Gráficas")
		#grafica de distribucion de usuarios
		fig, ax = plt.subplots()
		ax.plot(np.linspace(1,len(col_cobertura_usuarios),len(col_cobertura_usuarios)), col_cobertura_usuarios, 'b-o')
		self.graficas_disponibles_dic=formatear_grafica_simple(ax, 'Usuarios, Proceso Puntual Poisson', 'Usuarios por Celda', 
			'Realizaciones', 'Número de Usuarios', 'pic_dist_users_all', ruta_img_montecarlo, self.graficas_disponibles_dic)

		#grafica de distribucion de usuarios
		fig, ax = plt.subplots()
		ax.hist(col_cobertura_usuarios, 20)
		self.graficas_disponibles_dic=formatear_grafica_simple(ax, 'Histograma de Usuarios', 'Usuarios por Celda', 
			'Usuarios', 'Ocurrencia', 'pic_dist_users_hist', ruta_img_montecarlo, self.graficas_disponibles_dic)
		

		#grafica de distribucion de usuarios
		fig, ax = plt.subplots()
		data,bins=np.histogram(col_cob_conexion)
		ax.stem(bins[:-1],data, use_line_collection=True)
		self.graficas_disponibles_dic=formatear_grafica_simple(ax, 'Histograma de Usuarios Conectados', 'Usuarios: Pr-Sens>0', 
			'Porcentaje de Conexión (Normalizado)', 'Ocurrencia', 'pic_on_users_hist', ruta_img_montecarlo, self.graficas_disponibles_dic)
		
		
		#grafica conexion sinr
		#sinr > target
		ber_sinr=self.configuracion["cfg_simulador"]["params_general"]["ber_sinr"]
		fig, ax = plt.subplots()
		ax.hist(col_cob_conexion_sinr, cumulative=True)
		self.graficas_disponibles_dic=formatear_grafica_simple(ax, 'Histograma SINR > x dBs', "SINR mayor a {} dBs".format(ber_sinr), 
			'Porcentaje Acomulativo', 'Ocurrencia', 'pic_sys_sinr_hist', ruta_img_montecarlo, self.graficas_disponibles_dic)




		#grafica de tp
		fig, ax = plt.subplots()
		ax.hist(col_tp_mean)
		self.graficas_disponibles_dic=formatear_grafica_simple(ax, 'Promedio de Throughput', 'Histograma Throughput', 
			'Throughput', 'Ocurrencia', 'pic_sys_tp_hist', ruta_img_montecarlo, self.graficas_disponibles_dic)
		
		#grafica de tp comulativa
		fig, ax = plt.subplots()
		ax.hist(col_tp_mean, 20, cumulative=True)
		self.graficas_disponibles_dic=formatear_grafica_simple(ax, 'Promedio de Throughput Acumulado', 'Throughput Acumulado', 
			'Throughput', 'Ocurrencia', 'pic_sys_tp_cumsum', ruta_img_montecarlo, self.graficas_disponibles_dic)
		
		#grafica de tp montecarlo
		fig, ax = plt.subplots()
		ax.plot(np.arange(1,len(col_tp_mean)+1),np.cumsum(col_tp_mean)/np.arange(1,len(col_tp_mean)+1))
		self.graficas_disponibles_dic=formatear_grafica_simple(ax, 'Throughput Montecarlo', 'Simulación Throughput', 
			'Realizaciones', 'Tendencia Throughput', 'pic_mc_tp_sistema', ruta_img_montecarlo, self.graficas_disponibles_dic)
		
		#grafica de tp probabilidad
		fig, ax = plt.subplots()
		y_prob,x_prob,ancho=estats.calcular_probabilidad(np.array(col_tp_mean))
		ax.bar(x_prob, width=ancho, height=y_prob,ec='black')
		self.graficas_disponibles_dic=formatear_grafica_simple(ax, 'Probabilidad Throughtput', 'PDF', 
			'Throughput', 'Probabilidad', 'pic_pdf_tp_sistema', ruta_img_montecarlo, self.graficas_disponibles_dic)
		
		#grafica de tp probabilidad
		fig, ax = plt.subplots()
		#por corregir
		#y_prob,x_prob,ancho=estats.calcular_probabilidad(np.array(col_tp_mean))
		#ax.bar(height=np.sort(np.cumsum(y_prob)))
		#self.graficas_disponibles_dic=formatear_grafica_simple(ax, 'Probabilidad Acomulativa Throughtput', 'CDF', 
		#	'Throughput', 'Probabilidad', 'pic_cdf_tp_sistema', ruta_img_montecarlo, self.graficas_disponibles_dic)
		


		#GUARDAR DATOS
		self.configuracion_gui["montecarlo_graphs"]=self.graficas_disponibles_dic
		cfg.guardar_json(self.configuracion_gui, target_path="simapp/static/simulador/base_datos/config_gui")

		#plt.show()
		print("[OK]:montecarlo terminado, continuando con la operaion...")


def formatear_grafica_simple(ax, titulo_web, titulo_graf, xlab,ylab, nombre_archivo, ruta_img_montecarlo, diccionario):
	ax.set_title(titulo_graf)
	ax.set_xlabel(xlab)
	ax.set_ylabel(ylab)
	plt.grid(True)
	ruta=ruta_img_montecarlo+nombre_archivo+".png"
	plt.savefig("simapp/static/"+ruta)
	diccionario.update({titulo_web.upper():ruta})
	return diccionario


if __name__=="__main__":
	#Prototipo:
	pass
else:
	print("Modulo Importado: [", os.path.basename(__file__), "]")
