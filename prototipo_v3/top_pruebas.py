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
	'''Prueba para validar un balance del enlace simple (no 5G), al comparar esta prueba y la implementacion.

	1.DESIGN:
	#0.implementar para celdas>1, con los mismos usuarios. Ok para celda=2. Probar para c=n {con sus propios uusarios}
	#1. empaquetar el modelo del canal, balancel del enlace. para cumplir lo de arriba.
	#2. embeber el modelo del canal en la clase sistema celular
	#tarea: implementar grafica para el caso de no cumplir sensibilidad
	#3. crear modulos awgn y ruido
	'''
	print("============INICIO DE LA PRUEBA ==========")
	#IMPLEMENTACION:
	celdas=2
	radio=1000#unidades->m ATENCION: EL RADIO DEFINE LAS UNIDADES, SI SON EN M O EN KM, LOS CALCULOS TAMBIEN.
	#requerimiento 1 usuarios-OK
	#requerimiento n usuarios (lista)-OK
	####################################1.1 Generar escenario (celdas->1, usuarios->1)
	distribucion=((np.array([[1000, 250]]),np.array([[0, 250]])),"prueba_unitaria")
	distribucion=((np.array([[1000, 250],[1500, 1000]]),np.array([[0, 250],[500, 1500]])),"prueba_unitaria") #celdas=2
	mod_perdidas="espacio_libre" #espacio_libre, rappaport, ci, ts901. TUPLA: (tipo, perdidas_tx, perdidas_rx, ganancia_rx,ganancia_tx, sensibilidad)

	pot_tx=18
	loss_tx=5
	loss_rx=5
	gan_tx=5
	gan_rx=8
	sensibilidad=92

	freq=2.4 #asigno frecuencia en gigaz
	#TODOS LOS EQUIPOS TIENEN LA MISMA LOSS TX, GAN TX, ETC?
	#ES NECESARIO CREAR LOS USUARIOS Y LA ANTENA, con los parametros de arriba
	#Considerar lo siguiente: si tenemos dos layers, cada uno tendria un modelo de canal asociado.
	#pero si tienen un modelo de canal diferente, como usarian los mismos usuarios?
	#en realidad si habria un modelo del canal diferente?
	#cual es el criterio de las dos layers?

	param_perdidas=("espacio_libre", pot_tx,loss_tx, gan_tx, gan_rx, loss_rx,sensibilidad)
	'''IMPORTANTE: al incluir el modelo desde aca, puedo tener 2 tier o layer de Celdas
	#un modelo de celdas para umi y otro para uma de forma independiente, ahora como se relacionan?'''

	colmena=ss.Sistema_Celular((celdas,freq),radio, distribucion, param_perdidas)

	celda_0=colmena.cluster[0] #objeto de la celda 0
	celda_1=colmena.cluster[1]

	#opcion 1, como instancias diferentes
	#print(celda_0.user_x)
	##################################1.2 Calcular distancias a la base
	distancias_celda_cero=celda_0.distancias #obtengo las distancias de esa celda
	#print("++++++++++++distancias celda 0:",distancias_celda_cero)

	distancias_celda_uno=celda_1.distancias #obtengo las distancias de esa celda
	#print("++++++++++++distancias celda 1:",distancias_celda_uno)
	########################################print("************usarios en el sistema: ", colmena.no_usuarios_total)
	#print("************distancias en el sistema: ")
	############################################print(colmena.distancias_celdas)
	###############################3distancias_km=distancias_celda_cero/1000 #esta en km.
	#######################3print("&&&&&&&&&&&&distancias en km")
	#####################print(distancias_km)

	#print("Asumiendo que las distancias son en [km] las siguientes: ")
	#print(distancias_celda_cero) #asumiendo que la distancia esta en km
	modelo_prueba=moca.Modelo_Canal(param_perdidas,freq, (colmena.distancias_celdas, "m")) #creo el modelo_prueba del canal
	#print("las perdidas de esas distancias son: ")
	modelo_prueba.perdidas_espacio_libre_ghz() #calculo las perdidas en dB
	print("================top_pruebas==============")
	print("modelo perdidas")
	print(modelo_prueba.path_loss, "perdidas en [dB]")
	modelo_perdidas_simple=modelo_prueba.path_loss #asigno a una variable
	#############################################1.3 Recibir parámetros
	ptx=18 #[dBm]
	cable_conector_tx=5 #[dB]
	cable_conector_rx=5 #[dB]
	ganancia_tx=5 #dBi
	ganancia_rx=8 #dBi
	sensibilidad=92 #dBm

	###########################################1.4 Calcular balance del enlace
	segmento1=ptx-cable_conector_tx+ganancia_tx
	segmento2=ganancia_rx-cable_conector_rx
	print("segmentos", segmento1, segmento2)
	####print("modelo perdidas",modelo_perdidas_simple)
	print("type mod per simple", type(modelo_perdidas_simple))
	ecuacion_balance=ptx-cable_conector_tx+ganancia_tx-modelo_perdidas_simple+ganancia_rx-cable_conector_rx
	print("potencia irradiada: ", ecuacion_balance)
	print("type prx", type(ecuacion_balance))
	print("margen: ",ecuacion_balance+sensibilidad)

	#print("ptx",ptx)
	#print("ltx",cable_conector_tx)
	#print("gtx",ganancia_tx)
	#print("grx",ganancia_rx)
	#print("lrx",cable_conector_rx)
	#colmena.ver_celdas()
	#colmena.ver_usuarios()
	#PRUEBA DE BALANCE EXITOSA PARA celda=1, celda=2.
	colmena.ver_todo()
	plt.grid(True)
	plt.show()

