import matplotlib.pyplot as plt
#import modulo_circulos as mc
import numpy as np
import math
import random
import time
#http://webs.ucm.es/info/aocg/python/optica/interferencias/index.html
#http://stg-pepper.blogspot.com/2015/03/grafica-de-un-patron-de-radiacion-3d.html

#https://github.com/rilma/Antenna-Pattern
#https://medium.com/@johngrant/antenna-arrays-and-python-plotting-with-pyplot-ae895236396a
#https://medium.com/python-pandemonium/antenna-arrays-and-python-calculating-directivity-84a2cfea0739

class Antena:
	'''Clase que modela el patron de radiacion de una antena deseada'''
	def __init__(self, params):
		#entrada
		self.referencia=params[0]
		self.hpbw=params[1]
		self.ganancia_tx=params[2]
		self.a_min=params[3]
		self.apuntamiento=params[4]
		self.hiper_ganancias=params[5] #angulos de usuarios

		#auxiliar
		apunt_intersec=np.array(params[3])
		self.apunt_trisec=np.where(apunt_intersec>180, apunt_intersec-360, apunt_intersec)
		#
		self.angulos=0 #0 cuando no este en pruebas

		#salida
		self.patron_radiacion=0
		self.patron_radiacion_3s=0


		#inicializar
		if self.referencia=="4g":
			self.inicializar_ts_38942()
		elif self.referencia=="5G":
			pass
		else:
			pasos


	def inicializar_ts_38942_old(self):
		'''Modela el tipo de antena TS 36.942.
		Ver: https://www.etsi.org/deliver/etsi_tr/136900_136999/136942/08.02.00_60/tr_136942v080200p.pdf'''
		#print(angulos_x) #ok. Angulos discretos entre -180 a 180
		self.angulos=np.linspace(-180.0,180.0, 361)
		#no es neceario.
		##angulos_rad=((self.angulos*math.pi)/180)
		##print("angulos rad->",angulos_rad)

		at_in=12.0*((self.angulos/self.hpbw)**2)
		self.patron_radiacion=np.roll(-1*np.minimum(at_in, self.a_min), 45)
		self.patron_radiacion=-1*np.minimum(at_in, self.a_min)

		#angulos fijos, pueden alterarse con #import modulo_circulos as mc. No recomendado.
		#print(mc.calcular_angulo_v3(0,120))
		#dado una angulo inicial y la diferencia entre ellos, calcula la trisectorizacion.
		#apuntamiento=mc.calcular_angulo_v3(45,120)
		#print(apuntamiento)
		#CAMBIAR EL FIRST self.a_min por la ganancia de tx
		patron_1=np.roll(15-1*np.minimum(at_in, self.a_min), 45)
		patron_2=np.roll(15-1*np.minimum(at_in, self.a_min), 165)
		patron_3=np.roll(15-1*np.minimum(at_in, self.a_min), 285)

		'''Requerimiento, filtra en las posiciones de interseccion'''

		#patron_1=np.where(patron_1<0 or patron_1>, 0, patron_1) #el patron solo acepta entre -180 a 180.
		patron_completo=patron_1+patron_2+patron_3

		'''Funciona para angulos n=360, osea discretos, pero los arrays disponibles no tiene esa forma.

		Por eso, cuando la lista de angulos no es 361, al mover roll con un angulo cualquiera, no
		se obtiene el deseado.'''

		#que rayos fue lo que hice lol
		#A cada angulo radian, se sumo un corrimiento de tal forma que se traslada el patron de radiacion.
		#por que tiene que ser radian? Lo dice matplotlib.

		plt.polar(np.radians(self.angulos)+math.radians(45), self.patron_radiacion, '-r')
		plt.polar(np.radians(self.angulos)+math.radians(165), self.patron_radiacion, '-r')
		plt.polar(np.radians(self.angulos)+math.radians(285), self.patron_radiacion, '-r')
		plt.title("Patron superpuesto")
		plt.figure()
		'''
		#angulos->no es posible, tiene que ser en radianes.
		#plt.polar(np.radians(self.angulos)+np.radians(45), self.patron_radiacion, '-r')

		#polar limpio para observar el comportamiento cuando se modifican los angulos desde el principio
		#plt.polar(np.radians(self.angulos), self.patron_radiacion, '-r')
		'''
		plt.polar(np.radians(self.angulos), patron_completo, '-r')
		plt.title("Patron sumado POLAR")
		plt.figure()
		#plt.plot(self.angulos,self.patron_radiacion, 'ro')
		plt.plot(self.angulos,patron_completo, 'ro')
		plt.title("Patron sumado CARTE")
		plt.figure()
		plt.plot(self.angulos, patron_1)
		plt.plot(self.angulos, patron_2)
		plt.plot(self.angulos, patron_3)
		plt.title("Patron superpuesto CART*")


		#arrays internos todos deben tener la misma dimension


		res2=np.interp(self.hiper_ganancias,self.angulos,patron_completo)
		#print(test, res2)
		#res=interpol(test)

		'''Como hacer para cambiar el apuntamiento desde la misma ecuacion.

		Proposito, cambiar la direccion de cada lobulo, sumarlo y obtener una sola matriz.

		Requerimiento. Con un solo patron de radiacion y angulos, obtener los tres sectores.

		Ideas modulo entre -180 y 180. Funcion roll. A modo de venta.
		No funciona por que mueve los puntos pero siempre mantiene su valor en el plot mas no en el orden.

		Idea 2.
		Convertir a cartesiana, mover, sumar y retornar

		Idea 3. Con la actual inmplementacion, dado un angulo theta, calcular el valor de interpolacion
		del dataset disponible.

		Se puede hacer interpolación a un array con valores negativos?
		'''

	def inicializar_ts_38942(self):
		'''Modela el tipo de antena TS 36.942.
		Ver: https://www.etsi.org/deliver/etsi_tr/136900_136999/136942/08.02.00_60/tr_136942v080200p.pdf'''
		#print(angulos_x) #ok. Angulos discretos entre -180 a 180
		self.angulos=np.linspace(-180.0,180.0, 361)

		at_in=12.0*((self.angulos/self.hpbw)**2)
		self.patron_radiacion=np.roll(-1*np.minimum(at_in, self.a_min), 45)
		self.patron_radiacion=-1*np.minimum(at_in, self.a_min)

		#angulos fijos, pueden alterarse con #import modulo_circulos as mc. No recomendado.
		#print(mc.calcular_angulo_v3(0,120))
		#dado una angulo inicial y la diferencia entre ellos, calcula la trisectorizacion.
		#apuntamiento=mc.calcular_angulo_v3(45,120)
		#print(apuntamiento)
		#CAMBIAR EL FIRST self.a_min por la ganancia de tx
		patron_1=np.roll(self.a_min-1*np.minimum(at_in, self.a_min), 45)
		patron_2=np.roll(self.a_min-1*np.minimum(at_in, self.a_min), 165)
		patron_3=np.roll(self.a_min-1*np.minimum(at_in, self.a_min), 285)
		#
		plt.plot(self.angulos, patron_1,'ro')
		plt.plot(self.angulos, patron_2,'go')
		plt.plot(self.angulos, patron_3,'bo')
		plt.title("Patron superpuesto CART*ANTES")
		plt.figure()

		'''Requerimiento, filtra en las posiciones de interseccion'''
		limite=self.calcular_interseccion(patron_1,patron_2)
		patron_1=np.where(patron_1<=limite, 0, patron_1)
		patron_2=np.where(patron_2<=limite, 0, patron_2)
		patron_3=np.where(patron_3<=limite, 0, patron_3)

		patron_completo=patron_1+patron_2+patron_3
		#quito los ceros resultantes
		patron_completo=np.where(patron_completo<=0, limite, patron_completo) #el patron solo acepta entre -180 a 180.
		patron_completo=patron_completo-(self.a_min-self.ganancia_tx)
		print("diferencia ", self.a_min-self.ganancia_tx)
		plt.polar(np.radians(self.angulos)+math.radians(45), self.patron_radiacion, '-r')
		plt.polar(np.radians(self.angulos)+math.radians(165), self.patron_radiacion, '-r')
		plt.polar(np.radians(self.angulos)+math.radians(285), self.patron_radiacion, '-r')
		plt.title("Patron superpuesto")
		plt.figure()
		#

		plt.polar(np.radians(self.angulos), patron_completo, '-r')
		plt.title("Patron sumado POLAR")
		plt.figure()


		plt.plot(self.angulos,patron_completo, 'ro')
		plt.title("Patron sumado CARTE")
		plt.figure()
		plt.plot(self.angulos, patron_1,'ro')
		plt.plot(self.angulos, patron_2,'go')
		plt.plot(self.angulos, patron_3,'bo')
		plt.title("Patron superpuesto CART*")
		#arrays internos todos deben tener la misma dimension
		res2=np.interp(self.hiper_ganancias,self.angulos,patron_completo)
		'''Requerimiento, que ocurre cuando la ganancia no es amin? pues no funciona todo lo anterior haha
		Revisar los resultados, no parece que sean certeros.'''




	def calcular_interseccion_not(self):
		'''Dado una lista de angulos y el hpdw, calcula los nuevos angulos de interseccion'''
		print(self.apunt_trisec)
		for angulo in self.apunt_trisec:
			print(angulo+self.hpbw*0.5, angulo-self.hpbw*0.5, )

	def calcular_interseccion(self, patron1,patron2):
		'''Dada dos funciones, encuentra el punto donde ambos tienen la misma magnitud'''
		limite=0
		for f1,f2 in zip(patron1,patron2):
			if f1==f2:
				print(f1,f2)
				limite=f1
		return limite



if __name__=="__main__":
	#Implementación.
	#=10
	#horn()
	import modulo_circulos as mc
	hpbw=55
	amin=20
	ref="4g"
	gtx=15
	apunt=mc.calcular_angulo_v3(45,120) #inicio,angulo de particion.
	tar=np.array([45, 90, 180, -1, -179])
	#test=np.stack(np.array([  [4,5,9.11 ,14.3 , 7.05],[3.4, 5, 6.7, 7.8, 8.9] ]))
	parametros=[ref, hpbw, gtx, amin, apunt, tar]
	antena_prueba=Antena(parametros)
	plt.grid(True)
	#plt.minorticks_on()
	#print(antena_prueba.angulos)
	#plt.plot(antena_prueba.angulos,antena_prueba.patron_radiacion)
	plt.show()
	#theta_mod=self.angulos%360
	#print("theta mod",theta_mod)



else:
	print("Modulo Antena importado")
