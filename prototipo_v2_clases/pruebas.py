#import
import matplotlib.pyplot as plt
from matplotlib.patches import RegularPolygon
import numpy as np
#
import pk_red_dispositivos.celda as pkcel


def prueba_pk_dispositivos():
	colmena=pkcel.Celdas(3,4)
	ax=colmena.ver_celdas()
	plt.show()


if __name__=="__main__":
	#Prototipo:
	#pkcel.Celdas(1,100)
	prueba_pk_dispositivos()

	#pkcel.modulo_coordenadas.coordenadas_nceldas(3,4)

else:
	print("Modulo <escribir_nombre> importado")
