import matplotlib.pyplot as plt
import modulo_circulos as mc
import numpy as np
import math
import random
import time
#http://webs.ucm.es/info/aocg/python/optica/interferencias/index.html
#http://stg-pepper.blogspot.com/2015/03/grafica-de-un-patron-de-radiacion-3d.html

#https://github.com/rilma/Antenna-Pattern
#https://medium.com/@johngrant/antenna-arrays-and-python-plotting-with-pyplot-ae895236396a
#https://medium.com/python-pandemonium/antenna-arrays-and-python-calculating-directivity-84a2cfea0739

def horn():
	'''Modela el tipo de antena TS 36.942'''
	theta = np.linspace(-np.pi, np.pi, 361)
	theta2= np.linspace(-180.0,180.0, 361) #361 para una distribucion de 1 a 1
	ancho_3dB=65
	g_entrada=20
	#print(len(theta), len(theta2))
	#print(theta2)
	#for i in theta2:
	#	print(math.radians(i))
	#print(theta)
	#la funcion for y theta hacen lo mismo, es preferible la primera
	theta_mod=theta2%360
	#print(theta2)
	#print(len(theta_mod))
	#A_theta=[]
	#for i  in theta2:
	#	A_theta=-np.nanmin((12*(i/65)**2))
	#print(A_theta)
	at_in=(12.0*(theta2/ancho_3dB)**2)
	A_theta=-1*np.minimum(at_in, g_entrada)
	print(np.shape(A_theta), np.shape(theta2), np.shape(at_in))
	print("ok: ",np.shape(A_theta))

	A_theta_dif = A_theta - np.max(A_theta)
	#print("A_theta: ", A_theta )
	#print("Diferencia: ", A_theta_dif )
	#compara si A_theta y A_theta_dif, son iguales?
	#print(A_theta is A_theta_dif)

	#Esto quiere decir que son diferentes.
	print(mc.calcular_angulo_v3(0,120))
	apuntamiento=mc.calcular_angulo_v3(0,120)
	T=((theta2*math.pi)/180)
	print(np.shape(T))

	##plt.polar(theta2,A_theta_dif)
	##plt.plot(theta2,A_theta)
	plt.polar(T+math.radians(apuntamiento[0]), A_theta, '-r')
	plt.polar(T+math.radians(apuntamiento[1]), A_theta, '-r')
	plt.polar(T+math.radians(apuntamiento[2]), A_theta, '-r')
	plt.figure()
	plt.grid(True)
	plt.plot(theta2,A_theta)
	#plt.plot(theta2, A_theta_dif)
	plt.show()
	return 4, theta_mod, A_theta, A_theta_dif

class Antena:
	'''Clase que modela el patron de radiacion de una antena deseada'''
	def __init__(self, params):
		#entrada
		self.referencia=params[0]
		self.hpbw=params[1]
		self.a_min=params[2]

		#auxiliar
		self.angulos=0 #0 cuando no este en pruebas

		#salida
		self.patron_radiacion=0
		self.patron_radiacion_3s=0


		#inicializar
		if self.referencia=="ts38942":
			self.inicializar_ts_38942()
		else:
			pasos


	def inicializar_ts_38942(self):
		'''Modela el tipo de antena TS 36.942.
		Ver: https://www.etsi.org/deliver/etsi_tr/136900_136999/136942/08.02.00_60/tr_136942v080200p.pdf'''
		#angulos_x=np.linspace(-180.0,180.0, 361)
		#print(angulos_x) #ok. Angulos discretos entre -180 a 180
		#self.
		#print("angulos 180->",self.angulos)
		#no funciono self.angulos=np.roll(np.linspace(-180.0,180.0),50)
		self.angulos=np.linspace(-180.0,180.0, 361)
		print("angulos 180->",self.angulos)
		#self.angulos=np.linspace(0,360.0)
		#self.angulos=np.linspace(-180,360.0)

		#no es neceario.
		##angulos_rad=((self.angulos*math.pi)/180)
		##print("angulos rad->",angulos_rad)

		at_in=12.0*((self.angulos/self.hpbw)**2)
		self.patron_radiacion=np.roll(-1*np.minimum(at_in, self.a_min), 45)
		'''Funciona para angulos n=360, osea discretos, pero los arrays disponibles no tiene esa forma.

		Por eso, cuando la lista de angulos no es 361, al mover roll con un angulo cualquiera, no
		se obtiene el deseado.'''
		print("operacion--------------->\n", at_in)
		print("pr------------->\n", self.patron_radiacion)
		#que rayos fue lo que hice lol
		#A cada angulo radian, se sumo un corrimiento de tal forma que se traslada el patron de radiacion.
		#por que tiene que ser radian? Lo dice matplotlib.

		#print(mc.calcular_angulo_v3(0,120))
		#dado una angulo inicial y la diferencia entre ellos, calcula la trisectorizacion.
		apuntamiento=mc.calcular_angulo_v3(45,120)
		print(apuntamiento)
		#theta_mod=self.angulos%360
		#print("theta mod",theta_mod)


		#radianes
		#plt.polar(angulos_rad+math.radians(apuntamiento[0]), self.patron_radiacion, '-r')
		#plt.polar(angulos_rad+math.radians(apuntamiento[1]), self.patron_radiacion, '-r')
		#plt.polar(angulos_rad+math.radians(apuntamiento[2]), self.patron_radiacion, '-r')

		#angulos->no es posible, tiene que ser en radianes.
		#plt.polar(np.radians(self.angulos)+np.radians(45), self.patron_radiacion, '-r')

		#polar limpio para observar el comportamiento cuando se modifican los angulos desde el principio
		plt.polar(np.radians(self.angulos), self.patron_radiacion, '-r')

		#plt.figure()
		#plt.plot(self.angulos,self.patron_radiacion, 'ro')

		'''Como hacer para cambiar el apuntamiento desde la misma ecuacion.

		Proposito, cambiar la direccion de cada lobulo, sumarlo y obtener una sola matriz.

		Requerimiento. Con un solo patron de radiacion y angulos, obtener los tres sectores.

		Ideas modulo entre -180 y 180. Funcion roll. A modo de venta.
		No funciona por que mueve los puntos pero siempre mantiene su valor en el plot mas no en el orden.

		Idea 2.
		Convertir a cartesiana, mover, sumar y retornar

		Idea 3. Con la actual inmplementacion, dado un angulo theta, calcular el valor de interpolacion
		del dataset disponible.
		'''




if __name__=="__main__":
	#Implementación.
	#=10
	#horn()
	hpbw=65
	amin=20
	ref="ts38942"
	parametros=[ref, hpbw, amin]
	antena_prueba=Antena(parametros)
	plt.grid(True)
	#plt.minorticks_on()
	#print(antena_prueba.angulos)
	#plt.plot(antena_prueba.angulos,antena_prueba.patron_radiacion)
	plt.show()
else:
	print("Modulo Antena importado")
