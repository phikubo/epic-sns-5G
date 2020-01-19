#import
import matplotlib.pyplot as plt
from matplotlib.patches import RegularPolygon
import numpy as np
#
import pk_red_dispositivos.celda as pkcel


def prueba_pk_dispositivos():
	colmena=pkcel.Celdas(4,20)
	colmena.ver_estaciones_base()
	colmena.ver_celdas()
	colmena.ver_sectores()
	plt.axis("equal")
	plt.grid(True)
	#plt.savefig("base_datos/img_pruebas/test_4.png")
	plt.show()


if __name__=="__main__":
	#Prototipo:
	#pkcel.Celdas(1,100)
	prueba_pk_dispositivos()

	#pkcel.modulo_coordenadas.coordenadas_nceldas(3,4)

else:
	print("Modulo <escribir_nombre> importado")
