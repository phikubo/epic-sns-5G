#import
import matplotlib.pyplot as plt
from matplotlib.patches import RegularPolygon
import numpy as np
#
import pk_red_dispositivos.celda as prdcel
#import utilidades.mod_circulos as utc
from . import utilidades as ut

def prueba_pk_dispositivos():
	colmena=prdcel.Celdas(3,4)
	ax=colmena.dibujar_celdas()
	plt.show()


if __name__=="__main__":
	#Prototipo:
	#prdcel.Celdas(1,100)
	prueba_pk_dispositivos()
	angulos=ut.mod_operaciones.azimut_lista(30)
	print(angulos)
	#prdcel.modulo_coordenadas.coordenadas_nceldas(3,4)

else:
	print("Modulo <escribir_nombre> importado")