def prueba_top_3_balance_del_enlace():
	'''Prueba limpia para observar la nueva implementacion de la clase modelo del canal
	La prueba consiste en generar un escenario probado sin acudir a la clase modelo del canal como se hizo
	en la prueba top2.'''
	print("============INICIO DE LA PRUEBA P3 ==========")
	celdas=2
	radio=1000
	#parametros de param_escenario
	pot_tx=18
	loss_tx=5
	loss_rx=5
	gan_tx=5
	gan_rx=8
	sensibilidad=92
	freq=2.4
	#empaquetado de variables de escenario
	param_perdidas=("espacio_libre", pot_tx,loss_tx, gan_tx, gan_rx, loss_rx,sensibilidad)
	#definicion de las coordenadas de usuario
	distribucion=((np.array([[1000, 250],[1500, 1000]]),np.array([[0, 250],[500, 1500]])),"prueba_unitaria") #celdas=2
	#simulacion del escenario al crear un sistema celular
	sim_colmena=ss.Sistema_Celular((celdas,freq),radio, distribucion, param_perdidas)
	print(sim_colmena.modelo_canal.resultado_balance)
	print(sim_colmena.modelo_canal.resultado_margen)

	sim_colmena.ver_todo()
	plt.grid(True)
	plt.show()

def prueba_top_4_balance_del_enlace():
	'''Prueba limpia para observar la nueva implementacion de la clase modelo del canal
	La prueba consiste en generar un escenario probado sin acudir a la clase modelo del canal como se hizo
	en la prueba top2.'''
	print("============INICIO DE LA PRUEBA P3 ==========")
	celdas=5
	radio=1000
	#parametros de param_escenario
	pot_tx=18
	loss_tx=5
	loss_rx=5
	gan_tx=5
	gan_rx=8
	sensibilidad=92
	freq=2.4
	#empaquetado de variables de escenario
	param_perdidas=("espacio_libre", pot_tx,loss_tx, gan_tx, gan_rx, loss_rx,sensibilidad)
	#definicion de las coordenadas de usuario
	intensidad = 2
	distribucion=(intensidad/radio**2,"ppp")
	#simulacion del escenario al crear un sistema celular
	sim_colmena=ss.Sistema_Celular((celdas,freq),radio, distribucion, param_perdidas)
	print("POTENCIA RECIBIDA")
	print(sim_colmena.modelo_canal.resultado_balance)
	print("MARGEN")
	print(sim_colmena.modelo_canal.resultado_margen)

	#sim_colmena.ver_usuarios()
	#sim_colmena.ver_celdas()
	sim_colmena.ver_todo()
	plt.grid(True)
	plt.show()

