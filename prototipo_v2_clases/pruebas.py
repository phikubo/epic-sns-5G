# import
import matplotlib.pyplot as plt
from matplotlib.patches import RegularPolygon
import numpy as np
#
import pk_red_dispositivos.celda as pkcel
import utilidades.savedata as persistencia


def prueba_pk_dispositivos(celdas, radio, intensidad):
	'''Prueba para observar funcionamiento de graficas basicas'''
	intensidad = intensidad/radio**2
	colmena = pkcel.Celdas(celdas, radio, distribucion=("ppp", intensidad))
	colmena.ver_estaciones_base()
	colmena.ver_celdas()
	colmena.ver_sectores()
	colmena.ver_usuarios()
	# colmena.ver_todo()
	# plt.axis("equal")
	# plt.grid(True)
	# plt.savefig("base_datos/img_pruebas/ppp_4.png")
	# plt.show()


def prueba_guardar_datos():
	'''Prueba para observar comportamiento de guardado de datos'''
	# procedimiento
	# 1. obtener todos los arrays en la posision x o y.
	# 2. juntar todos los arrays en un solo array
	# 3. usar metodo correspondiente para guardar el array
	# 4. abrir el archivo con el metodo correspondiente.
	# Nota: resulta un paso extra (extra=ineficiente) por el hecho
	# de que los datos ya estan juntos en una sola variable, pero no
	# estan separados por celda
	radio = 20
	intensidad = 7
	intensidad = intensidad/radio**2
	celdas = 3
	colmena = pkcel.Celdas(celdas, radio, distribucion=("ppp", intensidad))
	# colmena.cluster --> se encuentra cada celda, y cada celda tiene las coordenadas x.
	# si iteramos sobre cada celda y obtenemos cada x, los podemos agrupar en una lista
	# en lo que podemos aplicar el metodo presente en savedata.
	print(len(colmena.cluster))
	#data = colmena.cluster[0].user_x
	#print(data)
	test = [celula.user_x for celula in colmena.cluster]
	data = test[0]
	print(data)
	tamano_cluster=len(test)
	for i in range(tamano_cluster-1):
		try:
			data=np.column_stack((data,test[i+1]))
		except Exception as esx:
			print(esx) #esta excepcion ocurre por el [i+1], cuando llega a 3+1=4; de 0 a 4, el 4 seria el 5
	print(data)
	header="x1, x2, ..., xn"
	nombre_archivo=persistencia.nombre_extension("base_datos","txt","reconocimiento")
	persistencia.guardar_archivo(data, nombre_archivo, header)

	# data=x1
    # for i in range(len(lista)):
    #    try:
    #        data=np.column_stack((data,lista[i+1]))
    #    except Exception as esx:
    #        print(esx) #esta excepcion ocurre por el [i+1], cuando llega a 3+1=4; de 0 a 4, el 4 seria el 5
    # print(data)

	


if __name__=="__main__":
	# Prototipo:
	# prueba_pk_dispositivos(celdas=2,radio=20,intensidad=5)

	# pkcel.modulo_coordenadas.coordenadas_nceldas(3,4)

	prueba_guardar_datos()

else:
	print("Modulo <escribir_nombre> importado")
