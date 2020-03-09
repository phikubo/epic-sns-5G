# import
import matplotlib.pyplot as plt
from matplotlib.patches import RegularPolygon
import numpy as np
import os
#
import pk_red_dispositivos.celda as pkcel
import utilidades.savedata as persistencia
import pk_modelo_canal.modelo_canal as moca
import sistema as ss
#http://research.iac.es/sieinvens/python-course/source/matplotlib.html #graficar datos
#me ga bru tal https://jakevdp.github.io/PythonDataScienceHandbook/04.05-histograms-and-binnings.html
#https://stackabuse.com/python-data-visualization-with-matplotlib/


def prueba_perdidas_basicas():
	'''Funcion de prueba para crear las perdidas basicas (espacio libre)'''
	#pasos:
	#1. crear cluster, en la celda 0
	#2. obtener distancias
	#3. asignar perdidas de espacio libre mediante una funcion propia
	#4. relacionar clase modelo de canal con celda
	radio = 20 #u -> metro
	intensidad = 2
	intensidad = intensidad/radio**2
	celdas = 2
	colmena = pkcel.Celdas(celdas, radio, distribucion=("ppp", intensidad)) #en este momento hay dos celdas, con sus parametros definidos

	#[critico - IMPORTANTE LEER] hay dos opciones para implementar
	#1. opcion. crear instancia de las celdas, obtener distancia; crear instancia de modelo del canal
	# alimentarlo con distancias y frecuencia de operacion, calcular perdidas, retornar
	# alimentar celdas con las perdidas, resultado: ahora la celda tiene sus propias perdidas.
	#{phikubo says: de esta forma podria tenerse un modelo para todas las celdas, el cual funciona
	# como modulo. Sin embargo esto no aprovecha el potencial de la clase, pues si ese es el caso,
	# pues es mas sencillo implmentarlo como un modulo y no una clase. Con la clase se pueden guardar
	# mas parametros y establecer relaciones mas fuertes y complejas}

	#2. opcion. crear la instancia del modelo del canal, asignarlo a un parametro de la celda
	# y calcular las perdidas desde la variable de la instancia de la celda.
	#{phikubo says: esta opcion me parece mejor pues es mas directa,
	# esta implementacion aun no se hara sino en la siguiente version. La ventaja es
	# que se puede manipular el modelo del canal para cada celda y de manera independiente. Se puede
	# realizar combinaciones realmente complejas.}

	#implementacion opcion 1.
	celda_inicial=colmena.cluster[0] #objeto de la celda 0
	#opcion 1, como instancias diferentes
	distancias_celda_cero=celda_inicial.distancias #obtengo las distancias de esa celda
	freq=10 #asigno frecuencia en gigaz
	print("Asumiendo que las distancias son en [km] las siguientes: ")
	print(distancias_celda_cero) #asumiendo que la distancia esta en km
	modelo=moca.Modelo_canal(freq, distancias_celda_cero) #creo el modelo del canal
	print("las perdidas de esas distancias son: ")
	modelo.perdidas_espacio_libre_ghz() #calculo las perdidas
	print(modelo.path_loss)
	print("asignacion de las perdidas en esa celda")
	celda_inicial.basic_path_loss=modelo.path_loss
	print(celda_inicial.basic_path_loss)
	#o puede hacerse con la funcion (cuando se desee para varias celdas debe usarse esa funcion)
	celda_inicial.asignar_perdidas_espacio_libre(modelo.path_loss)
	print(celda_inicial.basic_path_loss)
	#cualequiera de las dos formas es valida, sien embargo para automatizar en el futuro, se
	#usuara la funcion llamada: asginar_perdias_espacio_libre(etc,)

	#implementacion opcion 2
	#1. creamos la instancia del modelo del canal
	#2. creamos instancia de la celdas (colmena)
		#recibe como parametro celdas, radio, distribucion Y modelo del canal (la instancia creada en 1.)
		#celdas entonces crea automaticamente las configuraciones para todas las celdas
		#es decir, crea perdidas_basicas, para todas las celdas.

		#esto implica dos cosas:
			#1. la clase celdas (sistema) crea perdidas para todas las celdas automaticamente
			#1.1 es necesario modificar la inicializacion de variables
			#2. la clase celda tiene como una de sus variables al modelo del canal, que es una
				#instancia de modelo del canal.
			#2.1 la clase celda entonces ejecuta desde si misma, las perdidas y todas
			#las funciones y facultades que tenga el modelo del canal.
			#2.2 esto implica modificar la clase celda para habilitar este cambio:
				#solo es necesario crear una variable self.modelo=0
				#la clase sistema le dara un modelo distinto a cada celda si es necesario
				#la clase celda ejecuta self.perdidas=self.modelo.perdidas_espacio_libre_ghz()
				#completando el ciclo


def prueba_perdidas_basicas_2():
	'''Funcion de prueba de concepto, clase como una relacion de composicion en la celda.'''
	#https://stackoverflow.com/questions/38657337/how-can-i-get-the-type-of-a-class-without-instantiating-it-in-python
	radio = 20 #u -> metro
	intensidad = 2
	intensidad = intensidad/radio**2
	celdas = 2
	clase=moca.Modelo_canal
	colmena = pkcel.Celdas(celdas, radio, distribucion=("ppp", intensidad),Modelo_Canal=clase) #en este momento hay dos celdas, con sus parametros definidos
	#la idea es tener una referencia a la clase sin crear el objeto para luego crear este objeto en otra clase
	print(moca.Modelo_canal)


def prueba_externa_0():
	'''Prueba. Comprobar la utilidad de este script'''
	celdas=3
	radio=20
	intensidad=10
	distribucion=(intensidad/radio**2,"ppp") #0 en el primer valor si es otra distribucion (no necesario)
	mod_canal=None
	sc=ss.Sistema_Celular(celdas,radio, distribucion, mod_canal)

if __name__=="__main__":
	#REGLAS:
	#0 [critico]. Las pruebas en if name, deben ir comentadas por prueba 1., prueba 2., ..., prueba n.
		#0.1 Si se necesitan hacer mas de una prueba con la funcion, pasar de 1 a 1.1 a 1.2, etc.
		#en el numeral de la prueba

	#1. LAS FUNCIONES DE PRUEBA NO RECIBEN PARAMETROS, Excepto en el siguiente caso:
		#Que la funcion sea definida con parametros y al llamarla sea explicito los
		#parametros y los valores que reciben
		# funcion(parametro=valor1, parametro2=valor, etc)
		#ver prueba 1.
	#2. LAS VARIABLES VAN EN MINUSCULA
	#3. LOS NOMBRE DE FUNCIONES, MINUSCULA
	#4. LAS INSTANCIAS DE CLASE, MINUSCULA
	#5. LOS NOMBRES DEBEN SER ESPECIFICOS Y SEPARADOS POR: _ así:
		#EjemploDeFUNCION ---> x , ejemplo_de_funcion ---> bieeeen
		#fdp ----------------> x , funcion_de_prueba ----> mega bieeeen
		#etc.
	prueba_externa_0()

else:
	print("Modulo Importado: [", os.path.basename(__file__), "]")