def prueba_top_5_balance_del_enlace():
	'''Prueba limpia para observar la nueva implementacion de la clase modelo del canal
	La prueba consiste en generar un escenario probado sin acudir a la clase modelo del canal como se hizo
	en la prueba top2.'''
	print("============INICIO DE LA PRUEBA P3 ==========")
	celdas=4
	radio=1000 #km
	#parametros de param_escenario
	pot_tx=18
	loss_tx=5
	loss_rx=5
	gan_tx=5
	gan_rx=8
	sensibilidad=92
	freq=1500 #megaherz
	#empaquetado de variables de escenario. Debe seguir la norma Kwars
	param_perdidas=("okumura_hata", pot_tx,loss_tx, gan_tx, gan_rx, loss_rx,sensibilidad)
	#definicion de las coordenadas de usuario
	intensidad = 1
	distribucion=(intensidad/radio**2,"ppp")
	#simulacion del escenario al crear un sistema celular
	sim_colmena=ss.Sistema_Celular((celdas,freq),radio, distribucion, param_perdidas)
	print("MODELO DE PERDIDAS")
	print(sim_colmena.modelo_canal.resultado_path_loss)
	print("POTENCIA RECIBIDA")
	print(sim_colmena.modelo_canal.resultado_balance)
	print("MARGEN")
	print(sim_colmena.modelo_canal.resultado_margen)

	#sim_colmena.ver_usuarios()
	#sim_colmena.ver_celdas()
	sim_colmena.ver_todo()
	plt.grid(True)
	plt.show()


def prueba_sistema_v035():
	'''Prueba para implemenetar el requerimiento 5a1 del reporte version 39. Parte 1'''
	print("============INICIO DE LA PRUEBA requerimiento 5a1 ==========")
	celdas=19
	intensidad = 1
	#
	radio=1000 #km
	#parametros de param_escenario
	pot_tx=18
	loss_tx=5
	loss_rx=5
	gan_tx=5
	gan_rx=8
	sensibilidad=92
	freq=1500 #megaherz
	#empaquetado de variables de escenario. Debe seguir la norma Kwars
	param_perdidas=("okumura_hata", pot_tx,loss_tx, gan_tx, gan_rx, loss_rx,sensibilidad)
	#definicion de las coordenadas de usuario
	#
	distribucion=(intensidad/radio**2,"ppp")
	#simulacion del escenario al crear un sistema celular
	sim_colmena=ss.Sistema_Celular((celdas,freq),radio, distribucion, param_perdidas)
	print("[top] 1. El cluster tiene ahora,", len(sim_colmena.cluster), "celdas.")
	print("[top] 2. Tipo de dato  ",type(sim_colmena.ue_x)) #muestra la estructura de los datos.
	print("[top] 3. Logitud dato celda[0]-usuarios/celda: ",len(sim_colmena.ue_x[0]), " usuarios.")
	print("[top] 5. Total usuarios",sim_colmena.no_usuarios_total)
	#print("[top] 4. Estructura de celdas\n",sim_colmena.ue_x)
	print("[top] 6. distancia all usuarios c0",sim_colmena.cluster[0].interf_distancias)
	print("[top] 7. origen celda",sim_colmena.cluster[0].pos_x, sim_colmena.cluster[0].pos_y)

	'''Cada celda del cluster, ya contiene la distancia de los usuarios a las demas celdas.'''
	#En este caso se ha seleccionado la celda celda_0 para conocer las distancias asociadas de sus usuarios.
	stack_test=np.stack(sim_colmena.cluster[0].interf_distancias, axis=0)

	print("[top] 8. stak all usuarios c0",stack_test.shape)
	transpose_test=np.transpose(stack_test) #consituye las distancias de los usuarios a todas las celdas
	print("[top] 9. traspose all usuarios c0",transpose_test[0])
	print("[top] 10. maximo python c0",max(transpose_test[0]))
	print("[top] 11. minimo python c0",min(transpose_test[0]))
	print("[top] 12. maximo numpy c0",np.amax(transpose_test[0]))
	print("[top] 13. minimo numpy c0",np.amin(transpose_test[0]))
	print("[top] 14. cell id maximo numpy c0",np.where(transpose_test[0]==np.amax(transpose_test[0])))
	print("[top] 15. cell id minimo numpy c0",np.where(transpose_test[0]==np.amin(transpose_test[0])))
	#print("[top] 10. stak all usuarios c0",stack_test.shape)


	'''Diseno de implementacion
	1. Con las coordenadas de los usuarios, SIN asignarlos a una celda, calcular:
		a. distancia a la celda(s)-> n(input) celdas.
			a1. caso 1: todas las celdas
			values.index(max(values))
			a2. caso 2: celdas cercanas
		b. perdidas del modelo de propagacion correspondiente
		c. potencia recibida
	2. 	Con la potencia recibida asignar a usuario.







	'''
	sim_colmena.ver_todo()
	plt.grid(True)
	plt.show()


