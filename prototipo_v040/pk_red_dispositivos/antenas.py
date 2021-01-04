import matplotlib.pyplot as plt
#import modulo_circulos as mc
import numpy as np
import math
import random
import time
import os
#http://webs.ucm.es/info/aocg/python/optica/interferencias/index.html
#http://stg-pepper.blogspot.com/2015/03/grafica-de-un-patron-de-radiacion-3d.html

#https://github.com/rilma/Antenna-Pattern
#https://medium.com/@johngrant/antenna-arrays-and-python-plotting-with-pyplot-ae895236396a
#https://medium.com/python-pandemonium/antenna-arrays-and-python-calculating-directivity-84a2cfea0739

class Antena:
	'''Clase que modela el patron de radiacion de una antena deseada'''
	def __init__(self, cfg, angs):
		#entrada
		self.cfg=cfg
		self.hiper_angulos=angs #angulos de usuarios
		#para mayor claridad
		self.ganancia_tx=self.cfg["params_ant"][1]
		#self.referencia=cfg["tipo"]
		#self.cfg["hpbw"]=cfg[1]
		#self.ganancia_tx=cfg[2]
		#self.cfg["atmin"]=cfg[3]
		#self.apuntamiento=cfg[4]



		'''
		print("-------------------------------------")
		print("-------------------------------------")
		print("-------------------------------------")
		print("-------------------------------------")
		print("[DEBUG.Antenas]")
		print("parametros",cfg[0], "-",cfg[1], "-",cfg[2], "-",cfg[3], "-",cfg[4], "-",cfg[5].shape)
		print("-------------------------------------")
		print("-------------------------------------")
		print("-------------------------------------")
		'''
		#auxiliar
		#retoma los valores de
		#####################apunt_intersec=np.asarray(cfg[4])
		#print(apunt_intersec)
		###########self.apunt_trisec=np.where(apunt_intersec>180, apunt_intersec-360, apunt_intersec)
		#print(self.apunt_trisec)
		#
		#self.angulos=0 #0 cuando no este en pruebas
		#se define la ecuacion de patron de radiacion para -180,180.
		#se genera 360 puntos para lograr desplazar mas adelante los patrones con la funcion roll
		self.angulos=np.linspace(-180.0,180.0, 361)
		#salida
		self.relacion_angulos=0 #funcion generadora
		self.patron_radiacion_3s=[] #informacion de los tres sectores
		self.patron_radiacion=0 #el patron de radiacion resultante
		self.hiper_ganancias=0 #ganancia resultante
		#
		#inicializar
		if self.cfg["tipo"]=="4g":
			self.inicializar_ts_38942()
		elif self.cfg["tipo"]=="5G":
			pass
		else:
			pass
		#
		#conforma los sectores, de acuerdo a la referencia previa donde se generan los lobulos.
		self.conformar_sectores()
		#interpola los resultados anteriores, con los angulos de entrada y se obtiene la ganancia relativa de todos los usuarios.
		self.interpolar_resultados()
	#---------------------------------------------------------------------------
	#---------------------------------------------------------------------------
	#							OPERACIONES
	#---------------------------------------------------------------------------
	#---------------------------------------------------------------------------
	def inicializar_ts_38942(self):
		'''Modela el tipo de antena TS 36.942, en tres sectores
		Ver: https://www.etsi.org/deliver/etsi_tr/136900_136999/136942/08.02.00_60/tr_136942v080200p.pdf'''
		#ecuacion de la ts
		self.relacion_angulos=12.0*((self.angulos/self.cfg["hpbw"])**2) #antes at_int
		#sector, con corrimiento en angulos para desplazarlos en x, el numero de grados necesarios.
		#se eleva la funcion al piso 0 para sumarlas despues.
		#adicion04
		sector_1=np.roll(self.cfg["atmin"]-1*np.minimum(self.relacion_angulos, self.cfg["atmin"]), self.cfg["params_ant"][0][0])
		sector_2=np.roll(self.cfg["atmin"]-1*np.minimum(self.relacion_angulos, self.cfg["atmin"]), self.cfg["params_ant"][0][1])
		sector_3=np.roll(self.cfg["atmin"]-1*np.minimum(self.relacion_angulos, self.cfg["atmin"]), self.cfg["params_ant"][0][2])
		self.patron_radiacion_3s=[sector_1,sector_2,sector_3]


	def conformar_sectores(self):
		'''Conforma un patron de radiacion unico, dado los valores de ecuacion de patron de radiacion deseado'''
		#calculo el valor de magnitud correspondiente a la interseccion entre ambas graficas.
		limite=self.calcular_interseccion(self.patron_radiacion_3s[0],self.patron_radiacion_3s[1])
		#elimino la magnitud por debajo de la interseccion de valor limite
		patron_0=np.where(self.patron_radiacion_3s[0]<=limite, 0, self.patron_radiacion_3s[0])
		patron_1=np.where(self.patron_radiacion_3s[1]<=limite, 0, self.patron_radiacion_3s[1])
		patron_2=np.where(self.patron_radiacion_3s[2]<=limite, 0, self.patron_radiacion_3s[2])
		patron_completo=patron_0+patron_1+patron_2
		#cuando se realiza el procedimiento anterior, se generan 0 en el piso, modifica el patron.
		#para eliminarlos, los remplazamos con el valor del limite en esa posicion.
		patron_completo=np.where(patron_completo<=0, limite, patron_completo)
		#relaciono el patron de radiacion con la ganancia de trasmision, al disminuir la grafica
		#del valor piso de atenuacion, la diferencia entre la ganancia y el piso.
		self.patron_radiacion=patron_completo-(self.cfg["atmin"]-self.ganancia_tx)


	def interpolar_resultados(self):
		'''Interpola los angulos con el patron de radiacion, y generar el valor de ganacia resulte'''
		self.hiper_ganancias=np.interp(self.hiper_angulos,self.angulos,self.patron_radiacion)


	def calcular_interseccion_not(self):
		#DEPLETED
		'''Dado una lista de angulos y el hpdw, calcula los nuevos angulos de interseccion'''
		print(self.apunt_trisec)
		for angulo in self.apunt_trisec:
			print(angulo+self.cfg["hpbw"]*0.5, angulo-self.cfg["hpbw"]*0.5, )


	def calcular_interseccion(self, patron1,patron2):
		'''Dada dos funciones, encuentra el punto donde ambos tienen la misma magnitud'''
		limite=0
		for f1,f2 in zip(patron1,patron2):
			if f1==f2:
				#print(f1,f2)
				limite=f1
		return limite
	#---------------------------------------------------------------------------
	#---------------------------------------------------------------------------
	#							VISUALIZACION
	#---------------------------------------------------------------------------
	#---------------------------------------------------------------------------
	def observar_patron(self):
		#DEPLETED
		'''Grafica los patrones de radiacion. No terminado.'''
		plt.figure()
		patron_original=-1*np.minimum(self.relacion_angulos, self.cfg["atmin"])
		plt.plot(self.angulos, patron_original)
		plt.title("Patron original, piso a_min")

		plt.figure()
		plt.plot(self.angulos, self.patron_radiacion_3s[0])
		plt.plot(self.angulos, self.patron_radiacion_3s[1])
		plt.plot(self.angulos, self.patron_radiacion_3s[2])
		plt.title("[CART] Patron superpuesto *ANTES. Piso 0")

		plt.figure()
		plt.plot(self.angulos, self.patron_radiacion)
		plt.title("[CART] Patron final sumado. f(gtx, a_min)")

		plt.figure()
		patron_original=-1*np.minimum(self.relacion_angulos, self.cfg["atmin"])
		plt.polar(np.radians(self.angulos)+math.radians(45), patron_original, '-r')
		plt.polar(np.radians(self.angulos)+math.radians(165), patron_original, '-r')
		plt.polar(np.radians(self.angulos)+math.radians(285), patron_original, '-r')
		plt.title("[POL] Patron original superpuesto, desplazado, piso a_min")

		plt.figure()
		plt.polar(np.radians(self.angulos), self.patron_radiacion+(self.cfg["atmin"]-self.ganancia_tx), '-r')
		plt.title("[POL] Patron final, piso 0 (invertido)")

		plt.figure()
		plt.polar(np.radians(self.angulos), self.patron_radiacion, '-r')
		plt.title("[POL] Patron final, filtrado, sumado. f(gtx)")

		#plt.grid(True)
		#plt.show()

	#ADICIONAR01
	def ver_patron_local(self, nombre):
		#DEPLETED.
		'''Unicamente para la presimulacion'''
		plt.figure()
		plt.polar(np.radians(self.angulos), self.patron_radiacion, '-r')
		plt.title("[POL] Patron de Radiación Tipo: {}, Hbpw:{}.".format(self.cfg["tipo"], self.cfg["hpbw"]))
		ruta="base_datos/imagenes/presim-{}.png".format(nombre)
		plt.savefig(ruta)


if __name__=="__main__":
	#Implementación.
	import modulo_circulos as mc
	hpbw=55
	amin=20
	ref="4g"
	gtx=15
	apunt=mc.calcular_angulo_v3(45,120) #inicio,angulo de particion.
	tar=np.array([45, 90, 180, -1, -179])

	#tar=np.stack(np.array([  [4,5,9.11 ,14.3 , 7.05],[3.4, 5, 6.7, 7.8, 8.9] ]))
	#empaqueta los parametros en ese mismo orden.
	parametros=[ref, hpbw, gtx, amin, apunt, tar]
	#crea la instancia de antena.
	antena_prueba=Antena(parametros, 0)
	#comprueba el nuevo patron.
	antena_prueba.observar_patron()
	#print(antena_prueba.hiper_ganancias)

	#aprobado por phikubo


else:
	print("Modulo Importado: [", os.path.basename(__file__), "]")
