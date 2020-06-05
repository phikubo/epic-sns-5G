# import
import matplotlib.pyplot as plt
from matplotlib.patches import RegularPolygon
import numpy as np
import os
#
import pk_red_dispositivos.celda as pkcel #ya no es necesario
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
	intensidad = 10
	#intensidad = intensidad/radio**2
	distribucion=(intensidad/radio**2,"ppp")
	mod_canal=None
	celdas = 2

	colmena = ss.Sistema_Celular(celdas, radio, distribucion, mod_canal) #en este momento hay dos celdas, con sus parametros definidos

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
	modelo=moca.Modelo_Canal(freq, distancias_celda_cero) #creo el modelo del canal
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
	referencia_clase=moca.Modelo_Canal
	colmena = pkcel.Celdas(celdas, radio, distribucion=("ppp", intensidad),Modelo_Canal=referencia_clase) #en este momento hay dos celdas, con sus parametros definidos
	#la idea es tener una referencia a la clase sin crear el objeto para luego crear este objeto en otra clase
	print(moca.Modelo_Canal)


def prueba_externa_0():
	'''PRUEBA. Comprobar la utilidad de este script'''
	celdas=3
	radio=20
	intensidad=10
	distribucion=(intensidad/radio**2,"ppp") #0 en el primer valor si es otra distribucion (no necesario)
	mod_canal=None
	sc=ss.Sistema_Celular(celdas,radio, distribucion, mod_canal)



def prueba_top_1_balance_del_enlace():
	'''Prueba para validar un balance del enlace simple (no 5G)

	1.DESIGN:
	1.1 Generar escenario (celdas->1, usuarios->1)
	1.2 Calcular distancias a la base
	1.3 Recibir parámetros: frecuencia de operacion, perdidas tx, ganancia tx
													perdidas rx, ganacia rx
	1.4 Calcular balance del enlace asi:
	Potencia del transmisor [dBm] – Pérdida en el cable TX [dB] + Ganancia de antena TX [dBi] –
	Pérdidas en la trayectoria del espacio abierto [dB] + Ganancia de antena RX [dBi] – Pérdidas en
	el cable del RX [dB] = Margen – Sensibilidad del receptor [dBm]
	DATOS DE PRUEBA
	+Cable de baja calidad
	+Distancia: 1 km (0,622 millas)
	+Frecuencia: 2,4 GHz
	+Cables y conectores -5 dB
	+Salida del transmisor +18 dBm
	+Antena TX +5 dBi
	*** FSL -100 dB
	+Antena RX + 8 dBi
	+Cables y conectores Rx -5 dB
	+Sensibilidad del receptor -92 dBm
	***Total: (margen) + 13 dB

	El margen de este enlace es de 13 dB, adecuado para ambientes urbanos y la potencia irradiada es de
	18 dBm (<100 mW), quiere decir que el enlace es legal en cualquier país.
	1.5 Generar graficas.
	'''
	#IMPLEMENTACION:
	celdas=2
	radio=1000#unidades->m ATENCION: EL RADIO DEFINE LAS UNIDADES, SI SON EN M O EN KM, LOS CALCULOS TAMBIEN.
	#requerimiento 1 usuarios-OK
	#requerimiento n usuarios (lista)-OK
	####################################1.1 Generar escenario (celdas->1, usuarios->1)
	distribucion=((np.array([[1000, 250]]),np.array([[0, 250]])),"prueba_unitaria")
	distribucion=((np.array([[1000, 250],[1500, 1000]]),np.array([[0, 250],[500, 1500]])),"prueba_unitaria") #celdas=2
	#este formato (arriba) de la tupla no es correcto, por que la listas de n_usuarios
	#se guardan asi: [[celda0],[celda1],...,[celdan]]
	mod_perdidas="espacio_libre" #espacio_libre, rappaport, ci, ts901. TUPLA: (tipo, perdidas_tx, perdidas_rx, ganancia_rx,ganancia_tx, sensibilidad)
	'''IMPORTANTE: al incluir el modelo desde aca, puedo tener 2 tier o layer de Celdas
	#un modelo de celdas para umi y otro para uma de forma independiente, ahora como se relacionan?'''
	mono_celda=ss.Sistema_Celular(celdas,radio, distribucion, mod_perdidas)
	celda_0=mono_celda.cluster[0] #objeto de la celda 0
	#opcion 1, como instancias diferentes
	#print(celda_0.user_x)
	##################################1.2 Calcular distancias a la base
	distancias_celda_cero=celda_0.distancias #obtengo las distancias de esa celda
	print("dist:",distancias_celda_cero)
	distancias_km=distancias_celda_cero/1000 #esta en km.
	print(distancias_km)
	freq=2.4 #asigno frecuencia en gigaz
	#print("Asumiendo que las distancias son en [km] las siguientes: ")
	#print(distancias_celda_cero) #asumiendo que la distancia esta en km
	modelo_prueba=moca.Modelo_Canal(freq, distancias_km) #creo el modelo_prueba del canal
	#print("las perdidas de esas distancias son: ")
	modelo_prueba.perdidas_espacio_libre_ghz() #calculo las perdidas en dB
	print(modelo_prueba.path_loss, "[dB]")
	#############################################1.3 Recibir parámetros
	ptx=18 #[dBm]
	cable_conector_tx=5 #[dB]
	cable_conector_rx=5 #[dB]
	ganancia_tx=5 #dBi
	ganancia_rx=8 #dBi
	sensibilidad=92 #dBm
	modelo_perdidas_simple=modelo_prueba.path_loss
	###########################################1.4 Calcular balance del enlace
	ecuacion_balance=ptx-cable_conector_tx+ganancia_tx-modelo_perdidas_simple+ganancia_rx-cable_conector_rx
	print("potencia irradiada: ", ecuacion_balance)
	print("margen: ",ecuacion_balance+sensibilidad)
	#mono_celda.ver_celdas()
	#mono_celda.ver_usuarios()


	#0.implementar para celdas>1, con los mismos usuarios. Ok para celda=2. Probar para c=n {con sus propios uusarios}
	#1. empaquetar el modelo del canal, balancel del enlace. para cumplir lo de arriba.
	#2. embeber el modelo del canal en la clase sistema celular
	#tarea: implementar grafica para el caso de no cumplir sensibilidad
	#3. crear modulos awgn y ruido


	#PRUEBA DE BALANCE EXITOSA PARA celda=1, celda=2.
	mono_celda.ver_todo()
	plt.grid(True)
	plt.show()


