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

def gestionar_celdas(nivel, radio_ext):
	'''Main celdas. Gestiona tres elementos, celdas, distribucion de usuarios
	 (ppp) y tri-sectorizacion.'''
	coordenada_axial=pkg1.mod_patron_circular.ensamblar(nivel)
	cartx,carty=pkg1.mod_celda.mapear_coordenadas_cartesianas(coordenada_axial, radio_ext, nivel)
	ax=pkg1.mod_celda.dibujar_celdas(cartx,carty, radio_ext)
	azimuts=prot_funciones_especiales.prot_operaciones.azimut_lista(30)
	print(azimuts)
	
	apotema=math.sqrt(radio_ext**2 -(0.5*radio_ext)**2)
	
	#segmento_interno =2*apotema_tri
	##pero segmento_interno = radio_ext, haciendo el cambio de variable:
	apotema_trisec= radio_ext/2 #relaciono el apotema tri con el radio celda grande
	radio_trisec =2*apotema_trisec* math.sqrt((4/3))
	
	#test_radio=radio_ext - apotema, aproximado pero no igual
	#radio_circular=radio_ext+test_radio
	radio_circular=radio_trisec
	cir_x,cir_y,angulo_x,angulo_y=prot_funciones_especiales.prot_circulo_angulo.coordenadas_circulo(radio_circular,azimuts)
	plt.plot(cir_x,cir_y, 'g') #np variables, contienen una circunferencia
	pkg1.mod_celda.tri_sectorizar(angulo_x,angulo_y,radio_circular, ax)	
	 
if __name__=="__main__":
	#Prototipo: FUNCION MAIN QUE GOBIERNA TODAS LOS SCRIPTS, FUNCION MAIN QUE BUSCA TODOS LOS SCRIPTS
	print("--------------------------------------")
	print("Ash nazg durbatulûk, ash nazg gimbatul")
	print("--------------------------------------")
	entries = os.listdir()
	print(os.listdir())
	mi_nivel=1
	mi_radio_ext=100/10 #10 decametros
	gestionar_celdas(mi_nivel,mi_radio_ext)
	mis_angulos=[0, 90]
	#pca.dibujar_circulo(radio, angulos)
	plt.savefig("pkg1durbatuluk_fix_radius_tri.pdf")
	plt.show()
else:
	print("Modulo <ring of power> importado")
