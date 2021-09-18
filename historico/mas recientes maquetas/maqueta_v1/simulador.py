#import
import os
import matplotlib.pyplot as plt
from matplotlib.patches import RegularPolygon
import sistema as ss
from utilidades import config as cfg
import matplotlib.pyplot as plt

import numpy as np
#add change01
from scipy.special import factorial
import scipy.stats as stats


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
		pre_sim.info_sinr(True)
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
		print("[simulador]: Ejecutando simulacion...")
		print(self.configuracion)
		pre_sim=ss.Sistema_Celular(self.configuracion)
		pre_sim.ver_todo()
		plt.show()
		print("[OK]-terminado")

	#adicionar03
	def configurar_montecarlo(self):
		'''Modulo de N iteraciones.'''
		print("[simulador]: Ejecutando montecarlo...")
		iteracion=self.configuracion["cfg_simulador"]["params_general"]["iteracion"]
		iteracion=30
		coleccion_simulacion=[]
		#poisson
		col_cobertura_usuarios=[] 
		#poisson celdas
		col_cobertura_usuarios_celda=[]
		#margen, si supera margen
		col_cob_conexion=[]
		#si supera sinr objetivouse_line_collection
		col_cob_conexion_sinr=[]
		#debe calcularse como 1-cob_conexion
		col_cob_desconexion=[]
		it=0
		print("[simulador]: Ejecutando Simulación")
		for n in range(iteracion):
			if iteracion>49:
				pass
			else:
				print("[simulador]:*******************************SIMULACION {}****************************".format(it))
			sim=ss.Sistema_Celular(self.configuracion)
			coleccion_simulacion.append(sim)
			if iteracion>49:
				pass
			else:
				#sim.info_general("general")
				print("[simulador]:*******************************FIN SIMULACION*****************************\n\n")
			sim=0
			it+=1

		print("[simulador]: Ejecutando Coleccion")
		for borrar, simulacion in enumerate(coleccion_simulacion):

			col_cobertura_usuarios.append(simulacion.no_usuarios_total)
			col_cobertura_usuarios_celda.append(simulacion.no_usuarios_celda)
			col_cob_conexion.append(simulacion.medida_conexion_margen)
			col_cob_conexion_sinr.append(simulacion.medida_conexion_sinr)
			print("[debug-simulador2] total-simulacion {} ,total_celda {}".format(simulacion.no_usuarios_total, simulacion.no_usuarios_celda))
			#libero memoria de los objetos recolectados.
			coleccion_simulacion[borrar]=0
		
		print("[simulador]: Generando Gráficas")
		#para todas colocar los ejes #numero de realizaciones/porcentajes de ..
		#grafica de distribucion de usuarios
		plt.figure()
		#que se vea mas continua dependiendo de #iteraciones
		plt.title("distribucion")
		plt.hist(col_cobertura_usuarios)

		#grafica porcentaje de conexion
		plt.figure()
		#no debe haber rango de escalon
		plt.title("usuarios conectados")
		#plt.hist(col_cob_conexion, density=False, cumulative=False)
		data,bins=np.histogram(col_cob_conexion)
		print(bins,data)
		plt.stem(bins[:-1],data, use_line_collection=True)

		#grafica conexion sinr
		plt.figure()
		plt.title("umbral sinr")
		plt.hist(col_cob_conexion_sinr,density=True, cumulative=False)

		plt.figure()
		plt.title("umbral sinr cumulativa")
		plt.hist(col_cob_conexion_sinr,density=True, cumulative=True)
		
		plt.show()
		
		
		#import seaborn as sns
		#kwargs = dict(hist_kws={'alpha':.6}, kde_kws={'linewidth':3})
		##sns.distplot(col_cobertura_usuarios, color="dodgerblue", label="Distribución de Usuarios", **kwargs)
		#plt.legend();
		#sns.countplot('depth', data=col_cobertura_usuarios)
		
		
		#grafica porcentaje de desconexion

		#plt.show()
		#print(col_cobertura_usuarios)

		#data,bins=np.histogram(col_cobertura_usuarios)
		#print(data)
		#print(bins)
		'''
		print("--")

		
		#implementar
		print(col_cob_conexion)
		print("--")
		data1,bins1=np.histogram(col_cob_conexion, 1)
		print(data1)
		print(bins1)



		plt.figure()
		import seaborn as sns
		kwargs = dict(hist_kws={'alpha':.6}, kde_kws={'linewidth':3})
		sns.displot(col_cob_conexion, color="dodgerblue", label="Distribución de Usuarios", **kwargs)
		plt.legend();
		plt.plot()
		
		
		#bins='auto'
		#plt.figure()
		#plt.title("usuarios conectados")
		########plt.stem(data,"bs-")
		#plt.stem(data)
		#plt.hist(col_cobertura_usuarios, bins=100)
		print("test")
		#y=np.bincount(col_cobertura_usuarios_celda)
		#data1,bins1=np.histogram(col_cobertura_usuarios_celda, bins=np.nonzero(y)[0])
		#suma1=np.sum(data1)

		#print(data1)
		#print(suma1)
		print("------------------------\nendtest")


		intensidad=self.configuracion["cfg_simulador"]["params_general"]["distribucion"][1]
		radio=self.configuracion["cfg_simulador"]["params_general"]["radio_cel"]
		num_celdas=self.configuracion["cfg_simulador"]["params_general"]["n_celdas"]
		area=np.pi*(radio**2)

		poisson_lamb=area*intensidad
		print("[debug simulador]",radio, area, poisson_lamb)

		#por celdas
		y=np.bincount(col_cobertura_usuarios_celda)
		#print(y)
		#print(np.nonzero(y))
		#print(np.nonzero(y)[0])

		plt.hist(col_cobertura_usuarios_celda, bins=np.nonzero(y)[0], density=True)


		t = np.arange(min(col_cobertura_usuarios_celda), max(col_cobertura_usuarios_celda), 0.7)
		d = np.exp(-poisson_lamb)*np.power(poisson_lamb, t)/factorial(t)
		print(t.shape,d.shape)
		plt.plot(t, d, 'rs')



		
		plt.figure()
		#por sistema
		y=np.bincount(col_cobertura_usuarios)
		plt.hist(col_cobertura_usuarios, bins=np.nonzero(y)[0], density=True)
		#suma=sum(col_cobertura_usuarios)
		#nuevo landa
		poisson_lamb=area*intensidad
		t = np.arange(min(col_cobertura_usuarios), max(col_cobertura_usuarios), 0.7)
		d = np.exp(-poisson_lamb)*np.power(poisson_lamb, t)/factorial(t)
		#d=d/np.exp(num_celdas)


		plt.plot(t, d, 'rs')

		#mu = poisson_lamb
		#variance = 1
		#sigma = np.sqrt(variance)
		#x = np.linspace(mu - 3*sigma, mu + 3*sigma, 100)
		#plt.plot(x, stats.norm.pdf(x, mu, sigma))
		
		
		plt.show()


		'''
		print("[OK] montecarlo")


if __name__=="__main__":
	#Prototipo:
	pass
else:
	print("Modulo Importado: [", os.path.basename(__file__), "]")