def prueba_top_2_balance_del_enlace():
	'''Prueba para validar un balance del enlace simple (no 5G)

	1.DESIGN:
	#0.implementar para celdas>1, con los mismos usuarios. Ok para celda=2. Probar para c=n {con sus propios uusarios}
	#1. empaquetar el modelo del canal, balancel del enlace. para cumplir lo de arriba.
	#2. embeber el modelo del canal en la clase sistema celular
	#tarea: implementar grafica para el caso de no cumplir sensibilidad
	#3. crear modulos awgn y ruido
	'''
	#IMPLEMENTACION:
	celdas=2
	radio=1000#unidades->m ATENCION: EL RADIO DEFINE LAS UNIDADES, SI SON EN M O EN KM, LOS CALCULOS TAMBIEN.
	#requerimiento 1 usuarios-OK
	#requerimiento n usuarios (lista)-OK
	####################################1.1 Generar escenario (celdas->1, usuarios->1)
	distribucion=((np.array([[1000, 250]]),np.array([[0, 250]])),"prueba_unitaria")
	distribucion=((np.array([[1000, 250],[1500, 1000]]),np.array([[0, 250],[500, 1500]])),"prueba_unitaria") #celdas=2
	mod_perdidas="espacio_libre" #espacio_libre, rappaport, ci, ts901. TUPLA: (tipo, perdidas_tx, perdidas_rx, ganancia_rx,ganancia_tx, sensibilidad)

	pot_tx=0
	loss_tx=0
	loss_rx=0
	gan_tx=0
	gan_rx=0
	sensibilidad=0
	#TODOS LOS EQUIPOS TIENEN LA MISMA LOSS TX, GAN TX, ETC?
	#ES NECESARIO CREAR LOS USUARIOS Y LA ANTENA, con los parametros de arriba

	mod_perdidas=("espacio_libre", pot_tx,loss_tx,loss_rx,gan_tx,gan_rx,sensibilidad)
	'''IMPORTANTE: al incluir el modelo desde aca, puedo tener 2 tier o layer de Celdas
	#un modelo de celdas para umi y otro para uma de forma independiente, ahora como se relacionan?'''
	mono_celda=ss.Sistema_Celular(celdas,radio, distribucion, mod_perdidas)
	celda_0=mono_celda.cluster[0] #objeto de la celda 0
	#opcion 1, como instancias diferentes
	#print(celda_0.user_x)
	##################################1.2 Calcular distancias a la base
	distancias_celda_cero=celda_0.distancias #obtengo las distancias de esa celda
	print("dist:",distancias_celda_cero)
	distancias_km=distancias_celda_cero/1000 #esta en km.
	print(distancias_km)
	freq=2.4 #asigno frecuencia en gigaz
	#print("Asumiendo que las distancias son en [km] las siguientes: ")
	#print(distancias_celda_cero) #asumiendo que la distancia esta en km
	modelo_prueba=moca.Modelo_Canal(freq, distancias_km) #creo el modelo_prueba del canal
	#print("las perdidas de esas distancias son: ")
	modelo_prueba.perdidas_espacio_libre_ghz() #calculo las perdidas en dB
	print(modelo_prueba.path_loss, "[dB]")
	#############################################1.3 Recibir parámetros
	ptx=18 #[dBm]
	cable_conector_tx=5 #[dB]
	cable_conector_rx=5 #[dB]
	ganancia_tx=5 #dBi
	ganancia_rx=8 #dBi
	sensibilidad=92 #dBm
	modelo_perdidas_simple=modelo_prueba.path_loss
	###########################################1.4 Calcular balance del enlace
	ecuacion_balance=ptx-cable_conector_tx+ganancia_tx-modelo_perdidas_simple+ganancia_rx-cable_conector_rx
	print("potencia irradiada: ", ecuacion_balance)
	print("margen: ",ecuacion_balance+sensibilidad)
	#mono_celda.ver_celdas()
	#mono_celda.ver_usuarios()





	#PRUEBA DE BALANCE EXITOSA PARA celda=1, celda=2.
	mono_celda.ver_todo()
	plt.grid(True)
	plt.show()



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
	#1
	#prueba_externa_0()
	#2
	prueba_top_1_balance_del_enlace()

	#prueba_perdidas_basicas()

else:
	print("Modulo Importado: [", os.path.basename(__file__), "]")