def prueba_sistema_v036():
	'''Prueba para implemenetar el feature de visualizacion de radios circulares.'''
	print("============INICIO DE LA PRUEBA==========")
	celdas=5
	intensidad = 1
	#
	radio=1000 #km
	#parametros de param_escenario
	pot_tx=18
	loss_tx=5
	loss_rx=5
	gan_tx=5
	gan_rx=8
	sensibilidad=92
	freq=1500 #megaherz
	#empaquetado de variables de escenario. Debe seguir la norma Kwars
	param_perdidas=("okumura_hata", pot_tx,loss_tx, gan_tx, gan_rx, loss_rx,sensibilidad)
	#definicion de las coordenadas de usuario
	#
	distribucion=(intensidad/radio**2,"ppp")
	#simulacion del escenario al crear un sistema celular
	sim_colmena=ss.Sistema_Celular((celdas,freq),radio, distribucion, param_perdidas)
	sim_colmena.ver_circulos()
	sim_colmena.ver_todo()
	plt.grid(True)
	plt.show()
	'''Prueba terminada'''

def prueba_sistema_v037():
	'''Prueba para implemenetar el feature de visualizacion usuarios por celda, en diferente color.'''
	print("============INICIO DE LA PRUEBA==========")
	celdas=19
	intensidad = 1
	#
	radio=1000 #km
	#parametros de param_escenario
	pot_tx=18
	loss_tx=5
	loss_rx=5
	gan_tx=5
	gan_rx=8
	sensibilidad=92
	freq=1500 #megaherz
	#empaquetado de variables de escenario. Debe seguir la norma Kwars
	param_perdidas=("okumura_hata", pot_tx,loss_tx, gan_tx, gan_rx, loss_rx,sensibilidad)
	#definicion de las coordenadas de usuario
	#
	distribucion=(intensidad/radio**2,"ppp")
	#simulacion del escenario al crear un sistema celular
	sim_colmena=ss.Sistema_Celular((celdas,freq),radio, distribucion, param_perdidas)
	sim_colmena.ver_circulos()
	sim_colmena.ver_celdas()
	sim_colmena.ver_estaciones_base()
	sim_colmena.ver_usuarios_colores()
	sim_colmena.ver_usuarios()
	#sim_colmena.ver_todo()
	plt.grid(True)
	plt.show()


