#import
import matplotlib.pyplot as plt
from matplotlib.patches import RegularPolygon
import numpy as np
#
import pk_red_dispositivos.celda as pkcel


def prueba_pk_dispositivos():
	celdas=4
	radio=20
	intensidad=5
	intensidad=intensidad/radio**2
	colmena=pkcel.Celdas(celdas,radio, distribucion=("ppp", intensidad))
	colmena.ver_estaciones_base()
	colmena.ver_celdas()
	colmena.ver_sectores()
	colmena.ver_usuarios()
	plt.axis("equal")
	plt.grid(True)
	#plt.savefig("base_datos/img_pruebas/ppp_4.png")
	plt.show()
	


	


if __name__=="__main__":
	#Prototipo:
	#pkcel.Celdas(1,100)
	prueba_pk_dispositivos()

	#pkcel.modulo_coordenadas.coordenadas_nceldas(3,4)

else:
	print("Modulo <escribir_nombre> importado")
