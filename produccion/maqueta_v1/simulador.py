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
		self.configuracion=cfg.cargar_variables(target_path="base_datos/")
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
			print("--Generando data--")
			x_prueba=np.arange(-mul*radio_cel,mul*radio_cel,resolucion) #depende del radio_cel y numero de celdas.
			y_prueba=np.arange(-mul*radio_cel,mul*radio_cel,resolucion)
			xx,yy=np.meshgrid(x_prueba,y_prueba)
			print("--Escribiendo--")
			with open('base_datos/datos/test_x.npy', 'wb') as f:
				np.save(f, xx)
			with open('base_datos/datos/test_y.npy', 'wb') as f:
				np.save(f, yy)
			print("Terminado [Ok]")


		#simulacion
		pre_sim=ss.Sistema_Celular(self.configuracion)


		#display de imagen potencia
		if display_pic:
			pre_sim.ver_imagen_potencia(nombre="imagen_potencia")
			#comentar en sami
			#plt.show()
		else:
			pass

		#display de antena
		pre_sim.hiperc_antena.ver_patron_local(nombre="patron_radiacion")
		#plt.show()
		#display de perdidas por trayectoria
		#dist_modelo=np.array([0.1, 1, 2, 3, 4, 5, 6])
		#pre_sim.hiperc_modelo_canal.distancias=dist_modelo
		#print(pre_sim.hiperc_modelo_canal.distancias)
		pre_sim.hiperc_modelo_canal.ver_perdidas_local(nombre="perdidas")
		#pre_sim.hiperc_modelo_canal.inicializar_tipo()
		#display de desvanecimiento custom (si desvanecimiento)
		desva=self.configuracion["cfg_simulador"]["params_propagacion"]["params_desv"]["display"]
		if desva:
			
			pre_sim.hiperc_modelo_canal.ver_desvanecimiento_local(nombre="desvanecimiento")
		else:
			print("desvanecimiento desactivado, la grafica no se muestra")
			#eliminar, si.

		#eliminar todo despues de pre-simular
		pre_sim=0
		x_prueba=0
		y_prueba=0
		xx,yy=0,0


	def configurar_simulacion(self):
		'''Modulo de simulacion.'''
		pass


if __name__=="__main__":
	#Prototipo:
	pass
else:
	print("Modulo Importado: [", os.path.basename(__file__), "]")