def prueba_sistema_v038():
	'''Prueba para implemenetar el requerimiento 5a1 del reporte version 39. Parte 2'''
	print("============INICIO DE LA PRUEBA==========")
	celdas=19
	intensidad = 1
	#
	radio=1000 #km
	#parametros de param_escenario
	pot_tx=18
	loss_tx=5
	loss_rx=5
	gan_tx=5
	gan_rx=8
	sensibilidad=92
	freq=1500 #megaherz
	#empaquetado de variables de escenario. Debe seguir la norma Kwars
	param_perdidas=("okumura_hata", pot_tx,loss_tx, gan_tx, gan_rx, loss_rx,sensibilidad)
	#definicion de las coordenadas de usuario
	#
	distribucion=(intensidad/radio**2,"ppp")
	#simulacion del escenario al crear un sistema celular
	sim_colmena=ss.Sistema_Celular((celdas,freq),radio, distribucion, param_perdidas)
	print("HIPER CLUSTER")
	print(type(sim_colmena.distancias_hiper_cluster))
	stack_test=np.stack(sim_colmena.distancias_hiper_cluster, axis=0)
	print("stack original", stack_test)
	print("-------------------------------------------------")
	#print("stack original", stack_test*10)
	newarr = stack_test.reshape(celdas, celdas, -1)
	print(newarr.shape) #indica que no se puede organizar de otro modo, que no sea stack.
	print("--------------------------------------------------")
	print("stack2[0]", stack_test[0])
	print("stack3[0][0]", stack_test[0][0])
	print("[top] 3. Logitud dato celda[0]-usuarios/celda: ",len(sim_colmena.ue_x[0]), " usuarios.")
	print("[top] 5. Total usuarios",sim_colmena.no_usuarios_total)
	print("[top] 6'. Forma",stack_test.shape)
	print("--------------------------------------------test")
	print("stack4 celda0", stack_test[0][0])
	print("stack5 celda0", stack_test[1][0])
	print("stack6 celda0", stack_test[2][0])
	#significancia:
	# stack_test[i][j], con i: distancias de la i celda,
	#						j: usuarios de la j celda donde se originaron los usuarios propios.
	#
	#Mismos usuarios, desde la celda 1,2,3
	#los usuarios pertenencen a la celda 0 originalmente.
	print("\nstack41 celda1", stack_test[0][1])
	print("stack51 celda1", stack_test[1][1])
	print("stack61 celda1", stack_test[2][1])
	#
	print("\nstack42 celda2", stack_test[0][2])
	print("stack52 celda2", stack_test[1][2])
	print("stack62 celda3", stack_test[2][2])

	print("\nlen usuarios",len(sim_colmena.distancias_hiper_cluster[0][0]))
	print("\nlen1 celdas",len(np.array(sim_colmena.distancias_hiper_cluster)))
	print("**************************")
	print("MODELO DE PERDIDAS")
	print(sim_colmena.hiperc_modelo_canal.resultado_path_loss)
	print("POTENCIA RECIBIDA")
	print(sim_colmena.hiperc_modelo_canal.resultado_balance)
	print("MARGEN")
	print(sim_colmena.hiperc_modelo_canal.resultado_margen)
	'''for test in stack_test:
		print(test)
		print("--")
	for test in np.array(sim_colmena.distancias_hiper_cluster):
		print(test)
		print("*")

	print("...")
	#usuarios
	for cel in range(celdas):
		#celdas.
		for usrs in range(len(sim_colmena.ue_x[0])):
			print(usrs,cel)
			print("\n output", stack_test[usrs][cel])
			#print(stack_test[i][j])
			#print("\n")

	'''



	sim_colmena.ver_circulos()
	sim_colmena.ver_celdas()
	sim_colmena.ver_estaciones_base()
	sim_colmena.ver_usuarios_colores()
	sim_colmena.ver_usuarios()
	#sim_colmena.ver_todo()
	plt.grid(True)
	plt.show()
	#prueba exitosa!

def prueba_sistema_v039():
	'''Prueba para implemenetar el requerimiento 1e del reporte version 39. Parte 2.1: angulos'''
	print("============INICIO DE LA PRUEBA==========")
	'''Diseño
	1.Definir una funcion que recibe una lista, y calcula el angulo que forma respecto al punto 0.0.
		y contra las manecillas del reloj. Listo
	1.2.Definir una funcion que recibe una lista, y calcula el angulo que forma respecto al punto indicado. Ok
	1.3 Definir una funcion que recibe un array numpy, y calcula el angulo que forma respecto al punto indicado. OK

	2. Para cada angulo en el arrary 1.3, calcular la ganancia que debe recibir con 1 lobulo.
	2.2 Para cada angulo en el arrary 1.3, calcular la ganancia que debe recibir cuando existen 3 lobulos.
	2.3 Para cada angulo en el arrary 1.3, calcular la ganancia que debe recibir cuando existen n lobulos.
	ref:https://stackoverflow.com/questions/31735499/calculate-angle-clockwise-between-two-points
	'''
	celdas=2
	intensidad = 0.5
	#
	radio=1000 #km
	#parametros de param_escenario
	pot_tx=18
	loss_tx=5
	loss_rx=5
	gan_tx=5
	gan_rx=8
	sensibilidad=92
	freq=1500 #megaherz
	#empaquetado de variables de escenario. Debe seguir la norma Kwars
	param_perdidas=["okumura_hata", pot_tx,loss_tx, gan_tx, gan_rx, loss_rx,sensibilidad]
	#definicion de las coordenadas de usuario
	#
	distribucion=(intensidad/radio**2,"ppp")
	#simulacion del escenario al crear un sistema celular
	sim_colmena=ss.Sistema_Celular((celdas,freq),radio, distribucion, param_perdidas)
	print("------------------------")
	print("coordenadas de usuarios")
	print(sim_colmena.ue_x)
	print(sim_colmena.ue_y)
	print("------------------------")
	print("angulos hiper cluster grados -180,180")
	print(np.stack(sim_colmena.angulos_hiper_cluster))
	print("------------------------")
	print("angulos hiper cluster grados 360")
	theta=np.stack(sim_colmena.angulos_hiper_cluster)
	theta=np.where(theta<0, 360+theta, theta)
	print(theta)

	sim_colmena.ver_celdas()
	sim_colmena.ver_circulos()
	sim_colmena.ver_estaciones_base()
	sim_colmena.ver_usuarios_colores()
	sim_colmena.ver_usuarios()
	sim_colmena.ver_todo()
	plt.grid(True)
	plt.show()

