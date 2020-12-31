#import
import matplotlib.pyplot as plt
from matplotlib.patches import RegularPolygon
import numpy as np
import os
#librerias internas
from . import sistema as ss
from .utilidades import config as cfg

class Simulador:
	def __init__(self, tipo):
		self.tipo=tipo
		
		self.graficas_disponibles_dic={}
		self.configuracion=cfg.cargar_variables(target_path="simapp/static/simulador/base_datos/")
		if self.tipo=="presimulacion":
			self.configurar_presimulacion()
		else:
			self.configurar_simulacion()


	def configurar_presimulacion(self):
		'''Modulo de pre-simulacion'''
		n_cel=self.configuracion["cfg_simulador"]["params_general"]["n_celdas"]
		resolucion=self.configuracion["cfg_simulador"]["params_general"]["imagen"]["resolucion"]
		radio_cel=self.configuracion["cfg_simulador"]["params_general"]["radio_cel"]
		#siempre es True por que es presimulacion.

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
			with open('simapp/static/simulador/base_datos/datos/test_x.npy', 'wb') as f:
				np.save(f, xx)
			with open('simapp/static/simulador/base_datos/datos/test_y.npy', 'wb') as f:
				np.save(f, yy)
			#adicion01-rm
			#print("Terminado [Ok]")


		#simulacion
		#APAGAR LA IMAGEN SIN ESTA ENCEIDA.
		pre_sim=ss.Sistema_Celular(self.configuracion)


		#display de imagen potencia
		if display_pic:
			pre_sim.ver_imagen_potencia(nombre="imagen_potencia")
			titulo="Muestra de Potencia Recibida"
			ruta_img="simulador/base_datos/imagenes/presim/imagen_potencia.png"
			#self.graficas_disponibles.append(ruta_img)
			self.graficas_disponibles_dic.update({titulo:ruta_img})
			#comentar en sami
			#plt.show()
		else:
			pass

		#display de antena
		pre_sim.hiperc_antena.ver_patron_local(nombre="patron_radiacion")
		titulo="Patrón de Radiación Trisectorizado"
		ruta_img="simulador/base_datos/imagenes/presim/patron_radiacion.png"
		#self.graficas_disponibles.append(ruta_img)
		self.graficas_disponibles_dic.update({titulo:ruta_img})
		 
		#display de perdidas por trayectoria
		pre_sim.hiperc_modelo_canal.ver_perdidas_local(nombre="perdidas")
		titulo="Muestra de Pérdidas de Propagación"
		ruta_img="simulador/base_datos/imagenes/presim/perdidas.png"
		#self.graficas_disponibles.append(ruta_img)
		self.graficas_disponibles_dic.update({titulo:ruta_img})
		 
		#display de desvanecimiento custom (si desvanecimiento)
		desva=self.configuracion["cfg_simulador"]["params_propagacion"]["params_desv"]["display"]
		if desva:
			pre_sim.hiperc_modelo_canal.ver_desvanecimiento_local(nombre="desvanecimiento")
			titulo="Muestra de Desvanecimiento"
			ruta_img="simulador/base_datos/imagenes/presim/desvanecimiento.png"
			#self.graficas_disponibles.append(ruta_img)
			self.graficas_disponibles_dic.update({titulo:ruta_img})
			#
			pre_sim.hiperc_modelo_canal.ver_relaciones_local(nombre="relaciones")
			titulo="Muestra de Relación de Gráficas"
			ruta_img="simulador/base_datos/imagenes/presim/relaciones.png"
			#self.graficas_disponibles.append(ruta_img)
			self.graficas_disponibles_dic.update({titulo:ruta_img})
			#
			pre_sim.hiperc_modelo_canal.ver_balance_local(nombre="balance")
			titulo="Muestra de Balance del Enlace"
			ruta_img="simulador/base_datos/imagenes/presim/balance.png"
			#self.graficas_disponibles.append(ruta_img)
			self.graficas_disponibles_dic.update({titulo:ruta_img})
		else:
			print("desvanecimiento desactivado, la grafica no se muestra")
			pre_sim.hiperc_modelo_canal.ver_balance_sin_local(nombre="balance_sin")
			titulo="Muestra de Balance del Enlace (Sin desvanecimiento)"
			ruta_img="simulador/base_datos/imagenes/presim/balance_sin.png"
			#self.graficas_disponibles.append(ruta_img)
			self.graficas_disponibles_dic.update({titulo:ruta_img})
		
		pre_sim.ver_todo()
		titulo="Muestra de Escenario de Simulación"
		ruta_img="simulador/base_datos/imagenes/presim/base-sim.png"
		#self.graficas_disponibles.append(ruta_img)
		self.graficas_disponibles_dic.update({titulo:ruta_img})
		
		#guardar los nombres de graficas disponibles para desplegar despues.
		#self.configuracion["cfg_gui"]["presim_graphs"]=self.graficas_disponibles
		self.configuracion["cfg_gui"]["presim_graphs"]=self.graficas_disponibles_dic
		#desactivar la imagen de potencia para prepara el archivo para monte-carlo.
		self.configuracion["cfg_simulador"]["params_general"]["imagen"]["display"][0]=False
		#guardar el archivo.
		cfg.guardar_cfg(self.configuracion, target_path="simapp/static/simulador/base_datos/")
		#print("django-diccionario: \n",self.graficas_disponibles_dic)

		
		#eliminar todo despues de pre-simular para desocupar la memoria.
		pre_sim=0
		x_prueba=0
		y_prueba=0
		xx,yy=0,0


	def configurar_simulacion(self):
		'''Modulo de simulacion.'''
		pass
		#off imagen de potencia.


if __name__=="__main__":
	#Prototipo:
	pass
else:
	print("Modulo Importado: [", os.path.basename(__file__), "]")
