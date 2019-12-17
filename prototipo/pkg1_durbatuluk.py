#
import matplotlib.pyplot as plt
from matplotlib.patches import RegularPolygon
import numpy as np
import math
import time #debug
import os

import pkg1.mod_celda
import pkg1.mod_patron_circular
#
import prot_funciones_especiales.prot_circulo_angulo
import prot_funciones_especiales.prot_operaciones
import prot_funciones_especiales.prot_poissonpp
import GUI_thrakatuluk as gth

def gestionar_celdas(nivel, radio_ext,intensity):
	'''Main celdas. Gestiona tres elementos, celdas, distribucion de usuarios
	 (ppp) y tri-sectorizacion.'''
	coordenada_axial=pkg1.mod_patron_circular.ensamblar(nivel) #genera coordenadas axiales en n niveles
	cartx,carty=pkg1.mod_celda.mapear_coordenadas_cartesianas(coordenada_axial, radio_ext, nivel) #axial a cartesiano
	#cartx, carty son los centros de cada celda macro
	ax=pkg1.mod_celda.dibujar_celdas(cartx,carty, radio_ext) #dibuja celdas, retorna la grafica.
	print("tamano arreglo, cartx", len(cartx))
	azimuts=prot_funciones_especiales.prot_operaciones.azimut_lista(30)
	#print(azimuts)
	
	apotema=math.sqrt(radio_ext**2 -(0.5*radio_ext)**2)
	'''task4. Esta operacion de ajuste de radios, debe calcularse dentro de prot_celdas-terminado'''
	#segmento_interno =2*apotema_tri
	##pero segmento_interno = radio_ext, haciendo el cambio de variable:
	apotema_trisec= radio_ext/2 #relaciono el apotema tri con el radio celda grande
	radio_trisec =2*apotema_trisec* math.sqrt((4/3)) #radio a partir del apotema
	
	#test_radio=radio_ext - apotema, aproximado pero no igual
	#radio_circular=radio_ext+test_radio
	radio_circular=radio_trisec
	cir_x,cir_y,angulo_x,angulo_y=prot_funciones_especiales.prot_circulo_angulo.coordenadas_circulo(radio_circular,azimuts)
	plt.plot(cir_x,cir_y, 'g') #np variables, contienen una circunferencia
	pkg1.mod_celda.tri_sectorizar(angulo_x,angulo_y,radio_circular, ax, cartx,carty)
	'''fin trisectorizar'''
	#Poisson tambien debe hacerse en prot_celda
	#intensity=gth.get_dato()
	#x_ppp,y_ppp=prot_funciones_especiales.prot_poissonpp.distribuir_circulo(0.5*radio_ext,0.5*radio_ext*x, 0.5*radio*y, intensity)
	x_ppp,y_ppp=prot_funciones_especiales.prot_poissonpp.distribuir_circulo(apotema,0, 0, intensity)#puntero origen de la celda 
	'''task 5. distribuir en cada celda, radio = apotema'''
	#plt.scatter(x_ppp,y_ppp, edgecolor='b', facecolor='none', alpha=0.5 )

	coordenada_np_x, coordenada_np_y=prot_funciones_especiales.prot_poissonpp.distribuir_en_celdas(apotema,cartx, carty, intensity)
	plt.scatter(coordenada_np_x,coordenada_np_y, edgecolor='b', facecolor='none', alpha=0.5 )
	
	plt.savefig("all_ppp_trisec.jpg")
	plt.show()
	
	print("Terminado exitosamente")	
	 
if __name__=="__main__":
	#Prototipo: FUNCION MAIN QUE GOBIERNA TODAS LOS SCRIPTS, FUNCION MAIN QUE BUSCA TODOS LOS SCRIPTS
	print("--------------------------------------")
	print("Ash nazg durbatulûk, ash nazg gimbatul")
	print("--------------------------------------")
	entries = os.listdir()
	print(os.listdir())


	#Interfaz.GUI.thrakatuluk.SimulatorApp().run()
	mi_nivel=2
#	mi_nivel,radio_extq,inten=Interfaz.GUI.thrakatuluk.btn()
#	print("nivel  ",mi_nivel,"radio  ",radio_extq,"intensidad PPP ",inten)
	mi_radio_ext=100/10 #10 decametros
	gestionar_celdas(mi_nivel,mi_radio_ext)
	mis_angulos=[0, 90]

	#pca.dibujar_circulo(radio, angulos)

	
else:
	print("Modulo <ring of power> importado")