def prueba_sistema_v040():
	'''Prueba para implemenetar el requerimiento 1e del reporte version 39. Parte 2: ganancia relativa'''
	n_cel=3
	radio_cel=1000
	frecuencia=(1500,'mhz')
	intensidad=1/radio_cel**2
	distribucion=('ppp', intensidad)

	params_simulacion=[n_cel,radio_cel, distribucion, frecuencia]
	#propagacion='okumura_hata' #si no: se pone, se escribe o se escribe bien, el pathloss es 0
	hb=30 #m
	alfa=0
	hm=1.5
	params_prop=[hb, alfa, hm]
	propagacion=['okumura_hata', params_prop]
	pot_tx=18
	loss_tx=5
	gan_tx=5
	gan_rx=8
	loss_rx=0
	sensibilidad=92
	params_perdidas=[propagacion, pot_tx,loss_tx, gan_tx, gan_rx, loss_rx,sensibilidad]
	#
	hpbw=55
	amin=20
	ref="4g"
	gtx=params_perdidas[3]
	#apunt=mc.calcular_angulo_v3(45,120) #inicio,angulo de particion.
	#tar=np.array([45, 90, 180, -1, -179])
	params_transmision=[ref, hpbw, gtx, amin] #se adjunta luego: apunt, tar
	#
	params_recepcion=[0]

	#INICIO DE LA SIMULACION
	sim_colmena=ss.Sistema_Celular(params_simulacion, params_transmision, params_perdidas)
	print("[top]. Total usuarios",sim_colmena.no_usuarios_total)
	print("**************************")
	print("[top]. MODELO DE PERDIDAS\n")
	print(sim_colmena.hiperc_modelo_canal.resultado_path_loss)
	print("[top]. POTENCIA RECIBIDA\n")
	print(sim_colmena.hiperc_modelo_canal.resultado_balance)
	print("[top]. MARGEN **revisar ecuacion\n")
	print(sim_colmena.hiperc_modelo_canal.resultado_margen)

	plt.title("Escenario: "+propagacion[0])
	sim_colmena.ver_celdas()
	sim_colmena.ver_circulos()
	sim_colmena.ver_estaciones_base()
	sim_colmena.ver_usuarios_colores()
	sim_colmena.ver_usuarios()
	sim_colmena.ver_todo()
	#
	sim_colmena.hiperc_antena.observar_patron()
	plt.grid(True)
	plt.show()


