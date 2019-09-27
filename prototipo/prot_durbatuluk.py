#
import matplotlib.pyplot as plt
from matplotlib.patches import RegularPolygon
import numpy as np
import math
import time #debug
import os

import pkg1.mod_celda
import pkg1.blank
def gestionar_celdas(nivel, radio_ext):
	'''Main celdas. Gestiona tres elementos, celdas, distribucion de usuarios
	 (ppp) y tri-sectorizacion.'''
	coordenada_axial=pkg1.blank.ensamblar(nivel)
	cartx,carty=pkg1.mod_celda.mapear_coordenadas_cartesianas(coordenada_axial, radio_ext, nivel)
	pkg1.mod_celda.dibujar_celdas(cartx,carty, radio_ext)
	
	 
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
	plt.show()
else:
	print("Modulo <ring of power> importado")
