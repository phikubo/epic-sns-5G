#import
#import prot_grid.prot_filesistem
#
import matplotlib.pyplot as plt
from matplotlib.patches import RegularPolygon
import numpy as np
import math
import time #debug
import os


#from prot_grid import *
import prot_grid.prot_patron_hexagonal_circular as phcc
import prot_grid.blank
#import prot_grid.prot_celda as pcel
def gestionar_celdas(nivel, radio_ext):

	'''Main celdas. Gestiona tres elementos, celdas, distribucion de usuarios
	 (ppp) y tri-sectorizacion.'''
	#coordenadas_axiales = phcc.ensamblar(nivel)
	#cartesian_x,cartesian_y= pceld.mapear_coordenadas_cartesianas(coordenadas_axiales, radio_ext)


if __name__=="__main__":
	'''Ash nazg durbatulûk, ash nazg gimbatul'''
	#Prototipo: FUNCION MAIN QUE GOBIERNA TODAS LOS SCRIPTS, FUNCION MAIN QUE BUSCA TODOS LOS SCRIPTS
	entries = os.listdir()
	print(os.listdir())
	nivel=1
	radio_ext=100/10 #10 decametros
	gestionar_celdas(nivel,radio_ext)
	radio=10
	angulos=[0, 90]
	pca.dibujar_circulo(radio, angulos)
	plt.show()
else:
	print("Modulo <ring of power> importado")
