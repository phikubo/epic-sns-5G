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

def horn(tilt):
	'''Modela el tipo de antena TS 36.942'''
	theta = np.linspace(-np.pi, np.pi, 361)
	theta2= np.linspace(-180.0,180.0, 361) #361 para una distribucion de 1 a 1
	ancho_3dB=30
	g_entrada=30
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




if __name__=="__main__":
	#Implementación.
	tilt=10
	horn(tilt)
else:
	print("Modulo Antena importado")
