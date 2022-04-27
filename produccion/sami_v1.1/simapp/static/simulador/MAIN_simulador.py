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
#logger
#import logging
#libreria estadisticas
#from scipy.special import factorial
#import scipy.stats as stats



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

		pre_sim.ver_todo()
		nombre="base-sim"
		densidad_choices=(
        (1, 'Baja'),
        (10, 'Media'),
        (100, 'Moderada'),
        (1000, 'Alta [!]'),
        (2000, 'Masivo [!!]'),
        (3000, 'Ultra [!!!]'))
		densidad_dict=dict(densidad_choices)
		titulo="Escenario: intensidad {}".format(densidad_dict[int(self.configuracion["cfg_simulador"]["params_general"]["distribucion"][1])])
		
		#ruta_img="simulador/base_datos/imagenes/presim/base-sim.png"
		#self.graficas_disponibles.append(ruta_img)
		ruta=ruta_img_presim+nombre+".png"
		self.graficas_disponibles_dic.update({titulo.upper():ruta})

		#display de antena
		nombre="patron_radiacion"
		pre_sim.hiperc_antena.ver_patron_local(nombre="patron_radiacion")
		titulo="Escenario: Patrón de Radiación"
		#ruta_img="simulador/base_datos/imagenes/presim/patron_radiacion.png"
		#self.graficas_disponibles.append(ruta_img)
		ruta=ruta_img_presim+nombre+".png"
		self.graficas_disponibles_dic.update({titulo.upper():ruta})
		 
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
			pre_sim.hiperc_modelo_canal.ver_relaciones_local(nombre="relaciones_debug")
			titulo="Relación de Gráficas (Debug)"
			#ruta_img="simulador/base_datos/imagenes/presim/relaciones.png"
			#self.graficas_disponibles.append(ruta_img)
			ruta=ruta_img_presim+nombre+"_debug.png"
			if self.debug_:
				self.graficas_disponibles_dic.update({titulo.upper():ruta})
			else:
				pass
			#
			nombre="balance"
			pre_sim.hiperc_modelo_canal.ver_balance_local(nombre="balance")
			titulo="Balance del Enlace con Desvanecimiento"
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
		'''
		pre_sim.ver_todo()
		nombre="base-sim"
		titulo="Escenario de Simulación"
		#ruta_img="simulador/base_datos/imagenes/presim/base-sim.png"
		#self.graficas_disponibles.append(ruta_img)
		ruta=ruta_img_presim+nombre+".png"
		self.graficas_disponibles_dic.update({titulo.upper():ruta})
		'''
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
		#la logitud de las rutas depende de donde se almacena los datos. Las imagenes se producen una capa mas alta por lo que la ruta es menor.
		#en cambio los datos se guardan desde aqui por que la ruta debe ser completa. Similar con mapa_calor_x,y. Hint: buscar mapa_calor_x.
		ruta_img_montecarlo="simulador/base_datos/imagenes/montecarlo"
		ruta_datos='simapp/static/simulador/base_datos/datos'
		
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
		col_cob_sinr=[]
		col_cob_sinr_mean=[]
		col_cap_modulacion=[]
		col_cap_tasa=[]
		#
		col_cob_conexion_sinr=[]
		#debe calcularse como 1-cob_conexion
		col_cob_desconexion=[]

		#
		#colecion de throughput
		col_cap_throughput_promedio=[]
		col_cap_throughput_total=[]
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
			#col_cobertura_usuarios.append(simulacion.no_usuarios_total)
			col_cobertura_usuarios.append(simulacion.no_usuarios_celda)
			col_cob_conexion.append(simulacion.medida_conexion_margen)

			col_cob_conexion_sinr.append(simulacion.medida_conexion_sinr)
			col_cob_sinr.append(simulacion.sinr_db)
			col_cob_sinr_mean.append(np.mean(simulacion.sinr_db))
			col_cap_modulacion.append(simulacion.modelo_modulacion.arr_modulacion)
			col_cap_tasa.append(simulacion.modelo_modulacion.arr_tasa)

			col_cap_throughput_promedio.append(simulacion.throughput_sistema)
			col_cap_throughput_total.append(simulacion.throughput_users)
			
			#libero memoria de los objetos recolectados.
			coleccion_simulacion[borrar]=0
		print("[simulador]: Terminado Coleccion...\n")

		print("[simulador]: Ejecuntando Almacenamiento...\n") #opcional
		raw_datos.guardar_data(ruta_datos,"col_cobertura_usuarios",col_cobertura_usuarios, "Coleccion de usuarios por celda original")
		raw_datos.guardar_data(ruta_datos,"col_cob_conexion",col_cob_conexion, "Coleccion de usuarios cuya potencia es mayor a la sensibilidad.")
		raw_datos.guardar_data(ruta_datos,"col_cob_conexion_sinr",col_cob_conexion_sinr,"""Coleccion de usuarios cuya SINR es mayor a un target espcificado en self.configuracion["cfg_simulador"]["params_general"]["ber_sinr"] """)
		raw_datos.guardar_data(ruta_datos,"col_cap_throughput_promedio",col_cap_throughput_promedio,"Coleccion de TP por simulacion. El valor por simulacion es el promedio de TP entre todas las celdas disponibles.")

		#........................................................................
		#............................. COBERTURA ...............................
		#........................................................................

		#grafica de distribucion de usuarios
		fig, ax = plt.subplots()
		ax.plot(np.linspace(1,len(col_cobertura_usuarios),len(col_cobertura_usuarios)), col_cobertura_usuarios, 'b-o')
		self.graficas_disponibles_dic=formatear_grafica_simple(ax, 'Fig 1. Usuarios, Proceso Puntual Poisson', 'Usuarios por Celda', 
			'Realizaciones', 'Número de Usuarios', 'pic_users_all', ruta_img_montecarlo, self.graficas_disponibles_dic)

		#grafica de distribucion de usuarios
		fig, ax = plt.subplots()
		ax.hist(col_cobertura_usuarios, bins=numero_barras)
		self.graficas_disponibles_dic=formatear_grafica_simple(ax, 'Fig 2. Histograma de Usuarios', 'Usuarios por Celda', 
			'Usuarios', 'Número de Ocurrencia', 'pic_users_hist', ruta_img_montecarlo, self.graficas_disponibles_dic)
		
					
		#grafica de distribucion de usuarios
		fig, ax = plt.subplots()
		#data,bins=np.histogram(col_cob_conexion,bins=numero_barras)
		ax.hist(col_cob_conexion, bins=numero_barras)
		#ax.stem(np.diff(bins),data, use_line_collection=True)
		if min(col_cob_conexion)==1:
			ax.set_xlim([0.8, 1.01])
		else:
			pass
		self.graficas_disponibles_dic=formatear_grafica_simple(ax, 'Fig 3. Histograma de Usuarios Conectados ', 'Usuarios: Pr-Sens>0', 
			'Porcentaje de Conexión', 'Número de Ocurrencia', 'pic_users_hist_on', ruta_img_montecarlo, self.graficas_disponibles_dic)

		#grafica de distribucion de usuarios
		#fig, ax = plt.subplots()
		#data,bins=np.histogram(col_cob_conexion,bins=numero_barras)
		#centros=estats.calcular_centros(bins)
		#ancho=bins[1]-bins[0]
		#ax.bar(centros, width=ancho, height=np.cumsum(data),ec='black')
		#self.graficas_disponibles_dic=formatear_grafica_simple(ax, 'Acumulativo de Usuarios Conectados', 'Usuarios: Pr-Sens>0', 
		#	'Porcentaje de Conexión', '', 'pic_users_cumsum_on', ruta_img_montecarlo, self.graficas_disponibles_dic)
		#CDF normalizada

		fig, ax = plt.subplots()
		#acomulativo densidad
		ax.hist(col_cob_conexion, bins=numero_barras, cumulative=True, density=True)
		if min(col_cob_conexion)==1:
			ax.set_xlim([0.8, 1.01])
		else:
			pass
		self.graficas_disponibles_dic=formatear_grafica_simple(ax, 'Fig 4. CDF Usuarios con Pr-Sens>0 dB', 'Usuarios: Pr-Sens>0', 
		'Pr-Sens>0 [dB]', '', 'pic_users_cumsum_density', ruta_img_montecarlo, self.graficas_disponibles_dic)
			
		#........................................................................
		#............................. SINR ...............................
		#........................................................................
		#sinr > target
		if min(col_cob_conexion)==1:
			ax.set_xlim([0.8, 1.01])
		else:
			pass
		ber_sinr=self.configuracion["cfg_simulador"]["params_general"]["ber_sinr"]
		#histograma
		fig, ax = plt.subplots()
		ax.hist(col_cob_conexion_sinr, bins=numero_barras)
		self.graficas_disponibles_dic=formatear_grafica_simple(ax, 'Fig 5. Histograma SINR > {} dB'.format(ber_sinr), "SINR mayor a {} dB".format(ber_sinr), 
			'Porcentaje de Usuarios con SINR>1 dB', 'Número de Ocurrencia', 'pic_sys_sinr_hist', ruta_img_montecarlo, self.graficas_disponibles_dic)
		
		#cdf, no normalizado
		fig, ax = plt.subplots()
		ax.hist(col_cob_conexion_sinr, bins=numero_barras, cumulative=True)
		self.graficas_disponibles_dic=formatear_grafica_simple(ax, 'Fig 6. CDF No normalizada SINR > {} dB'.format(ber_sinr), "SINR mayor a {} dB".format(ber_sinr), 
		'Porcentaje de Usuarios con SINR>1 dB', '', 'pic_sys_sinr_hist_acomulativo', ruta_img_montecarlo, self.graficas_disponibles_dic)
		
		#PDF, normalizada
		fig, ax = plt.subplots()
		y_prob,x_prob,ancho=estats.calcular_probabilidad(np.array(col_cob_conexion_sinr),numero_barras)
		ax.bar(x_prob, width=ancho, height=y_prob,ec='black')
		self.graficas_disponibles_dic=formatear_grafica_simple(ax, 'Fig 7. PDF SINR > {} dB'.format(ber_sinr), 'SINR mayor a {} dB'.format(ber_sinr), 
		'SINR>1 [dB]', 'Frecuencia de Ocurrencia', 'pic_sys_sinr_pdf', ruta_img_montecarlo, self.graficas_disponibles_dic)
		
		#CDF normalizada
		fig, ax = plt.subplots()
		#acomulativo densidad
		ax.hist(col_cob_conexion_sinr, bins=numero_barras, cumulative=True, density=True)
		self.graficas_disponibles_dic=formatear_grafica_simple(ax, 'Fig 8. CDF SINR > {} dB'.format(ber_sinr), 'SINR mayor a {} dB'.format(ber_sinr), 
		'SINR>1 [dB]', '', 'pic_sys_sinr_cumsum_density', ruta_img_montecarlo, self.graficas_disponibles_dic)

		#-------------------sinr total y promedio por simulacion
		#CDF no normalizada
		fig, ax = plt.subplots()
		#acomulativo densidad
		print(np.vstack(np.array(col_cob_sinr)).shape)
		ax.hist(np.vstack(np.array(col_cob_sinr)), bins=numero_barras)
		self.graficas_disponibles_dic=formatear_grafica_simple(ax, 'Fig 9. CDF SINR total', 'SINR', 
		'SINR', 'Ocurrencia', 'pic_sys_sinr_total', ruta_img_montecarlo, self.graficas_disponibles_dic)


		#CDF no normalizada
		fig, ax = plt.subplots()
		#acomulativo densidad
		#print(np.vstack(np.array(col_cob_sinr)).shape)
		ax.hist(col_cob_sinr_mean, bins=numero_barras)
		self.graficas_disponibles_dic=formatear_grafica_simple(ax, 'Fig 10. CDF SINR promedio', 'SINR', 
		'SINR', 'Ocurrencia', 'pic_sys_sinr_mean', ruta_img_montecarlo, self.graficas_disponibles_dic)

		#CDF normalizada
		fig, ax = plt.subplots()
		#acomulativo densidad
		#print(np.vstack(np.array(col_cob_sinr)).shape)
		ax.hist(np.vstack(np.array(col_cob_sinr)), bins=numero_barras, cumulative=True, density=True)
		self.graficas_disponibles_dic=formatear_grafica_simple(ax, 'Fig 11. CDF SINR total acomulativo', 'SINR', 
		'SINR', 'Ocurrencia', 'pic_sys_sinr_total_cumsum_density', ruta_img_montecarlo, self.graficas_disponibles_dic)

		#CDF normalizada
		fig, ax = plt.subplots()
		#acomulativo densidad
		#print(np.vstack(np.array(col_cob_sinr)).shape)
		ax.hist(col_cob_sinr_mean, bins=numero_barras, cumulative=True, density=True)
		self.graficas_disponibles_dic=formatear_grafica_simple(ax, 'Fig 12. CDF SINR promedio acomulativo', 'SINR', 
		'SINR', 'Ocurrencia', 'pic_sys_sinr_mean_cumsum_density', ruta_img_montecarlo, self.graficas_disponibles_dic)

		#........................................................................
		#............................. TASA Y MOD ...............................
		#........................................................................

		#CDF no normalizada
		fig, ax = plt.subplots()
		#acomulativo densidad
		proccessed_tasa=np.vstack(np.concatenate(np.array([np.array(xi) for xi in col_cap_tasa])))
		ax.hist(proccessed_tasa,bins=numero_barras)
		self.graficas_disponibles_dic=formatear_grafica_simple(ax, 'Fig 13. CDF TASA total', 'TASA', 
		'TASA', 'Ocurrencia', 'pic_sys_tasa_total', ruta_img_montecarlo, self.graficas_disponibles_dic)


		#CDF no normalizada
		fig, ax = plt.subplots()
		#acomulativo densidad
		#print(np.vstack(np.array(col_cap_modulacion)).shape)
		proccessed_tasa=np.vstack(np.concatenate(np.array([np.array(xi) for xi in col_cap_modulacion])))
		ax.hist(proccessed_tasa,bins=numero_barras)
		self.graficas_disponibles_dic=formatear_grafica_simple(ax, 'Fig 14. CDF MODULACION total', 'TASA', 
		'TASA', 'Ocurrencia', 'pic_sys_modulacion_total', ruta_img_montecarlo, self.graficas_disponibles_dic)
		

		#........................................................................
		#............................. THROUGHTPUT ...............................
		#........................................................................

		#histograma
		verificar_tp=sum(col_cap_throughput_promedio[0:20])
		if verificar_tp<1:
			print("THROUGHPUT ES MENOR A UNO, INDICANDO SCARCITY OF RESOURCES. SOLO SE MUESTRA TENDENCIA")
			#grafica de tp montecarlo
			fig, ax = plt.subplots()
			ax.plot(np.arange(1,len(col_cap_throughput_promedio)+1),np.cumsum(col_cap_throughput_promedio)/np.arange(1,len(col_cap_throughput_promedio)+1))
			self.graficas_disponibles_dic=formatear_grafica_simple(ax, 'Fig 15. Valor medio de Throughput', 'Throughput', 
				'Realizaciones', 'Throughput [Mbps]', 'pic_sys_tp_mc', ruta_img_montecarlo, self.graficas_disponibles_dic)
		else:
			#muestra todas las graficas.
			fig, ax = plt.subplots()
			ax.hist(col_cap_throughput_promedio,numero_barras)
			self.graficas_disponibles_dic=formatear_grafica_simple(ax, 'Fig 16. Histograma de Throughput Promedio', 'Histograma de Throughput Promedio', 
				'Throughput [Mbps]', 'Número de Ocurrencia', 'pic_sys_tp_hist', ruta_img_montecarlo, self.graficas_disponibles_dic)
			
			#grafica de tp comulativa
			#histograma acomulativo
			#fig, ax = plt.subplots()
			#ax.hist(col_cap_throughput_promedio, numero_barras, cumulative=True)
			#self.graficas_disponibles_dic=formatear_grafica_simple(ax, '2 Promedio de Throughput Acumulado', 'Throughput Acumulado', 
			#	'Throughput', 'Frecuencia de Ocurrencia', 'pic_sys_tp_cumsum', ruta_img_montecarlo, self.graficas_disponibles_dic)


			#grafica de tp comulativa
			#fig, ax = plt.subplots()
			#ax.hist(col_cap_throughput_promedio, numero_barras, density=True)
			#self.graficas_disponibles_dic=formatear_grafica_simple(ax, '3 Densidad de Throughput', 'Densidad Throughput', 
			#	'Throughput', 'Densidad', 'pic_sys_tp_density', ruta_img_montecarlo, self.graficas_disponibles_dic)
			
			
			#grafica de tp probabilidad
			fig, ax = plt.subplots()
			y_prob,x_prob,ancho=estats.calcular_probabilidad(np.array(col_cap_throughput_promedio),numero_barras)
			ax.bar(x_prob, width=ancho, height=y_prob,ec='black')
			self.graficas_disponibles_dic=formatear_grafica_simple(ax, 'Fig 17. PDF Throughput promedio', 'PDF de Throughput', 
				'Throughput [Mbps]', 'Frecuencia de Ocurrencia', 'pic_sys_tp_pdf', ruta_img_montecarlo, self.graficas_disponibles_dic)
			
			#grafica de tp probabilidad
			'''fig, ax = plt.subplots()
			x_prob=x_prob/max(x_prob)
			y_prob=np.cumsum(y_prob)
			ancho=x_prob[1]-x_prob[0]
			ax.bar(x_prob,y_prob, width=ancho,ec='black')
			ax.step(x_prob,y_prob,'r-o',where='mid')
			#ax.plot(x_prob, y_prob, drawstyle='steps-pre')
			self.graficas_disponibles_dic=formatear_grafica_simple(ax, '6 CDF Throughput', 'CDF Throughput', 
				'Throughput normalizado', '', 'pic_sys_tp_cdf', ruta_img_montecarlo, self.graficas_disponibles_dic)
			'''
			#grafica de tp comulativa
			fig, ax = plt.subplots()
			#acomulativo densidad
			ax.hist(col_cap_throughput_promedio, numero_barras, cumulative=True, density=True)
			self.graficas_disponibles_dic=formatear_grafica_simple(ax, 'Fig 18. CDF de Throughput promedio', 'CDF de Throughput', 
				'Throughput [Mbps]', '', 'pic_sys_tp_cumsum_density', ruta_img_montecarlo, self.graficas_disponibles_dic)

			#grafica de tp montecarlo
			fig, ax = plt.subplots()
			ax.plot(np.arange(1,len(col_cap_throughput_promedio)+1),np.cumsum(col_cap_throughput_promedio)/np.arange(1,len(col_cap_throughput_promedio)+1))
			self.graficas_disponibles_dic=formatear_grafica_simple(ax, 'Fig 19. Valor medio de Throughput promedio', ' Throughput', 
				'Realizaciones', ' Throughput [Mbps]', 'pic_sys_tp_mc', ruta_img_montecarlo, self.graficas_disponibles_dic)
			


			#grafica de tp comulativa
			fig, ax = plt.subplots()
			#acomulativo densidad
			processed_tp=np.vstack(np.array(np.concatenate(col_cap_throughput_total)))
			ax.hist(processed_tp, bins=numero_barras)
			self.graficas_disponibles_dic=formatear_grafica_simple(ax, 'Fig 20. Histograma de Throughput total', 'Throughput total', 
				'Throughput [Mbps]', '', 'pic_sys_tp_total_1_cumsum_density', ruta_img_montecarlo, self.graficas_disponibles_dic)

			#grafica de tp comulativa
			fig, ax = plt.subplots()
			#acomulativo densidad
			processed_tp=np.vstack(np.array(np.concatenate(col_cap_throughput_total)))
			ax.hist(processed_tp, bins=numero_barras, cumulative=True, density=True)
			self.graficas_disponibles_dic=formatear_grafica_simple(ax, 'Fig 20. CDF de Throughput total', 'CDF de Throughput', 
				'Throughput [Mbps]', '', 'pic_sys_tp_total_2_cumsum_density', ruta_img_montecarlo, self.graficas_disponibles_dic)


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
	ruta=ruta_img_montecarlo+'/'+nombre_archivo+".png"
	plt.savefig("simapp/static/"+ruta)
	diccionario.update({titulo_web.upper():ruta})
	return diccionario


if __name__=="__main__":
	#Prototipo:
	pass
else:
	print("Modulo Importado: [", os.path.basename(__file__), "]")
