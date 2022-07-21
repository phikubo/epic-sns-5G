#librerias internas
try:
	print("From simulador.py")
	from . import sistema as ss
	from .utilidades import config as cfg
	from .utilidades import modulo_almacenamiento as raw_datos
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
import seaborn as sns
class Simulador:
	def __init__(self, tipo):
		#
		self.debug_=True
		self.tipo=tipo
		self.graficas_disponibles_dic={}
		self.conf_sim=cfg.cargar_json(target_path="simapp/static/simulador/base_datos/config_sim")
		#self.configuracion=cfg.cargar_cfg(target_path="simapp/static/simulador/base_datos")
		self.configuracion=cfg.cargar_json_full(target_path=self.conf_sim["ruta_activa"])

		self.configuracion_gui=cfg.cargar_json(target_path="simapp/static/simulador/base_datos/config_gui")
		'''NOTA PARA EL DESARROLADOR:
		En presimulacion se carga la variable self.configuracion. En simulacion y montecarlo se recarga. Esto debido a que en presimulacion
		se genera la imagen de potencia y para evitar que esta sobre cargue el sistema en montecarlo, el archivo de configuracion se modifica
		desactivando la imagen, y se almacena nuevamente el archivo.'''
		if self.tipo=="presimulacion":
			#una sola simulacion.
			print("[simulador]: Ejecutando presimulación...")
			self.configurar_presimulacion()
		elif self.tipo=="simulacion":
			#si iteracion ==1.
			print("[simulador]: Ejecutando simulación...")
			self.configuracion=cfg.cargar_json_full(target_path=self.conf_sim["ruta_activa"])
			self.configurar_simulacion()
		elif self.tipo=="montecarlo":
			print("[simulador]: Ejecutando montecarlo...")
			self.configuracion=cfg.cargar_json_full(target_path=self.conf_sim["ruta_activa"])
			self.configurar_montecarlo()
		else:
			print("Parametro Simulador no válido.")
		
		


	def configurar_presimulacion(self):
		'''Modulo de pre-simulacion'''
		#
		ascii_banner = pyfiglet.figlet_format("PRESIM")
		print(ascii_banner)
		ruta_img_presim="simulador/base_datos/imagenes/presim/"
		#configuracion de ruta principal
		cfg_sim=cfg.cargar_json(target_path="simapp/static/simulador/base_datos/config_sim")
		self.ruta_activa=cfg_sim["ruta_activa"].split("/")[-1].split(".")[0]
		ruta_relativa=os.getcwd().replace("\\", "/")
		ruta_directorio="{}/simapp/static/simulador/base_datos/imagenes/resultados/{}/".format(ruta_relativa,self.ruta_activa)
		if os.path.exists(ruta_directorio):
			pass
		else:
			os.mkdir(ruta_directorio)

		#configuracion de subruta
		ruta_directorio="{}/simapp/static/simulador/base_datos/imagenes/resultados/{}/presim".format(ruta_relativa,self.ruta_activa)
		if os.path.exists(ruta_directorio):
			pass
		else:
			os.mkdir(ruta_directorio)

		ruta_img_presim="simulador/base_datos/imagenes/resultados/{}/presim/".format(self.ruta_activa)
		#print("Ruta presim", ruta_img_presim)

		#
		n_cel=self.configuracion["cfg_simulador"]["params_general"]["n_celdas"]
		resolucion=self.configuracion["cfg_simulador"]["params_general"]["imagen"]["resolucion"]
		radio_cel=self.configuracion["cfg_simulador"]["params_general"]["isd"]
		#radio de la celda fijo.
		#radio_cel=(2/3)*radio_cel*math.sqrt(3)/2
		#reactivo la generacion de imagenes, asi se haya desactivado antes.
		self.configuracion["cfg_simulador"]["params_general"]["imagen"]["display"][0]=True
		#siempre es True por que es presimulacion.

		#configuracion de imagen de potencia
		display_pic=True
		if display_pic:
			if n_cel<=1:
				mul=1
			elif n_cel>1 and n_cel<=7:
				mul=2
			elif n_cel>7 and n_cel <=19:
				#tamaño del canvas
				mul=3
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
			with open('simapp/static/simulador/base_datos/datos/mapa_calor_x.npy', 'wb') as archivo_npy:
				np.save(archivo_npy, xx)
			with open('simapp/static/simulador/base_datos/datos/mapa_calor_y.npy', 'wb') as archivo_npy:
				np.save(archivo_npy, yy)
			#adicion01-rm
			#print("Terminado [Ok]")


		#simulacion
		#APAGAR LA IMAGEN SIN ESTA ENCEIDA.
		print("!!!!!!!!!!!!pre simulacion instancia iniciada")
		pre_sim=ss.Sistema_Celular(self.configuracion.copy())
		print("!!!!!!!!!!!!pre simulacion instancia terminada")
		'''
		***OPTIMIZACION***
		En este punto ya se ha completado esta simulacion hasta el final'''

		#display de imagen potencia
		if display_pic:
			nombre="Fig1_imagen_potencia"
			#[!]guardar imagen
			pre_sim.ver_imagen_potencia(nombre=nombre, ruta_global=ruta_img_presim)
			titulo="Imágen de Potencia Recibida, Resolución: {}".format(resolucion) #resolucion
			#ruta_img="simulador/base_datos/imagenes/presim/imagen_potencia.png"
			#self.graficas_disponibles.append(ruta_img)
			ruta=ruta_img_presim+nombre+".png"
			self.graficas_disponibles_dic.update({titulo.upper():ruta})
			#comentar en sami
			#plt.show()
		else:
			pass
		#[!]guardar imagen
		nombre="Fig2_base-sim"
		pre_sim.ver_todo(nombre=nombre, ruta_global=ruta_img_presim)
		densidad_choices=(
        (1, 'Baja'),
        (10, 'Media'),
        (100, 'Moderada'),
        (1000, 'Alta [!]'),
        (2000, 'Masivo [!!]'),
        (3000, 'Ultra [!!!]'))
		densidad_dict=dict(densidad_choices)
		titulo="Densidad de MS: {}".format(densidad_dict[int(self.configuracion["cfg_simulador"]["params_general"]["distribucion"][1])])

		#ruta_img="simulador/base_datos/imagenes/presim/base-sim.png"
		#self.graficas_disponibles.append(ruta_img)
		ruta=ruta_img_presim+nombre+".png"
		self.graficas_disponibles_dic.update({titulo.upper():ruta})

		titulo="Asignación de servicio MS, en función de la SINR"
		nombre="Fig2_base-sim_on_off"
		pre_sim.ver_usuarios_conectados(nombre=nombre, ruta_global=ruta_img_presim)
		ruta=ruta_img_presim+nombre+".png"
		self.graficas_disponibles_dic.update({titulo.upper():ruta})


		#display de antena
		nombre="Fig3_patron_radiacion"
		pre_sim.hiperc_antena.ver_patron_presim(nombre=nombre, ruta_global=ruta_img_presim)
		titulo="Patrón de Radiación"
		#ruta_img="simulador/base_datos/imagenes/presim/patron_radiacion.png"
		#self.graficas_disponibles.append(ruta_img)
		ruta=ruta_img_presim+nombre+".png"
		self.graficas_disponibles_dic.update({titulo.upper():ruta})
		 
		#sim=pre_sim

		#display de perdidas por trayectoria
			#ver_perdidas_presim -> referencia a perdidas con muestra 20km.
		nombre="Fig4_perdidas"
		pre_sim.hiperc_modelo_canal.ver_perdidas_presim(nombre=nombre, ruta_global=ruta_img_presim)
		titulo="Pérdidas de Propagación"
		#ruta_img="simulador/base_datos/imagenes/presim/perdidas.png"
		#self.graficas_disponibles.append(ruta_img)
		ruta=ruta_img_presim+nombre+".png"
		self.graficas_disponibles_dic.update({titulo.upper():ruta})
		 
		#display de desvanecimiento custom (si desvanecimiento)
		desva=self.configuracion["cfg_simulador"]["params_propagacion"]["params_desv"]["display"]
		if desva:
			#
			nombre="Fig5_balance"
			pre_sim.hiperc_modelo_canal.ver_balance_presim(nombre=nombre, ruta_global=ruta_img_presim)
			titulo="Balance del Enlace con Desvanecimiento"
			#ruta_img="simulador/base_datos/imagenes/presim/balance.png"
			#self.graficas_disponibles.append(ruta_img)
			ruta=ruta_img_presim+nombre+".png"
			self.graficas_disponibles_dic.update({titulo.upper():ruta})


			nombre="Fig6_desvanecimiento"
			#solo funciona en presim, por eso esta mas relacionada en la instancia en lugar de la clase sistema.
			pre_sim.hiperc_modelo_canal.ver_desvanecimiento_presim(nombre=nombre, ruta_global=ruta_img_presim)
			titulo="Desvanecimiento"
			#ruta_img="simulador/base_datos/imagenes/presim/desvanecimiento.png"
			#self.graficas_disponibles.append(ruta_img)
			ruta=ruta_img_presim+nombre+".png"
			self.graficas_disponibles_dic.update({titulo.upper():ruta})
			#
			nombre="relaciones"
			pre_sim.hiperc_modelo_canal.ver_relaciones_presim(nombre="relaciones_debug", ruta_global=ruta_img_presim)
			titulo="Relación de Gráficas (Debug)"
			#ruta_img="simulador/base_datos/imagenes/presim/relaciones.png"
			#self.graficas_disponibles.append(ruta_img)
			ruta=ruta_img_presim+nombre+"_debug.png"
			if self.debug_:
				self.graficas_disponibles_dic.update({titulo.upper():ruta})
			else:
				pass
			
		else:
			print("[simulador]: desvanecimiento desactivado, la grafica no se genera")
			nombre="Fig5_balance_sin"
			pre_sim.hiperc_modelo_canal.ver_balance_sin_presim(nombre=nombre, ruta_global=ruta_img_presim)
			titulo="Balance del Enlace (Sin desvanecimiento)"
			#ruta_img="simulador/base_datos/imagenes/presim/balance_sin.png"
			#self.graficas_disponibles.append(ruta_img)
			ruta=ruta_img_presim+nombre+".png"
			self.graficas_disponibles_dic.update({titulo.upper():ruta})

		#guardar los nombres de graficas disponibles para desplegar despues.
		#self.configuracion["cfg_gui"]["presim_graphs"]=self.graficas_disponibles
		
		#desactivar la imagen de potencia para prepara el archivo para monte-carlo.
		self.configuracion["cfg_simulador"]["params_general"]["imagen"]["display"][0]=False
		#guardar el archivo.
		cfg.guardar_json_full(self.configuracion, target_path=self.conf_sim["ruta_activa"])
		
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
		ascii_banner = pyfiglet.figlet_format("Montecarlo")
		print(ascii_banner)
		#
		numero_barras=self.configuracion["cfg_gui"]["histograma_cfg"]["numero_barras"]
		#
		cfg_sim=cfg.cargar_json(target_path="simapp/static/simulador/base_datos/config_sim")

		self.ruta_activa=cfg_sim["ruta_activa"].split("/")[-1].split(".")[0]
		#self.ruta_activa=self.ruta_activa.split(".")[-1]
		ruta_relativa=os.getcwd().replace("\\", "/")
		ruta_directorio="{}/simapp/static/simulador/base_datos/imagenes/resultados/{}/montecarlo/".format(ruta_relativa,self.ruta_activa)
		if os.path.exists(ruta_directorio):
			pass
		else:
			os.mkdir(ruta_directorio)
		#ruta_completa=ruta_relativa+"simapp/static/simulador/base_datos/imagenes/montecarlo"

		#la logitud de las rutas depende de donde se almacena los datos. Las imagenes se producen una capa mas alta por lo que la ruta es menor.
		#en cambio los datos se guardan desde aqui por que la ruta debe ser completa. Similar con mapa_calor_x,y. Hint: buscar mapa_calor_x.
		#ruta_img_montecarlo="simulador/base_datos/imagenes/montecarlo"
		ruta_img_montecarlo="simulador/base_datos/imagenes/resultados/{}/montecarlo/".format(self.ruta_activa)
		#os.mkdir(ruta_img_montecarlo)

		ruta_datos='simapp/static/simulador/base_datos/datos'
		
		#
		iteracion=self.configuracion["cfg_simulador"]["params_general"]["iteracion"]
		coleccion_simulacion=[]
		#poisson
		col_cobertura_MS=[]

		#poisson celdas
		col_cobertura_MS_celda=[] 

		#margen, si supera margen
		col_cob_conexion=[]

		#si supera sinr objetivo
		col_cob_sinr_total=[]

		#modulacion
		col_cap_modulacion_total=[]
		#tasa
		col_cap_tasa_total=[]
		#
		col_cob_conexion_sinr=[]

		#MS con SINR > 1. No porcentaje, numero de MS.
		col_cob_probabilidad_servicio=[]

		#
		#colecion de throughput
		col_cap_throughput_promedio=[]
		col_cap_throughput_total=[]

		#MS con SINR > 1. No porcentaje, numero de MS.
		col_cap_throughput_servicio=[]

		#contador de iteracion
		it=0
		print("[simulador]: Generando simulaciones...")
		for n in range(iteracion):
			#print("[simulador]:*******************************SIMULACION {}****************************".format(it))
			sim=ss.Sistema_Celular(self.configuracion)
			#se recolecta la informacion de cada simulacion en una lista de objetos tipo simulacion.
			coleccion_simulacion.append(sim)
			#se imprime la informacion de cada simulacion.
			##################################################################
			'''
			sim.info_general("general")
			sim.info_data(True)
			'''
			#libero memoria
			sim=0
			it+=1
		print("[simulador]:Terminado simulaciones...\n")
		print("[simulador]: Ejecutando Coleccion...")
		for borrar, simulacion in enumerate(coleccion_simulacion):
			
			#no es un numero valido de poisson.
			#col_cobertura_MS.append(simulacion.no_usuarios_total)
			col_cobertura_MS.append(simulacion.no_usuarios_celda)
			col_cob_conexion.append(simulacion.medida_conexion_margen)

			col_cob_conexion_sinr.append(simulacion.medida_conexion_sinr)
			col_cob_sinr_total.append(simulacion.sinr_db)
			#depleted_col_cob2_sinr_mean.append(np.mean(simulacion.sinr_db))
			col_cap_modulacion_total.append(simulacion.modelo_modulacion.arr_modulacion)
			col_cap_tasa_total.append(simulacion.modelo_modulacion.arr_tasa)

			col_cap_throughput_promedio.append(simulacion.throughput_sistema)
			col_cap_throughput_total.append(simulacion.throughput_users)
			
			#nuevas Figuras
			col_cob_probabilidad_servicio.append(simulacion.mapa_conexion_desconexion)
			col_cap_throughput_servicio.append(simulacion.mapa_throughput_minimo)
			#libero memoria de los objetos recolectados.
			coleccion_simulacion[borrar]=0
		print("[simulador]: Terminado Coleccion...\n")

		print("[simulador]: Ejecuntando Almacenamiento...\n") #opcional
		raw_datos.guardar_data(ruta_datos,"col_cobertura_MS",col_cobertura_MS, "Coleccion de usuarios por celda original")
		raw_datos.guardar_data(ruta_datos,"col_cob_conexion",col_cob_conexion, "Coleccion de usuarios cuya potencia es mayor a la sensibilidad.")
		raw_datos.guardar_data(ruta_datos,"col_cob_conexion_sinr",col_cob_conexion_sinr,"""Porcentaje de usuarios cuya SINR es mayor a un target espcificado en self.configuracion["cfg_simulador"]["params_general"]["ber_sinr"] """)
		#raw_datos.guardar_data(ruta_datos,"col_cap_throughput_promedio",col_cap_throughput_promedio,"Coleccion de TP por simulacion. El valor por simulacion es el promedio de TP entre todas las celdas disponibles.")
		
		#raw_datos.guardar_data(ruta_datos,"col_cob_probabilidad_servicio",col_cob_probabilidad_servicio, "Probababilidad de SINR>1")
		#raw_datos.guardar_data(ruta_datos,"col_cap_throughput_servicio",col_cap_throughput_servicio, "Probabilidad de TP > 100 mbps {}".format(col_cap_throughput_servicio[0].shape))
		#........................................................................
		#............................. COBERTURA ...............................
		#........................................................................

		#grafica de distribucion de usuarios
		fig, ax = plt.subplots()
		ax.plot(np.linspace(1,len(col_cobertura_MS),len(col_cobertura_MS)), col_cobertura_MS, 'b-o')
		#formatear_grafica_simple(ax, titulo_web, titulo_graf, xlab,ylab, nombre_archivo, ruta_img_montecarlo, diccionario, ruta_activa)
		self.graficas_disponibles_dic=formatear_grafica_simple(ax, 'Fig01. Histograma de MS', 'MS por Celda', 
			'Realizacion', 'Número de MS', 'Fig01', ruta_img_montecarlo, self.graficas_disponibles_dic, self.ruta_activa)

		#grafica de distribucion de usuarios
		#fig, ax = plt.subplots()
		
		#ax.hist(col_cobertura_MS, bins=numero_barras)
		#m,d,v,md=estats.media_desviacion_varianza(col_cobertura_MS)
		#formatear_grafica_simple(ax, titulo_web, titulo_graf, xlab,ylab, nombre_archivo, ruta_img_montecarlo, diccionario, ruta_activa)
		#self.graficas_disponibles_dic=formatear_grafica_simple(ax, 'Fig02. Histograma de MS', 'MS por Celda. \nMediana: {}, Media: {}, Desviación: {}, Varianza: {}'.format(round(md,2),round(m,2),round(d,2),round(v,2)), 
			#'MS', 'Número de Ocurrencias', 'Fig02', ruta_img_montecarlo, self.graficas_disponibles_dic, self.ruta_activa)
		#m=0;d=0;v=0;
		
					
		fig, ax = plt.subplots()
		#ax=sns.kdeplot(col_cobertura_MS, shade=True, kde=True)
		#ax.hist(col_cobertura_MS, bins=numero_barras)
		ax=sns.histplot(col_cobertura_MS,kde=True, bins=numero_barras)
		m,d,v,md=estats.media_desviacion_varianza(col_cobertura_MS)
		#formatear_grafica_simple(ax, titulo_web, titulo_graf, xlab,ylab, nombre_archivo, ruta_img_montecarlo, diccionario, ruta_activa)
		self.graficas_disponibles_dic=formatear_grafica_simple(ax, 'Fig02. Histograma de MS', 'MS por Celda. \nMediana: {}, Media: {}, Desviación: {}'.format(round(md,2),round(m,2),round(d,2)), 
			'MS', 'Número de Ocurrencias', 'Fig02', ruta_img_montecarlo, self.graficas_disponibles_dic, self.ruta_activa)
		#m=0;d=0;v=0;

		fig, ax = plt.subplots()
		data=np.vstack(col_cobertura_MS)
		m,d,v,md=estats.media_desviacion_varianza(data)
		#data_normal=estats.normalizar_arreglo_a_b(data)
		#ax.hist(data_normal, bins=numero_barras)
		ax.boxplot(data, vert=False, notch=True)
		ax.violinplot(data, vert=False)
		ax.set_yticklabels([''])
		#formatear_grafica_simple(ax, titulo_web, titulo_graf, xlab,ylab, nombre_archivo, ruta_img_montecarlo, diccionario, ruta_activa)
		self.graficas_disponibles_dic=formatear_grafica_simple(ax, 'Fig02.1. Resumen de Distribución de MS', 'Resumen de Distribución de MS.\nMediana: {}, Media: {}, Desviación: {}'.format(round(md,2),round(m,2),round(d,2)), 
		'MS', '', 'Fig02.1', ruta_img_montecarlo, self.graficas_disponibles_dic, self.ruta_activa)


		fig, ax = plt.subplots()
		#ax=sns.kdeplot(col_cobertura_MS, shade=True, kde=True)
		#ax.hist(col_cobertura_MS, bins=numero_barras)
		a,b,c=ax.hist(col_cobertura_MS, cumulative=True, density=True, bins=numero_barras,alpha=0.1)
		ax=sns.histplot(col_cobertura_MS,kde=True, cumulative=True, stat="density",bins=numero_barras)
		#m,d,v,md=estats.media_desviacion_varianza(col_cobertura_MS)
		#formatear_grafica_simple(ax, titulo_web, titulo_graf, xlab,ylab, nombre_archivo, ruta_img_montecarlo, diccionario, ruta_activa)
		self.graficas_disponibles_dic=formatear_grafica_simple(ax, 'Fig02.2. CDF MS por Celda', 'CDF MS.\nMínimo: {}, Máximo: {}.'.format(round(np.min(b),2), round(np.max(b),2)), 
			'MS', 'Probabilidad Acumulada', 'Fig02.2', ruta_img_montecarlo, self.graficas_disponibles_dic, self.ruta_activa)
		#m=0;d=0;v=0;				
		
		fig, ax = plt.subplots()
		#acomulativo densidad
		#data,bins=np.histogram(col_cob_conexion,bins=numero_barras)
		unique, counts = np.unique(col_cob_conexion, return_counts=True)
		m,d,v,md=estats.media_desviacion_varianza(col_cob_conexion)
		ax.stem(unique,counts)
		self.graficas_disponibles_dic=formatear_grafica_simple(ax, 'Fig03. Histograma de MS con Pr-Sens>0 dB', 'Pulso: MS con Pr-Sens>0.\nMediana: {}, Media: {}, Desviación: {}'.format(round(md,2),round(m,2),round(d,2)), 
		'Pr-Sens > 0 [dB]', 'Número de Ocurrencias', 'Fig03', ruta_img_montecarlo, self.graficas_disponibles_dic, self.ruta_activa)

		#grafica de distribucion de usuarios
		fig, ax = plt.subplots()
		#data,bins=np.histogram(col_cob_conexion,bins=numero_barras)
		a,b,c=ax.hist(col_cob_conexion, cumulative=True, density=True, bins=numero_barras,alpha=0.1)
		ax=sns.histplot(col_cob_conexion, kde=True, cumulative=True, stat="density",bins=numero_barras)
		self.graficas_disponibles_dic=formatear_grafica_simple(ax, 'Fig04. CDF de MS Conectados', 'CDF MS con Pr-Sens>0.\nMínimo: {}, Máximo: {}.'.format(round(np.min(b),2), round(np.max(b),2)), 
			'Probabilidad de Conexión', 'Probabilidad Acumulativa', 'Fig04', ruta_img_montecarlo, self.graficas_disponibles_dic, self.ruta_activa)
		#self.graficas_disponibles_dic=formatear_grafica_simple(ax, 'Fig03. Histograma de MS Conectados', 'Escalon: MS: Pr-Sens>0', 
		#	'Porcentaje de Conexión', 'Número de Ocurrencias', 'Fig03', ruta_img_montecarlo, self.graficas_disponibles_dic, self.ruta_activa)

		#........................................................................
		#............................. SINR ...............................
		#........................................................................
		
		#-------------------sinr total y promedio por simulacion
		#CDF no normalizada
		fig, ax = plt.subplots()
		#acomulativo densidad
		processed_data=np.vstack(np.array(col_cob_sinr_total))
		a,b,c=ax.hist(processed_data, bins=numero_barras,alpha=0.1)
		ax=sns.histplot(processed_data,kde=True, bins=numero_barras, legend=False)
		#ax.set_xscale('log')
		 #\nMedia: {}, Desviación: {} y Varianza: {}.'.format(round(m,2),round(d,2),round(v,2))
		#formatear_grafica_simple(ax, titulo_web, titulo_graf, xlab,ylab, nombre_archivo, ruta_img_montecarlo, diccionario, ruta_activa)
		self.graficas_disponibles_dic=formatear_grafica_simple(ax, 'Fig05. Histograma SINR', 'Histograma SINR. \nMínimo: {} dB, Máximo: {} dB.'.format(round(np.min(b),2), round(np.max(b),2)), 
		'SINR [dB]', 'Número de Ocurrencias', 'Fig05', ruta_img_montecarlo, self.graficas_disponibles_dic, self.ruta_activa)

		fig, ax = plt.subplots()
		data=np.vstack(np.array(col_cob_sinr_total))
		m,d,v,md=estats.media_desviacion_varianza(data)
		#data_normal=estats.normalizar_arreglo_a_b(data)
		#ax.hist(data_normal, bins=numero_barras)
		ax.boxplot(data, vert=False, notch=True)
		ax.violinplot(data, vert=False)
		ax.set_yticklabels([''])
		#formatear_grafica_simple(ax, titulo_web, titulo_graf, xlab,ylab, nombre_archivo, ruta_img_montecarlo, diccionario, ruta_activa)
		self.graficas_disponibles_dic=formatear_grafica_simple(ax, 'Fig06. Resumen de Distribución de SINR', 'Resumen de Distribución de SINR.\nMediana: {} dB, Media: {} dB, Desviación: {} dB'.format(round(md,2),round(m,2),round(d,2)), 
		'SINR [dB]', '', 'Fig06', ruta_img_montecarlo, self.graficas_disponibles_dic, self.ruta_activa)


		#CDF normalizada
		fig, ax = plt.subplots()
		#acomulativo densidad
		data=np.vstack(np.vstack(np.array(col_cob_sinr_total)))
		#data_normal=estats.normalizar_arreglo_a_b(data)
		a,b,c=ax.hist(data, cumulative=True, density=True, bins=numero_barras,alpha=0.1)
		ax=sns.histplot(data,kde=True, cumulative=True, stat="density",bins=numero_barras, legend=False)
		self.graficas_disponibles_dic=formatear_grafica_simple(ax, 'Fig07. CDF SINR', 'CDF SINR.\nMínimo: {} dB, Máximo: {} dB.'.format(round(np.min(b),2), round(np.max(b),2)), 
		'SINR [dB]', 'Probabilidad Acumulada', 'Fig07', ruta_img_montecarlo, self.graficas_disponibles_dic, self.ruta_activa)

		fig, ax = plt.subplots()
		#acomulativo densidad
		processed_data=np.vstack(np.array(col_cob_probabilidad_servicio))
		ax.plot(np.arange(1,len(processed_data)+1),np.cumsum(processed_data)/np.arange(1,len(processed_data)+1))
		self.graficas_disponibles_dic=formatear_grafica_simple(ax, 'Fig07_2. Tendencia de MS con SINR > SINR_min', 'Tendencia de probabilidad de servicio (SINR).', 
		'Número de MS Total', 'Probabilidad de Servicio (SINR)', 'Fig07_2', ruta_img_montecarlo, self.graficas_disponibles_dic, self.ruta_activa)

		#........................................................................
		#............................. TASA Y MOD ...............................
		#........................................................................

		#CDF no normalizada
		#fig, ax = plt.subplots()
		#acomulativo densidad
		proccessed_tasa=np.vstack(np.concatenate(np.array([np.array(xi) for xi in col_cap_tasa_total])))
		#m,d,v,md=estats.media_desviacion_varianza(proccessed_tasa)
		#data, bins, patch=ax.hist(proccessed_tasa)
		#self.graficas_disponibles_dic=formatear_grafica_simple(ax, 'Fig08. Histograma Tasa de Codificación', 'Tasa de Codificación. \nMediana: {}, Media: {}, Desviación: {}, Varianza: {}'.format(round(md,2),round(m,2),round(d,2),round(v,2)), 
		#'Tasa Codificación', 'Número de Ocurrencias', 'Fig08', ruta_img_montecarlo, self.graficas_disponibles_dic, self.ruta_activa)

		fig, ax = plt.subplots()
		unique, counts = np.unique(proccessed_tasa, return_counts=True)
		ax.stem(unique,counts)
		m,d,v,md=estats.media_desviacion_varianza(proccessed_tasa)
		#formatear_grafica_simple(ax, titulo_web, titulo_graf, xlab,ylab, nombre_archivo, ruta_img_montecarlo, diccionario, ruta_activa)
		self.graficas_disponibles_dic=formatear_grafica_simple(ax, 'Fig08_2. Histograma Tasa de Codificación', 'Tasa de Codificación. \nMediana: {}, Media: {}, Desviación: {}'.format(round(md,2),round(m,2),round(d,2)),
		'Tasa Codificación', 'Número de Ocurrencias', 'Fig08_2', ruta_img_montecarlo, self.graficas_disponibles_dic, self.ruta_activa)

		#CDF no normalizada
		#fig, ax = plt.subplots()
		#acomulativo densidad
		#print(np.vstack(np.array(col_cap_modulacion_total)).shape)
		proccessed_tasa=np.vstack(np.concatenate(np.array([np.array(xi) for xi in col_cap_modulacion_total])))
		#m,d,v,md=estats.media_desviacion_varianza(proccessed_tasa)
		#ax.hist(proccessed_tasa)
		#self.graficas_disponiblepys_dic=formatear_grafica_simple(ax, 'Fig09. Histograma Índice de Modulación', 'Índice de Modulación. \nMediana: {}, Media: {}, Desviación: {}, Varianza: {}'.format(round(md,2),round(m,2),round(d,2),round(v,2)), 
		#'Índice de Modulación', 'Número de Ocurrencias', 'Fig09', ruta_img_montecarlo, self.graficas_disponibles_dic, self.ruta_activa)
		
		fig, ax = plt.subplots()
		unique, counts = np.unique(proccessed_tasa, return_counts=True)
		m,d,v,md=estats.media_desviacion_varianza(proccessed_tasa)
		ax.stem(unique,counts)
		ax.legend(['2 = QPSK \n4 = 16-QAM\n6 = 64-QAM\n8 = 256-QAM'])
		#formatear_grafica_simple(ax, titulo_web,                            titulo_graf,
		#xlab,         ylab,    nombre_archivo, ruta_img_montecarlo,      diccionario,              ruta_activa)
		self.graficas_disponibles_dic=formatear_grafica_simple(ax, 'Fig09_2. Histograma Índice de Modulación', 'Índice de Modulación.\nMediana: {}, Media: {}, Desviación: {}, Varianza: {}'.format(round(md,2),round(m,2),round(d,2),round(v,2)), 
		'Índice de Modulación', 'Número de Ocurrencias', 'Fig09_2', ruta_img_montecarlo, self.graficas_disponibles_dic, self.ruta_activa)

		#........................................................................
		#............................. THROUGHTPUT ...............................
		#........................................................................
		
		#histograma
		verificar_tp=sum(col_cap_throughput_promedio[0:20])
		if verificar_tp<1:
			print("THROUGHPUT ES MENOR A UNO, INDICANDO SCARCITY OF RESOURCES. SOLO SE MUESTRA TENDENCIA")
			#grafica de tp montecarlo
			fig, ax = plt.subplots()
			processed_tp=np.vstack(np.array(np.concatenate(col_cap_throughput_total)))
			ax.plot(np.arange(1,len(processed_tp)+1),np.cumsum(processed_tp)/np.arange(1,len(processed_tp)+1))
			self.graficas_disponibles_dic=formatear_grafica_simple(ax, 'Fig10_3. Histograma de Throughput', 'Throughput', 
				'Throughput [Mbps]', 'Número de Ocurrencias', 'Fig10_3', ruta_img_montecarlo, self.graficas_disponibles_dic, self.ruta_activa)
		else:
			
			#grafica de tp comulativa
			fig, ax = plt.subplots()
			#acomulativo densidad
			processed_tp=np.vstack(np.array(np.concatenate(col_cap_throughput_total)))
			a,b,c=ax.hist(processed_tp, bins=numero_barras,alpha=0.1)
			ax=sns.histplot(processed_tp,kde=True,bins=numero_barras,legend=False)
			##############################formatear_grafica_simple(ax, titulo_web,                            titulo_graf,
			#xlab,         ylab,    nombre_archivo, ruta_img_montecarlo,      diccionario,              ruta_activa)
			self.graficas_disponibles_dic=formatear_grafica_simple(ax, 'Fig10. Histograma de Throughput', 'Throughput.\nMínimo: {} Mbps, Máximo: {} Mbps.'.format(round(np.min(b),2), round(np.max(b),2)), 
			'Throughput [Mbps]', 'Número de Ocurrencias', 'Fig10', ruta_img_montecarlo, self.graficas_disponibles_dic, self.ruta_activa)

			#grafica de tp comulativa
			fig, ax = plt.subplots()
			#acomulativo densidad
			processed_tp=np.vstack(np.array(np.concatenate(col_cap_throughput_total)))
			m,d,v,md=estats.media_desviacion_varianza(processed_tp)
			#data_normal=estats.normalizar_arreglo_a_b(processed_tp)
			#ax.hist(data_normal, bins=numero_barras)
			ax.boxplot(processed_tp, vert=False, notch=True)
			ax.violinplot(processed_tp, vert=False)
			ax.set_yticklabels([''])
			self.graficas_disponibles_dic=formatear_grafica_simple(ax, 'Fig10_2. Resumen de distribución de Throughput', 'Resumen de distribución de Throughput.\nMediana: {} Mbps, Media: {} Mbps, Desviación: {} Mbps.'.format(round(md,2),round(m,2),round(d,2)), 
			'Throughput [Mbps]', '', 'Fig10_2', ruta_img_montecarlo, self.graficas_disponibles_dic, self.ruta_activa)



			#grafica de tp comulativa
			fig, ax = plt.subplots()
			#acomulativo densidad
			processed_tp=np.vstack(np.array(np.concatenate(col_cap_throughput_total)))
			#data_normal=estats.normalizar_arreglo_a_b(processed_tp)
			a,b,c=ax.hist(processed_tp, cumulative=True, density=True, bins=numero_barras,alpha=0.1)
			ax=sns.histplot(processed_tp,kde=True, cumulative=True, stat="density",bins=numero_barras,legend=False)
			self.graficas_disponibles_dic=formatear_grafica_simple(ax, 'Fig11. CDF de Throughput', 'CDF de Throughput.\nMínimo: {} Mbps, Máximo: {} Mbps.'.format(round(np.min(b),2), round(np.max(b),2)), 
			'Throughput [Mbps]', 'Probabilidad Acumulada', 'Fig11', ruta_img_montecarlo, self.graficas_disponibles_dic, self.ruta_activa)
			


			#grafica de tp montecarlo
			fig, ax = plt.subplots()
			processed_tp=np.vstack(np.array(np.concatenate(col_cap_throughput_total)))
			ax.plot(np.arange(1,len(processed_tp)+1),np.cumsum(processed_tp)/np.arange(1,len(processed_tp)+1))
			self.graficas_disponibles_dic=formatear_grafica_simple(ax, 'Fig12. Tendencia de Throughput Promedio', 'Tendencia de Throughput Promedio', 
				'Número de MS Total', ' Throughput [Mbps]', 'Fig12', ruta_img_montecarlo, self.graficas_disponibles_dic, self.ruta_activa)

			fig, ax = plt.subplots()
			processed_data=np.vstack(np.array(col_cap_throughput_servicio))
			ax.plot(np.arange(1,len(processed_data)+1),np.cumsum(processed_data)/np.arange(1,len(processed_data)+1))
			self.graficas_disponibles_dic=formatear_grafica_simple(ax, 'Fig12_2. Tendencia de Throughput > Throughput_min (100 Mbps)', 'Tendencia de Probabilidad de Servicio', 
			'Número de MS Total', 'Probabilidad de servicio (Throughput)', 'Fig12_2', ruta_img_montecarlo, self.graficas_disponibles_dic, self.ruta_activa)

		#GUARDAR DATOS
		self.configuracion_gui["montecarlo_graphs"]=self.graficas_disponibles_dic
		cfg.guardar_json(self.configuracion_gui, target_path="simapp/static/simulador/base_datos/config_gui")

		#plt.show()
		print("[OK]:montecarlo terminado, continuando con la operaion...")


def formatear_grafica_simple(ax, titulo_web, titulo_graf, xlab,ylab, nombre_archivo, ruta_img_montecarlo, diccionario, ruta_activa):
	ax.set_title(titulo_graf)
	ax.set_xlabel(xlab)
	ax.set_ylabel(ylab)
	plt.grid(True)
	ruta=ruta_img_montecarlo+nombre_archivo+".png"
	print("_---formato ruta---_", ruta)
	plt.savefig("simapp/static/"+ruta)
	diccionario.update({titulo_web.upper():ruta})
	return diccionario


if __name__=="__main__":
	#Prototipo:
	pass
else:
	print("Modulo Importado: [", os.path.basename(__file__), "]")