def prueba_sistema_v041():
	'''Prueba para implemenetar el requerimiento 1e del reporte version 39. Parte 3: desvanecimiento'''
	n_cel=3
	radio_cel=1000 #DEFINICION, SIEMPRE EN METROS. La distancia tambien es en metros.
	frecuencia=(1500,'mhz')
	intensidad=1/radio_cel**2
	distribucion=('ppp', intensidad)

	params_simulacion=[n_cel,radio_cel, distribucion, frecuencia]
	#propagacion='okumura_hata' #si no: se pone, se escribe o se escribe bien, el pathloss es 0
	hb=30 #m
	alfa=0
	hm=1.5
	params_prop=[hb, alfa, hm]
	#
	#params desv
	tipo_desv='lento'
	alpha_n=3.1
	sigma_xn=8.1
	mu=0
	play_desv=True
	#el tercer valor va en el mismo orden, dependiendo del desvanecimiento
	params_desv=[tipo_desv, play_desv, [alpha_n, sigma_xn, mu]]
	#
	propagacion=['okumura_hata', params_prop, params_desv]
	pot_tx=18
	loss_tx=5
	gan_tx=5
	gan_rx=8
	loss_rx=0
	sensibilidad=92
	params_perdidas=[propagacion, pot_tx,loss_tx, gan_tx, gan_rx, loss_rx,sensibilidad]
	#
	hpbw=55
	amin=20
	ref="4g"
	gtx=params_perdidas[3]
	#apunt=mc.calcular_angulo_v3(45,120) #inicio,angulo de particion.
	#tar=np.array([45, 90, 180, -1, -179])
	params_transmision=[ref, hpbw, gtx, amin] #se adjunta luego: apunt, tar
	#
	params_recepcion=[0]

	#INICIO DE LA SIMULACION
	sim_colmena=ss.Sistema_Celular(params_simulacion, params_transmision, params_perdidas)
	print("[top]. Total usuarios",sim_colmena.no_usuarios_total)
	print("**************************")
	print("[top]. MODELO DE PERDIDAS -ANTES")
	print(sim_colmena.hiperc_modelo_canal.resultado_path_loss_antes)
	print("\n[top]. MODELO DE PERDIDAS")
	print(sim_colmena.hiperc_modelo_canal.resultado_path_loss)
	print("\n[top]. POTENCIA RECIBIDA")
	print(sim_colmena.hiperc_modelo_canal.resultado_balance)
	print("\n[top]. MARGEN **revisar ecuacion")
	print(sim_colmena.hiperc_modelo_canal.resultado_margen)

	plt.title("Escenario: "+propagacion[0])
	sim_colmena.ver_celdas()
	sim_colmena.ver_circulos()
	sim_colmena.ver_estaciones_base()
	sim_colmena.ver_usuarios_colores()
	sim_colmena.ver_usuarios()
	sim_colmena.ver_todo()
	#
	###################sim_colmena.hiperc_antena.observar_patron()
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
	#prueba_top_1_balance_del_enlace()
	#prueba_top_2_balance_del_enlace()
	#prueba_top_3_balance_del_enlace()
	#prueba_top_5_balance_del_enlace()
	#prueba_perdidas_basicas()
	#prueba_sistema_v035()
	#prueba_sistema_v036()
	#prueba_sistema_v037()
	#prueba_sistema_v038()
	#prueba_sistema_v039()
	#prueba_sistema_v040()
	prueba_sistema_v041()


else:
	print("Modulo Importado: [", os.path.basename(__file__), "]")

'''Requerimientos:

1. [ok] Si cada modelo de propagacion tiene sus propias variables, como las recibo? ->parametros de entrada del modelo,
	reciben el nombre del modelo y sus parametros. Cada funcino interna del modelo del canal, selecciona
	sus parametros internos de acuerdo a un orden establecido.
2. [ok] Seleccionar el modelo de canal segun las unidades de freccuencia y distancia.
O, convertir todo a una misma unidad para efectos de uso. -> funcion modelocanal.inicializar_tipo()

3. Supongamos que tenemos n realizaciones de instancias de la clase Sistema_Celular. Cada instancia tiene
diferentes longitudes de usuarios, por ser el resutlado de un numero poisson.
Luego, como realizar una comparacion entre simulaciones?. Que es lo que se compara en cobertura?
	a. idea 1: la probabilidad de outage es un valor unico en cada simulacion, puede compararse.
		1.1 debe ser un kpi comparable, que sea unico a pesar de los diferentes usuarios.

4. [OK] La funcion normal especifica un numero de puntos asociados, pero si estos no son especificados?
Por ejemplo, tengo un array numpy y deseo operar sobre ellos, como deberia operar? ->solucionado,np.random.normal, funciona con np.shape.

5. [OK] Deseo como parametro de entrada, especificar si quiero incorporar el desvanecimiento o no. ->

6. Modelo del canal debe especificar cuando se hace el balance del enlace, no la clase sistema.
7. Revisar ecuacion del balance
8. Implmentar balance del enlace, mcl. mcl debe ser un parametro de entrada?->no. Revisar las condiciones urbano.
9. Implementar clase usuario, crear view interactiva y obtener informacion, dada las coordendas.


'''
