#import
import matplotlib.pyplot as plt
from matplotlib.patches import RegularPolygon
import numpy as np
#
import pk_red_dispositivos.celda as prd

def prueba_pk_dispositivos():
	colmena=prd.Celdas(3,4)
	ax=colmena.dibujar_celdas()
	plt.show()


if __name__=="__main__":
	#Prototipo:
	#prd.Celdas(1,100)
	prueba_pk_dispositivos()
	#prd.modulo_coordenadas.coordenadas_nceldas(3,4)

else:
	print("Modulo <escribir_nombre> importado")
