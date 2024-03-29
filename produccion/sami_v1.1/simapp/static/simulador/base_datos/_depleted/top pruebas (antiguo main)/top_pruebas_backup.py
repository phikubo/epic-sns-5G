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



def parametros_de_prueba():
	'''Parametros centralizados'''
	debug=False #[6]
	n_cel=15
	resolucion=3
	radio_cel=500 #DEFINICION, SIEMPRE EN METROS. La distancia tambien es en metros.
	frecuencia=(700,'mhz')
	bw=20 #'mhz') #1.4, 3, 5, 10, 15, 20, ..., 50, 100, 200, 400
	intensidad=40/radio_cel**2
	fr=6 #dB
	print("INTENSIDAD DE ENTRADA: ",intensidad)
	if n_cel>7:
		mul=4.6
	else:
		mul=3
	x_prueba=np.arange(-mul*radio_cel,mul*radio_cel,resolucion) #depende del radio_cel y numero de celdas.
	y_prueba=np.arange(-mul*radio_cel,mul*radio_cel,resolucion)
	xx,yy=np.meshgrid(x_prueba,y_prueba)
	mapa_calor=(False, (xx,yy))
	distribucion=('ppp', intensidad, mapa_calor)
	#verificar mcl
	#x_prueba=np.array([[1000, 0, 1000, 0],[1500, 1000, 1000, 1500]])
	#y_prueba=np.array([[0,	 10, 550, 580],[500, 1500, 1000, 1750]])
	#distribucion=("prueba_unitaria",(np.array([[1000, 250],[1500, 1000]]),np.array([[0, 250],[500, 1500]]))) #celdas=2
	#distribucion=("prueba_unitaria",(x_prueba,y_prueba) ) #celdas=2

	params_simulacion=[n_cel,radio_cel, distribucion, frecuencia, bw, fr, debug]
	#propagacion='okumura_hata' #si no: se pone, se escribe o se escribe bien, el pathloss es 0
	hb=30 #m
	alfa=0
	hm=1.5
	params_prop=[hb, alfa, hm]
	#
	#params desv
	tipo_desv='normal'
	alpha_n=3.1
	sigma_xn=8.1
	mu=0
	play_desv=True


	#el tercer valor va en el mismo orden, dependiendo del desvanecimiento
	params_desv=[tipo_desv, play_desv, [alpha_n, sigma_xn, mu]]
	#
	propagacion=['okumura_hata', params_prop, params_desv]
	pot_tx=19 #dBm
	loss_tx=5
	gan_tx=15#
	gan_rx=8
	loss_rx=0
	sensibilidad=-92
	params_perdidas=[propagacion, pot_tx,loss_tx, gan_tx, gan_rx, loss_rx,sensibilidad]
	#
	hpbw=65
	amin=20
	ref="4g"
	gtx=params_perdidas[3]
	#apunt=mc.calcular_angulo_v3(45,120) #inicio,angulo de particion.
	#tar=np.array([45, 90, 180, -1, -179])
	params_transmision=[ref, hpbw, gtx, amin] #se adjunta luego: apunt, tar
	#
	params_recepcion=[0]
	'''Requerimiento:
	Dados unos parametros fijos, siendo la distribucion cualquiera (menos la malla_rectangular),
	segun una bandera, puedo simular tanto los usuarios aleatorios, como los usuarios de la imagen.
	Pero ambos siguen un flujo de simulacion diferente.
	Si la bandera es verdadera, las dimensiones deben conservarse en todo el proceso.
	'''

	return params_simulacion, params_transmision, params_perdidas

def parametros_de_prueba_unitaria():
	'''Parametros centralizados. La intensidad es un parametro independiente de la prueba
	mapa del calor, pues la intensidad del mapa del calor es basicamente la resolucion o espaciamiento
	entre los puntos.'''
	debug=False #[6]
	resolucion=10
	n_cel=3
	"""Experimento:
	Con 2 celdas.
	Se varia el radio de la celda.
	-2 cel, En 1000 se obtiene aproximadamente 60-63%.
	-3 cel, en 1000,900,800, ... 48+/-3%
	-3 cel, en 600,500,400,300,200 ... 50+/-2%
	-3 cel, en 100, ... 1+-0.5%
	-3 cel, en <100, 0%.
	Conclusion del experimento"""
	radio_cel=1000#DEFINICION, SIEMPRE EN METROS. La distancia tambien es en metros.

	frecuencia=(900,'mhz')
	bw=20 #'mhz') #1.4, 3, 5, 10, 15, 20, ..., 50, 100, 200, 400
	intensidad=1/radio_cel**2
	fr=6 #dB

	if n_cel>7:
		mul=4.6
	else:
		mul=3
	x_prueba=np.arange(-mul*radio_cel,mul*radio_cel,resolucion) #depende del radio_cel y numero de celdas.
	y_prueba=np.arange(-mul*radio_cel,mul*radio_cel,resolucion)
	xx,yy=np.meshgrid(x_prueba,y_prueba)
	mapa_calor=(False, (xx,yy))
	print("[debug.parametros_unitaria]: ", xx.shape)
	print("INTENSIDAD DE ENTRADA: ",intensidad)
	distribucion=('ppp', intensidad, mapa_calor)

	#x_prueba=np.array([[1000, 0, 1000, 0],[1500, 1000, 1000, 1500]])
	#y_prueba=np.array([[0,	 10, 550, 580],[500, 1500, 1000, 1750]])


	#distribucion=("prueba_unitaria",(np.array([[1000, 250],[1500, 1000]]),np.array([[0, 250],[500, 1500]]))) #celdas=2
	#distribucion=("malla_rectangular",(xx,yy) ) #celdas=2

	params_simulacion=[n_cel,radio_cel, distribucion, frecuencia, bw, fr, debug]
	#propagacion='okumura_hata' #si no: se pone, se escribe o se escribe bien, el pathloss es 0
	hb=30 #m
	alfa=0
	hm=1.5
	params_prop=[hb, alfa, hm]
	#
	#params desv
	tipo_desv='normal'
	alpha_n=3.1
	sigma_xn=8.1
	mu=0
	play_desv=False
	#el tercer valor va en el mismo orden, dependiendo del desvanecimiento
	params_desv=[tipo_desv, play_desv, [alpha_n, sigma_xn, mu]]
	#
	propagacion=['okumura_hata', params_prop, params_desv]
	pot_tx=30 #dBm #para un 1w, 10 watts para rural.
	loss_tx=1 #dB
	gan_tx=15#dBi
	gan_rx=8 #dBi
	loss_rx=1 #dB
	sensibilidad=-92 #antes -92 #dBm
	params_perdidas=[propagacion, pot_tx,loss_tx, gan_tx, gan_rx, loss_rx,sensibilidad]
	#
	hpbw=65
	amin=20
	ref="4g"
	gtx=params_perdidas[3]
	#apunt=mc.calcular_angulo_v3(45,120) #inicio,angulo de particion.
	#tar=np.array([45, 90, 180, -1, -179])
	params_transmision=[ref, hpbw, gtx, amin] #se adjunta luego: apunt, tar
	#
	params_recepcion=[0]

	return params_simulacion, params_transmision, params_perdidas


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
	print("[top] 2. Tipo de dato  ",type(sim_colmena.usuario_x)) #muestra la estructura de los datos.
	print("[top] 3. Logitud dato celda[0]-usuarios/celda: ",len(sim_colmena.usuario_x[0]), " usuarios.")
	print("[top] 5. Total usuarios",sim_colmena.no_usuarios_total)
	#print("[top] 4. Estructura de celdas\n",sim_colmena.usuario_x)
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
	print("[top] 3. Logitud dato celda[0]-usuarios/celda: ",len(sim_colmena.usuario_x[0]), " usuarios.")
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
		for usrs in range(len(sim_colmena.usuario_x[0])):
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
	print(sim_colmena.usuario_x)
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
	intensidad=10/radio_cel**2
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
	'''Prueba para implemenetar el requerimiento 1e del reporte version 39. Parte 3: desvanecimiento lento, mcl'''
	n_cel=2
	radio_cel=1000 #DEFINICION, SIEMPRE EN METROS. La distancia tambien es en metros.
	frecuencia=(1500,'mhz')
	intensidad=1/radio_cel**2
	distribucion=('ppp', intensidad)
	#verificar mcl
	distribucion=("prueba_unitaria",(np.array([[1000, 250],[1500, 1000]]),np.array([[0, 250],[500, 1500]]))) #celdas=2
	distribucion=("prueba_unitaria",(np.array([[1000, 0],[1500, 1000]]),np.array([[0, 10],[500, 1500]]))) #celdas=2

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
	play_desv=False
	#el tercer valor va en el mismo orden, dependiendo del desvanecimiento
	params_desv=[tipo_desv, play_desv, [alpha_n, sigma_xn, mu]]
	#
	propagacion=['okumura_hata', params_prop, params_desv]
	pot_tx=18 #dBm
	loss_tx=5
	gan_tx=5
	gan_rx=8
	loss_rx=0
	sensibilidad=-92
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


def prueba_sistema_v042():
	'''Prueba para implemenetar el requerimiento 1e del reporte version 39. Parte 3: desvanecimiento lento, mcl'''
	n_cel=2
	radio_cel=1000 #DEFINICION, SIEMPRE EN METROS. La distancia tambien es en metros.
	frecuencia=(1500,'mhz')
	intensidad=1/radio_cel**2
	distribucion=('ppp', intensidad)
	#verificar mcl
	x_prueba=np.array([[1000, 0, 1000, 0],[1500, 1000, 1000, 1500]])
	y_prueba=np.array([[0,	 10, 550, 580],[500, 1500, 1000, 1750]])
	distribucion=("prueba_unitaria",(np.array([[1000, 250],[1500, 1000]]),np.array([[0, 250],[500, 1500]]))) #celdas=2
	distribucion=("prueba_unitaria",(x_prueba,y_prueba) ) #celdas=2

	params_simulacion=[n_cel,radio_cel, distribucion, frecuencia]
	#propagacion='okumura_hata' #si no: se pone, se escribe o se escribe bien, el pathloss es 0
	hb=30 #m
	alfa=0
	hm=1.5
	params_prop=[hb, alfa, hm]
	#
	#params desv
	tipo_desv='normal'
	alpha_n=3.1
	sigma_xn=8.1
	mu=0
	play_desv=True
	#el tercer valor va en el mismo orden, dependiendo del desvanecimiento
	params_desv=[tipo_desv, play_desv, [alpha_n, sigma_xn, mu]]
	#
	propagacion=['okumura_hata', params_prop, params_desv]
	pot_tx=18 #dBm
	loss_tx=5
	gan_tx=15#
	gan_rx=8
	loss_rx=0
	sensibilidad=-92
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
	print("************")
	print("[top]. Tipo hiper-dato: ",type(sim_colmena.hiperc_ganancia_relativa))
	print("************")
	print("[top]. Forma hiper-dato: ",sim_colmena.hiperc_ganancia_relativa.shape)
	print("**************************")
	print("[top]. GANANCIA")
	print(sim_colmena.hiperc_ganancia_relativa)
	print("[top]. DISTANCIAS")
	print(sim_colmena.hiperc_distancias)
	#print("[top]. MODELO DE PERDIDAS -ANTES")
	#print(sim_colmena.hiperc_modelo_canal.resultado_path_loss_antes) *ELIMINAR ANTES PATLOSS
	print("\n[top]. MODELO DE PERDIDAS + Desva (si aplica)")
	print(sim_colmena.hiperc_modelo_canal.resultado_path_loss) #ya no aplica, ahora aplica en el balance

	print("\n[top]. POTENCIA RECIBIDA, simplificado, sin tx. ")
	print(sim_colmena.hiperc_modelo_canal.balance_simplificado_antes)
	print("\n[top]. POTENCIA RECIBIDA + Desva (si aplica) ")
	print(sim_colmena.hiperc_modelo_canal.resultado_balance)
	print("\n[top]. MARGEN")
	print(sim_colmena.hiperc_modelo_canal.resultado_margen)

	plt.title("Escenario: "+propagacion[0])
	sim_colmena.ver_celdas()
	sim_colmena.ver_circulos()
	sim_colmena.ver_estaciones_base()
	sim_colmena.ver_usuarios_colores()
	sim_colmena.ver_usuarios()
	sim_colmena.ver_todo()
	#
	#sim_colmena.hiperc_antena.observar_patron()
	plt.grid(True)
	plt.show()


def prueba_sistema_v043():
	'''Prueba para implemenetar el requerimiento 1e del reporte version 39. Parte 4: datos por usuario.'''
	n_cel=2
	radio_cel=1000 #DEFINICION, SIEMPRE EN METROS. La distancia tambien es en metros.
	frecuencia=(1500,'mhz')
	intensidad=1/radio_cel**2
	distribucion=('ppp', intensidad)
	#verificar mcl
	#x_prueba=np.array([[1000, 0, 1000, 0],[1500, 1000, 1000, 1500]])
	#y_prueba=np.array([[0,	 10, 550, 580],[500, 1500, 1000, 1750]])
	#distribucion=("prueba_unitaria",(np.array([[1000, 250],[1500, 1000]]),np.array([[0, 250],[500, 1500]]))) #celdas=2
	#distribucion=("prueba_unitaria",(x_prueba,y_prueba) ) #celdas=2

	params_simulacion=[n_cel,radio_cel, distribucion, frecuencia]
	#propagacion='okumura_hata' #si no: se pone, se escribe o se escribe bien, el pathloss es 0
	hb=30 #m
	alfa=0
	hm=1.5
	params_prop=[hb, alfa, hm]
	#
	#params desv
	tipo_desv='normal'
	alpha_n=3.1
	sigma_xn=8.1
	mu=0
	play_desv=True
	#el tercer valor va en el mismo orden, dependiendo del desvanecimiento
	params_desv=[tipo_desv, play_desv, [alpha_n, sigma_xn, mu]]
	#
	propagacion=['okumura_hata', params_prop, params_desv]
	pot_tx=18 #dBm
	loss_tx=5
	gan_tx=15#
	gan_rx=8
	loss_rx=0
	sensibilidad=-92
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
	print("\n**************************")
	print("[top] Por celda: ",len(sim_colmena.usuario_x[0]), " usuarios.")
	print("[top]. Total usuarios",sim_colmena.no_usuarios_total)
	print("************")
	print("[top]. Tipo hiper-dato: ",type(sim_colmena.hiperc_ganancia_relativa))
	print("************")
	print("[top]. Forma hiper-dato: ",sim_colmena.hiperc_ganancia_relativa.shape)
	print("**************************")
	#print("\n[top]. GANANCIA")
	#print(sim_colmena.hiperc_ganancia_relativa)
	print("[top]. DISTANCIAS->", type(sim_colmena.hiperc_distancias))
	print(sim_colmena.hiperc_distancias)
	print("**************************")
	'''
	ind_celda=0
	print("**************************distancias[a]->indice [a] (usuarios creados en celda a) -->CELDA[{}]".format(ind_celda))
	print(sim_colmena.hiperc_distancias[ind_celda])
	print("**************************")
	print("**************************")

	ind_celda_1=1
	print("\n**************************distancias[a][b]->indice [b] (usuarios creados en celda a, distancia usuarios en celda b) -->CELDA[{}][{}]".format(ind_celda,ind_celda_1))
	print(sim_colmena.hiperc_distancias[ind_celda][ind_celda_1])

	print("**************************")
	print("**************************")

	ind_us=0
	print("\n**************************\ndistancias[a][b][c]->indice [c] (usuario {} creados en celda a, distancia usuarios en celda b) -->CELDA[{}][{}][{}]".format(ind_us,ind_celda,ind_celda_1,ind_us))
	print(sim_colmena.hiperc_distancias[ind_celda][ind_celda_1][ind_us])

	print("\n**************************")
	print("\n**************************")
	print("\n******* INICIO DE LA PRUEBA 1 ************")
	print("\n**************************")
	print("\n**************************")
	test=[]
	organizacion=[0 for i in range(n_cel)]
	print(organizacion)
	for ind,celda in enumerate(sim_colmena.hiperc_distancias):
		print("Celda ", ind)
		print(celda)
		print("***")
		print(celda[0])
		test.append(celda[0])
		print("************************\n")

	print(test)
	'''
	print("\n**************************")
	print("\n**************************")
	print("\n******* INICIO DE LA PRUEBA 2 ************")
	print("\n**************************")
	print("\n**************************")
	organizacion=[0 for i in range(n_cel)] #usuarios de cada celda organizados.
	temporal=[] #array temporal
	print(sim_colmena.hiperc_distancias)
	for origen in range(n_cel):
		print("origen->",origen)
		for ind,celda in enumerate(sim_colmena.hiperc_distancias):
			print("Celda ", ind)
			print(celda)
			print("*** OUTPUT----->")
			print(celda[origen])
			a=celda[origen]
			print("<----->\n")
			temporal.append(a)
		organizacion[origen]=np.stack(temporal,axis=-1)
		temporal=[]
	print("IN: ",sim_colmena.hiperc_distancias)
	print("\nOUT 0: ")
	organizacion=np.asarray(organizacion).shape
	print("\n",organizacion)

	'''
	organizacion=[0 for i in range(n_cel)]
	temporal=[]
	def configurar_dimension():
		#Funcion que re dimensiona un arreglo de la forma [ [ [celda 1][celda2][celda3] ] [ [celda 1][celda2][celda3] ]]
		a una organizacion de usuarios por celda.

		#itero sobre el numero de celdas
		for users in range(n_cel):
			#itero sobre el arreglo
			for ind,celda in enumerate(target):
				arreglo=celda[users]
				temporal.append(arreglo)
			#guardo los arrays en stack en una lista
			organizacion[users]=np.stack(temporal,axis=-1)
			#convierto la lista en ndarray para ejecutar operaciones numpy.
			organizacion=np.asarray(organizacion)
			#limpio la lista temporal para guardar la siguiente iteracion de la celdas
			temporal=[]
	'''



	#print("\nOUT 0: ",organizacion[0])

	#print("OUT 1: ",organizacion[1])

	#print("OUT 2: ",organizacion[2])



	pass

	'''
	organizacion=[0 for i in range(n_cel)] #usuarios de cada celda organizados.
	temporal=[] #array temporal
	print(sim_colmena.hiperc_distancias)
	print("**************************")
	print("**************************")
	print("**************************")
	print("**************************")
	print(type(sim_colmena.hiperc_distancias))
	for origen in range(n_cel):
		print("origen->",origen )
		for ind,celda in enumerate(sim_colmena.hiperc_distancias):
			#print("Celda ", ind)
			#print(celda)
			#print("*** OUTPUT----->")
			#print(celda[origen])
			a=celda[origen]
			#print("<----->\n")
			temporal.append(a)
		organizacion[origen]=np.stack(temporal,axis=-1)
		temporal=[]
	print("IN: ",sim_colmena.hiperc_distancias)
	print("\nOUT 0: ")
	organizacion=np.asarray(organizacion)
	print("\n",organizacion)
	print("**************************")
	print("**************************")
	print("**************************")
	print("**************************")


	'''
	pass




	'''
	#print("[top]. MODELO DE PERDIDAS -ANTES")
	#print(sim_colmena.hiperc_modelo_canal.resultado_path_loss_antes) *ELIMINAR ANTES PATLOSS
	print("\n[top]. MODELO DE PERDIDAS + Desva (si aplica)")
	print(sim_colmena.hiperc_modelo_canal.resultado_path_loss) #ya no aplica, ahora aplica en el balance
	print("\n[top]. POTENCIA RECIBIDA, simplificado, sin tx. ")
	print(sim_colmena.hiperc_modelo_canal.balance_simplificado_antes)
	print("\n[top]. POTENCIA RECIBIDA + Desva (si aplica) ")
	print(sim_colmena.hiperc_modelo_canal.resultado_balance)
	print("\n[top]. MARGEN")
	print(sim_colmena.hiperc_modelo_canal.resultado_margen)


	Requerimiento:
	Es deseable para cada usuario, conocer: distancia, ganancia, perdidas, potencia recibida, de todas las celdas.

	------
	Idea 1.
	Crear n_cel matrices con la forma:

	Matriz 1 para distancia, usuarios creados en la celda 1:
		us1 usd2 usd3 ... usdi
	cel1
	cel2
	cel3
	...
	celj


	Matriz 2 para distancia, usuarios creados en la celda 2:
		us1 usd2 usd3 ... usdi
	cel1
	cel2
	cel3
	...
	celj

	...

	Matriz k para distancia, usuarios creados en la celda k:
		us1 usd2 usd3 ... usdi
	cel1
	cel2
	cel3
	...
	celj


	Se crean n_cel matrices para cada parametro distancia, ganancia, perdidas, potencia recibida.
	Iniciar con distancia y aplicar el mismo modelo a los demas parámetros.

	------
	Idea 2:

	Crear una matriz unica, con todos los usuarios de todas las estaciones.

		us1 us2 ... usi .. us21 us22 ... us2i .. .. usni
	cel1
	cel2
	cel3
	...
	celj

	***********************************
	crear ambas matrices y comparar cual seria mejor usar.

	Idea 1: desing:
	Requerimiento lv3:
	La estructura tiene el siguiente diseno: [-  [-[] [] []-]   [-[] [] []-]   [-[] [] []-] -]

	'''

	#plt.title("Escenario: "+propagacion[0])
	#sim_colmena.ver_celdas()
	#sim_colmena.ver_circulos()
	#sim_colmena.ver_estaciones_base()
	#sim_colmena.ver_usuarios_colores()
	#sim_colmena.ver_usuarios()
	#sim_colmena.ver_todo()
	#
	#sim_colmena.hiperc_antena.observar_patron()
	#plt.grid(True)
	#plt.show()

def prueba_sistema_v044():
	'''Prueba para implemenetar el requerimiento 1e del reporte version 39. Parte 4: datos por usuario.'''
	n_cel=5
	radio_cel=1000 #DEFINICION, SIEMPRE EN METROS. La distancia tambien es en metros.
	frecuencia=(1500,'mhz')
	intensidad=2/radio_cel**2
	print("INTENSIDAD DE ENTRADA: ",intensidad)
	distribucion=('ppp', intensidad)
	#verificar mcl
	#x_prueba=np.array([[1000, 0, 1000, 0],[1500, 1000, 1000, 1500]])
	#y_prueba=np.array([[0,	 10, 550, 580],[500, 1500, 1000, 1750]])
	#distribucion=("prueba_unitaria",(np.array([[1000, 250],[1500, 1000]]),np.array([[0, 250],[500, 1500]]))) #celdas=2
	#distribucion=("prueba_unitaria",(x_prueba,y_prueba) ) #celdas=2

	params_simulacion=[n_cel,radio_cel, distribucion, frecuencia]
	#propagacion='okumura_hata' #si no: se pone, se escribe o se escribe bien, el pathloss es 0
	hb=30 #m
	alfa=0
	hm=1.5
	params_prop=[hb, alfa, hm]
	#
	#params desv
	tipo_desv='normal'
	alpha_n=3.1
	sigma_xn=8.1
	mu=0
	play_desv=True
	#el tercer valor va en el mismo orden, dependiendo del desvanecimiento
	params_desv=[tipo_desv, play_desv, [alpha_n, sigma_xn, mu]]
	#
	propagacion=['okumura_hata', params_prop, params_desv]
	pot_tx=19 #dBm
	loss_tx=5
	gan_tx=15#
	gan_rx=8
	loss_rx=0
	sensibilidad=-92
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
	print("\n**************************")
	print("[top] Por celda: ",len(sim_colmena.usuario_x[0]), " usuarios.")
	print("[top]. Total usuarios en {} celdas".format(n_cel),sim_colmena.no_usuarios_total)
	print("************")
	print("[top]. Tipo hiper-dato: ",type(sim_colmena.hiperc_ganancia_relativa))
	print("************")
	print("[top]. Forma hiper-dato: ",sim_colmena.hiperc_ganancia_relativa.shape)
	print("**************************")
	'''
	#print("\n[top]. GANANCIA")
	#print(sim_colmena.hiperc_ganancia_relativa)
	print("[top]. DISTANCIAS->", type(sim_colmena.hiperc_distancias))
	print(sim_colmena.hiperc_distancias)
	print("\n[top]. MODELO DE PERDIDAS + Desva (si aplica)")
	print(sim_colmena.hiperc_modelo_canal.resultado_path_loss) #ya no aplica, ahora aplica en el balance
	print("\n[top]. POTENCIA RECIBIDA, simplificado, sin tx. ")
	print(sim_colmena.hiperc_modelo_canal.balance_simplificado_antes)

	print("\n[top]. MARGEN")
	print(sim_colmena.hiperc_modelo_canal.resultado_margen)
	'''
	print("\n[top]. POTENCIA RECIBIDA + Desva (si aplica) ")
	print(sim_colmena.hiperc_modelo_canal.resultado_balance.shape)
	#import dask.dataframe as dd
	#darr = dd.from_array(sim_colmena.hiperc_modelo_canal.resultado_balance[0])
	print(sim_colmena.hiperc_modelo_canal.resultado_balance)
	print("-")

	#np.savetxt('test1.txt', sim_colmena.hiperc_modelo_canal.resultado_balance[0])

	'''Stacking:
	Convertir arreglo a 2 dimensiones de la forma:
			celdas	+
	usuarios ...
	+

	concatenar: [   [a]   [b]    [c]  ... [z]   ]
	n=2
	aux=a+b
	aux=aux+c

	n=n

	for ind,celda in zip(concatenar):
		0, celda=a, concatenar[0+1]=b
		if ind == 0:
			aux=celda
		else:
			pass
		#1: aux=a+b, concatenar[1+1]=c
		aux=concatenate(aux,concatenar[i+1])

	In the general case of a (l, m, n) ndarray:
	numpy.reshape(a, (l*m, n)) should be used.
	numpy.reshape(a, (a.shape[0]*a.shape[1], a.shape[2]))

	'''
	'''
	In the general case of a (l, m, n) ndarray:
	numpy.reshape(a, (l*m, n)) should be used.
	numpy.reshape(a, (a.shape[0]*a.shape[1], a.shape[2]))
	'''
	potencia_recibida_dB=sim_colmena.hiperc_modelo_canal.resultado_balance
	l,m,n=sim_colmena.hiperc_modelo_canal.resultado_balance.shape
	potencia_recibida_dB_2D=np.reshape(potencia_recibida_dB, (l*m, n))
	print("------reshape 3D->2D-------")
	print(potencia_recibida_dB_2D)
	print("-----transpuesta, primera columna--------")
	print(np.transpose(potencia_recibida_dB_2D)[0])
	c0=np.transpose(potencia_recibida_dB_2D)[0]
	c=np.sum(potencia_recibida_dB_2D, axis=1, keepdims=True)
	print(c.shape) #initial no funciona
	print("------transpuesta, re dimensionamiento-------")
	c01=c0.reshape(c.shape)
	print(c0.reshape(c.shape))
	print("--------operacion interferencia. no unidades ----------")
	print(c-c01)
	#plt.title("Escenario: "+propagacion[0])
	#sim_colmena.ver_celdas()
	#sim_colmena.ver_circulos()
	#sim_colmena.ver_estaciones_base()
	#sim_colmena.ver_usuarios_colores()
	#sim_colmena.ver_usuarios()
	#sim_colmena.ver_todo()

	#
	#sim_colmena.hiperc_antena.observar_patron()
	#plt.grid(True)
	#plt.show()

def main2(x,y):
	fig=plt.figure()
	ax=fig.add_subplot(111)
	#ax.set_title('click on points')
	#x=np.array([1.41010145,2,3,4])
	#y=np.array([1,2.28282828289,3,4])
	line,=ax.plot(x,y,'ro',picker=6)
	def onpick(event):
		thisline=event.artist
		xdata=thisline.get_xdata()
		#todas las coordenadas
		ydata=thisline.get_ydata()
		#todas las coordenadas
		#print(xdata, ydata)
		ind=event.ind
		points=tuple(zip(xdata[ind], ydata[ind]))
		print("on pick points", points, type(points[0][0]))
		print("x :",np.around(points[0][0],6))
		print("y :",np.around(points[0][1],6))
	fig.canvas.mpl_connect('pick_event',onpick)
	#plt.show()




def prueba_sistema_v045():
	'''Prueba para implemenetar el requerimiento 1e del reporte version 39. Parte 4: sinr y contabilidad'''
	params_simulacion, params_transmision, params_perdidas=parametros_de_prueba()
	n_cel=3
	#INICIO DE LA SIMULACION
	sim_colmena=ss.Sistema_Celular(params_simulacion, params_transmision, params_perdidas)
	print("\n**************************")
	print("[top] Por celda: ",len(sim_colmena.usuario_x[0]), " usuarios.")
	print("[top]. Total usuarios en {} celdas".format(n_cel),sim_colmena.no_usuarios_total)
	print("************")
	print("[top]. Tipo hiper-dato: ",type(sim_colmena.hiperc_ganancia_relativa))
	print("************")
	print("[top]. Forma hiper-dato: ",sim_colmena.hiperc_ganancia_relativa.shape)
	print("**************************")
	print("\n[top]. POTENCIA RECIBIDA + Desva (si aplica) ")
	print(sim_colmena.hiperc_modelo_canal.resultado_balance.shape)
	#import dask.dataframe as dd
	#darr = dd.from_array(sim_colmena.hiperc_modelo_canal.resultado_balance[0])
	print(sim_colmena.hiperc_modelo_canal.resultado_balance)
	print("***************************")

	#np.savetxt('test1.txt', sim_colmena.hiperc_modelo_canal.resultado_balance[0])

	'''
	Requerimiento, calcular sinr:
		1. identificar celda de conexion, criterio: mayor potencia recibida.
			1.1 reemplazar con 0 las potencias maximas.
		2. sumar las potencias interferentes en veces
			2.1 convertir a dB.
		3. calcular la sinr, relacionado Max_ptx, pn y ptx_interf; con la ecuacion dada en dB.
	In the general case of a (l, m, n) ndarray:
	numpy.reshape(a, (l*m, n)) should be used.
	numpy.reshape(a, (a.shape[0]*a.shape[1], a.shape[2]))
	'''
	#creo la variable local de trabajo
	potencia_recibida_dB=sim_colmena.hiperc_modelo_canal.resultado_balance
	#obtenengo las dimensiones del arreglo cluster
	l,m,n=sim_colmena.hiperc_modelo_canal.resultado_balance.shape
	#redimensiono la potencia recibida de un arreglo 3D a 2D.
	potencia_recibida_dB_2D=np.reshape(potencia_recibida_dB, (l*m, n))
	#convierto a veces
	potencia_recibida_v_2D=(10**(potencia_recibida_dB_2D/10))
	#
	print("array 2D, veces\n", potencia_recibida_v_2D)
	#
	#filtro y obtengo los valores maximos en veces.
	maximo=np.nanmax(potencia_recibida_v_2D,axis=-1)
	#
	print("res maximo\n", maximo)
	#creo una variable auxiliar
	indices=[]
	#itero sobre el maximo y el array 2D.
	indx=0
	for maxx, arr in zip(maximo, potencia_recibida_v_2D):
		print("componentes:\n",arr,maxx)
		print("arreglo:\n",potencia_recibida_v_2D[indx])
		#obtengo el lugar (indice) en el array donde esta el valor maximo de potencia
		indice=np.where(arr==maxx)
		#reeemplazo los valores maximos con 0
		potencia_recibida_v_2D[indx][indice]=0
		print(indice[0])
		#guardo el indice.
		indices.append(indice[0])
		indx+=1
	#convierto a una dimension el array.
	ind_np=np.stack(indices)
	#
	print("Celdas destino",ind_np, ind_np.shape)
	celdas_usuarios_conectados=[]

	#contamos cuantos usuarios por celda fueron conectados a la mayor potencia recibida.
	for cnt in range(n_cel): #range numero de celdas
		celdas_usuarios_conectados.append(np.count_nonzero(ind_np==cnt))
	#cuentas_0=np.count_nonzero(ind_np==0)
	print("En su orden, usuarios conectados:",celdas_usuarios_conectados)

	print("Arreglo limpio en potencia recibidad maxima")
	print(potencia_recibida_v_2D)
	#sumo en el eje x, manteniendo la dimension. #DIMENION SE PUEDE MANTENER PARA OPTIMIZAR
	suma_interf=np.sum(potencia_recibida_v_2D, axis=1, keepdims=True)
	print("Suma en Arreglo limpio en potencia recibidad maxima")
	print(suma_interf) #ok
	#re definimos la dimension de la potencia recibida en veces
	prx_veces=maximo.reshape(suma_interf.shape) #

	print("--------operacion interferencia. no unidades ----------\n", prx_veces)
	pn=10**(sim_colmena.potencia_ruido/10) #en veces
	#calculo sinr de acuerdo a la ecuacion
	SINR_dB=10*np.log10(prx_veces)-10*np.log10(suma_interf+pn)
	print("SIRN[dB]: \n",SINR_dB)
	print("----")
	print("celda |---| sinr")
	for a,b in zip(ind_np,SINR_dB):

		print(a, "  |---|",b)

	#print(sim_colmena.usuario_x.flatten())
	#print(sim_colmena.usuario_y.flatten())
	x=sim_colmena.usuario_x.flatten()
	y=sim_colmena.usuario_y.flatten()
	print(np.around(x,6))
	print(np.around(y,6))

	plt.title("Escenario: "+ params_perdidas[0][0])
	sim_colmena.ver_todo()
	main2(x,y)
	#sim_colmena.hiperc_antena.observar_patron()
	plt.grid(True)
	plt.show()


def prueba_sistema_v045_1():
	'''Prueba para implemenetar el requerimiento 1e del reporte version 39. Parte 4: sinr y contabilidad'''
	params_simulacion, params_transmision, params_perdidas=parametros_de_prueba()
	n_cel=3
	#INICIO DE LA SIMULACION
	sim_colmena=ss.Sistema_Celular(params_simulacion, params_transmision, params_perdidas)
	print("\n**********Inicio de la prueba [top]****************")
	print("[top] Por celda: ",len(sim_colmena.usuario_x[0]), " usuarios.")
	print("[top]. Total usuarios en {} celdas".format(n_cel),sim_colmena.no_usuarios_total)
	print("***************************")
	'''
	#creo la variable local de trabajo
	potencia_recibida_dB=sim_colmena.hiperc_modelo_canal.resultado_balance
	#obtenengo las dimensiones del arreglo cluster
	l,m,n=sim_colmena.hiperc_modelo_canal.resultado_balance.shape
	#redimensiono la potencia recibida de un arreglo 3D a 2D.
	potencia_recibida_dB_2D=np.reshape(potencia_recibida_dB, (l*m, n))
	#convierto a veces
	potencia_recibida_v_2D=(10**(potencia_recibida_dB_2D/10))
	#
	#print("array 2D, veces\n", potencia_recibida_v_2D)
	#
	#filtro y obtengo los valores maximos en veces.
	maximo=np.nanmax(potencia_recibida_v_2D,axis=-1)
	#
	#print("res maximo\n", maximo)
	#creo una variable auxiliar
	indices=[]
	#itero sobre el maximo y el array 2D.
	indx=0
	for maxx, arr in zip(maximo, potencia_recibida_v_2D):
		#print("componentes:\n",arr,maxx)
		#print("arreglo:\n",potencia_recibida_v_2D[indx])
		#obtengo el lugar (indice) en el array donde esta el valor maximo de potencia
		indice=np.where(arr==maxx)
		#reeemplazo los valores maximos con 0
		potencia_recibida_v_2D[indx][indice]=0
		#print(indice[0])
		#guardo el indice.
		indices.append(indice[0])
		indx+=1
	#convierto a una dimension el array.
	ind_np=np.stack(indices)
	#
	#print("Celdas destino",ind_np, ind_np.shape)
	celdas_usuarios_conectados=[]

	#contamos cuantos usuarios por celda fueron conectados a la mayor potencia recibida.
	for cnt in range(n_cel): #range numero de celdas
		celdas_usuarios_conectados.append(np.count_nonzero(ind_np==cnt))
	#cuentas_0=np.count_nonzero(ind_np==0)
	#("En su orden, usuarios conectados:",celdas_usuarios_conectados)

	#print("Arreglo limpio en potencia recibidad maxima")
	#print(potencia_recibida_v_2D)
	#sumo en el eje x, manteniendo la dimension. #DIMENION SE PUEDE MANTENER PARA OPTIMIZAR
	suma_interf=np.sum(potencia_recibida_v_2D, axis=1, keepdims=True)
	#print("Suma en Arreglo limpio en potencia recibidad maxima")
	#print(suma_interf) #ok
	#re definimos la dimension de la potencia recibida en veces
	prx_veces=maximo.reshape(suma_interf.shape) #
	print("inteferente en veces \n", prx_veces )

	pn=10**(sim_colmena.potencia_ruido/10) #en veces
	print("potencia de ruido <---------\n", pn)
	#calculo sinr de acuerdo a la ecuacion
	SINR_dB=10*np.log10(prx_veces)-10*np.log10(suma_interf+pn)
	print("SIRN[dB]: \n",SINR_dB)
	print("----")
	print("celda |---| sinr")
	for a,b in zip(ind_np,SINR_dB):

		print(a, "  |---|",b)
	'''
	print("***************************")
	sim_colmena.info_sinr()


def prueba_sistema_v045_2():
	'''Prueba para implemenetar el requerimiento 1e del reporte version 39. Parte 4: montecarlo'''
	params_simulacion, params_transmision, params_perdidas=parametros_de_prueba()
	n_cel=params_simulacion[0]
	print("**************************************************")
	print("**********Inicio de la prueba [top]****************")
	print("**************************************************")
	iteracion=1#
	#INICIO DE LA SIMULACION
	#sim_colmena=ss.Sistema_Celular(params_simulacion, params_transmision, params_perdidas)
	#print("[top] Por celda: ",len(sim_colmena.usuario_x[0]), " usuarios.")
	#print("[top]. Total usuarios en {} celdas".format(n_cel),sim_colmena.no_usuarios_total)


	coleccion_simulacion=[]
	it=0
	for n in range(iteracion):
		print("**********SIMULACION {}*****************".format(it))
		coleccion_simulacion.append(ss.Sistema_Celular(params_simulacion, params_transmision, params_perdidas))
		it+=1

	coleccion_relacion_conexion=[]
	for simulacion in coleccion_simulacion:
		#simulacion.ver_todo() # ok.
		coleccion_relacion_conexion.append(simulacion.medida_conexion)
	#coleccion_relacion_conexion=np.stack(coleccion_relacion_conexion)



	plt.figure()
	plt.plot(coleccion_relacion_conexion,'b*-')
	coleccion_relacion_conexion=np.sort(coleccion_relacion_conexion)
	plt.plot(coleccion_relacion_conexion,'r*-')
	p=1.*np.arange(len(coleccion_relacion_conexion))/(len(coleccion_relacion_conexion)-1)
	#print(p)
	'''
	eje_x=np.arange(1,len(coleccion_relacion_conexion)+1)
	#coleccion_relacion_conexion=np.sort(coleccion_relacion_conexion)#

	acomulativa=np.cumsum(coleccion_relacion_conexion) #normalizado
	print(eje_x, acomulativa, max(acomulativa))

	#
	'''
	fig=plt.figure()
	ax1=fig.add_subplot(121)
	ax1.plot(p,coleccion_relacion_conexion, 'g-')
	ax1.set_xlabel("$Dist P$")
	ax1.set_ylabel("$Conexion$")

	ax2=fig.add_subplot(122)
	ax2.plot(coleccion_relacion_conexion,p, 'k-')
	ax2.set_xlabel("$Conexion$")
	ax2.set_ylabel("$Dist P$")

	plt.figure()
	plt.hist(coleccion_relacion_conexion)


	'''Definicion prueba de montecarlo:
	El sistema celular tiene la siguiente propiedad:
	self.medida_conexion=self.conexion_total/self.no_usuarios_total

	La prueba de montecarlo del hexagono fue definida asi:
	montecarlo=(area_hexagono/area_circulo), en terminos de radio, seria:
	P(x: x C Hexagono)=(area_hexagono/area_circulo)
	P(...) -> P(x: x esta contenido en Hexagono)
	Despejando el área del hexagono obtenemos:
	 -> area_hexagono= ( P(...) * pi*r**2)
	 N_a=sum(puntos)
	 N=len(puntos)
	 P_a=N_a/N
	 print("probabilidad de exito", P_a)
	 print("area del hexagono: ", math.pi*self.radio**2*P_a)
	 acomulativa=np.cumsum(puntos)

	Luego,
	P(x: x E conexion) = conexion_total/no_usuarios_total
	conexion_total: x: x>12 dB
	no_usuarios_total=n

	N_a=conexion_total
	N=no_usuarios_total
	P_a=N_a/N

	Luego:
	Luego, cual es la relacion de P_a, con la probabilidad de outage? cual seria la ecuacion.
	Sera que P_a = Probabilida de outage?
	'''
	plt.figure()
	N=len(coleccion_relacion_conexion)
	eje_x=np.arange(1,N+1)
	#print(eje_x)

	plt.show()


def prueba_sistema_v046():
	'''Prueba para implemenetar el requerimiento 1e del reporte version 39. Parte 4: usuarios por color, si iteracion==1.'''
	params_simulacion, params_transmision, params_perdidas=parametros_de_prueba()
	n_cel=params_simulacion[0]
	print("**************************************************")
	print("**********Inicio de la prueba [top]****************")
	print("**************************************************")
	iteracion=1#
	#INICIO DE LA SIMULACION
	#sim_colmena=ss.Sistema_Celular(params_simulacion, params_transmision, params_perdidas)
	#print("[top] Por celda: ",len(sim_colmena.usuario_x[0]), " usuarios.")
	#print("[top]. Total usuarios en {} celdas".format(n_cel),sim_colmena.no_usuarios_total)


	coleccion_simulacion=[]
	it=0
	for n in range(iteracion):
		print("**********SIMULACION {}*****************".format(it))
		coleccion_simulacion.append(ss.Sistema_Celular(params_simulacion, params_transmision, params_perdidas))
		it+=1

	print(coleccion_simulacion[0].usuario_x.shape)
	###print(coleccion_simulacion[0].usuario_x)
	#este procedimiento no es el correcto.
	##coordendas_nuevas_x=coleccion_simulacion[0].configurar_organizar_arreglos(coleccion_simulacion[0].usuario_x)
	#print(coordendas_nuevas_x.shape)
	'''El requerimiento es crear 1 arreglo 2D a 1D'''
	coordendas_nuevas_x=coleccion_simulacion[0].configurar_disminuir_dim(coleccion_simulacion[0].usuario_x)
	coordendas_nuevas_y=coleccion_simulacion[0].configurar_disminuir_dim(coleccion_simulacion[0].usuario_y)
	print("[Top.pruebas] 1",coordendas_nuevas_x.shape, coordendas_nuevas_x.shape)
	#print("[Top.pruebas] 2",coordendas_nuevas_x)
	#print("[Top.pruebas] 3",coordendas_nuevas_y)

	###plt.plot(coordendas_nuevas_x,coordendas_nuevas_y, "+") ok.

	#coleccion_simulacion[0].info_sinr()
	'''
	Requerimiento 1:
		Distinguir los usuarios conectados de los que no.
	Requerimiento 2:
		Distinguir los usuarios por celda, y ademas requerimiento 1.

	'''
	mapa=coleccion_simulacion[0].mapa_conexion_usuario
	sinr=coleccion_simulacion[0].sinr_db
	conexion=np.where(sinr>12,1,0)
	mapa_estacion=coleccion_simulacion[0].mapa_conexion_estacion
	print(mapa_estacion)
	ind=0
	print("usuario---conex?--celda--sinr")
	for bandera,t1,t2 in zip(conexion,mapa,sinr):
		print("     {}   {}     {}     {}".format(ind,bandera, t1,t2))
		ind+=1

	'''Solo necesito 3 arreglos: ind, bandera, y mapa. Sinr no pues mapa se deriva de sinr.
	Si, considero la bandera, 0 indica desconexion. Luego, si reemplazo en esa misma posicion -1 en mapa.
	Obtengo un mapa de ncel variables + -1 indicando desconexion.
	'''
	#plt.figure()
	for usuario, (bandera, map) in enumerate(zip(conexion, mapa)):
		#print(usuario, bandera, map)
		if bandera==0:
			mapa[usuario]=-1
	#ctest=[map/max(i) for i in range()]
	#print(ctest)
	'''
	colores=0
	for usuario, map in enumerate(mapa):
		thisx=coordendas_nuevas_x[usuario]
		thisy=coordendas_nuevas_y[usuario]
		if map==-1:
			plt.plot(thisx,thisy,'k+')
		else:
			#color=np.array([map/max(mapa),0,0])
			plt.plot(thisx,thisy,'go')
	#print(mapa)
	'''
	#OPCION PANDAS.
	import pandas as pd
	testx=coordendas_nuevas_x
	testy=coordendas_nuevas_y
	mapa=np.reshape(mapa, testx.shape)
	print(mapa.shape)
	print(testx.shape, testy.shape, mapa.shape)

	data=pd.DataFrame({"X value":testx, "Y value":testy, "Category":mapa})
	print(data)
	grupos=data.groupby("Category")
	'''
	for name, group in grupos:
		#thisx=coordendas_nuevas_x[usuario]
		#thisy=coordendas_nuevas_y[usuario]
		plt.plot(group["X value"], group["Y value"], marker="o", linestyle="", label=name)
	plt.legend()
	'''
	med=coleccion_simulacion[0].conexion_total
	print("Medida:",med)
	coleccion_simulacion[0].ver_todo()
	coleccion_simulacion[0].info_sinr()

	#PRUEBA TERMINADA EXITOSAMENTE.
	plt.show()


def prueba_sistema_v046_1():
	'''Prueba para implemenetar el requerimiento 1e del reporte version 39. Parte 4: usuarios por color, si iteracion==1.'''
	params_simulacion, params_transmision, params_perdidas=parametros_de_prueba()
	n_cel=params_simulacion[0]
	print("**************************************************")
	print("**********Inicio de la prueba [top]****************")
	print("**************************************************")
	iteracion=1#
	#INICIO DE LA SIMULACION
	#sim_colmena=ss.Sistema_Celular(params_simulacion, params_transmision, params_perdidas)
	#print("[top] Por celda: ",len(sim_colmena.usuario_x[0]), " usuarios.")
	#print("[top]. Total usuarios en {} celdas".format(n_cel),sim_colmena.no_usuarios_total)


	coleccion_simulacion=[]
	it=0
	for n in range(iteracion):
		print("**********SIMULACION {}*****************".format(it))
		coleccion_simulacion.append(ss.Sistema_Celular(params_simulacion, params_transmision, params_perdidas))
		it+=1

	#coleccion_simulacion[0].ver_todo()
	#coleccion_simulacion[0].info_sinr()
	print("De {} usuarios, {} cumplen BER objetivo. P_a: {}".format(coleccion_simulacion[0].no_usuarios_total,
	 	coleccion_simulacion[0].conexion_total, coleccion_simulacion[0].medida_conexion))
	#PRUEBA TERMINADA EXITOSAMENTE.
	plt.show()

def prueba_sistema_v046_2():
	'''Prueba para implemenetar el requerimiento 1e del reporte version 39. Parte 4: intensida sinr, si iteracion==1.'''
	params_simulacion, params_transmision, params_perdidas=parametros_de_prueba()
	n_cel=params_simulacion[0]
	print("**************************************************")
	print("**********Inicio de la prueba [top]****************")
	print("**************************************************")
	iteracion=1#
	#INICIO DE LA SIMULACION
	#sim_colmena=ss.Sistema_Celular(params_simulacion, params_transmision, params_perdidas)
	#print("[top] Por celda: ",len(sim_colmena.usuario_x[0]), " usuarios.")
	#print("[top]. Total usuarios en {} celdas".format(n_cel),sim_colmena.no_usuarios_total)


	coleccion_simulacion=[]
	it=0
	for n in range(iteracion):
		print("**********SIMULACION {}*****************".format(it))
		coleccion_simulacion.append(ss.Sistema_Celular(params_simulacion, params_transmision, params_perdidas))
		it+=1

	#coleccion_simulacion[0].ver_todo()
	coleccion_simulacion[0].info_sinr() #.info_sinr(True)
	simtest=coleccion_simulacion[0]
	test=simtest.sinr_db

	#print(test)
	#print(test.shape)
	intensidad=simtest.configurar_disminuir_dim(test)
	#print(intensidad)
	#print(intensidad.shape)
	colormap=plt.cm.cool
	normalize=plt.Normalize(vmin=min(intensidad), vmax=max(intensidad))
	coordendas_nuevas_x=coleccion_simulacion[0].configurar_disminuir_dim(coleccion_simulacion[0].usuario_x)
	coordendas_nuevas_y=coleccion_simulacion[0].configurar_disminuir_dim(coleccion_simulacion[0].usuario_y)
	testx=coordendas_nuevas_x
	#print(testx)
	testy=coordendas_nuevas_y

	plt.scatter(testx, y=testy,c=intensidad, cmap=colormap,marker='o')

	#a=[4,5,2,5,6,20,1,34]
	#colormap=plt.cm.cool
	plt.show()


def prueba_sistema_v046_3():
	'''Prueba para implemenetar el requerimiento 1e del reporte version 39. Parte 4: intensida potencia recibida, si iteracion==1.'''
	params_simulacion, params_transmision, params_perdidas=parametros_de_prueba_unitaria()
	n_cel=params_simulacion[0]
	print("**************************************************")
	print("**********Inicio de la prueba [top]****************")
	print("**************************************************")
	iteracion=1#
	coleccion_simulacion=[]
	it=0
	for n in range(iteracion):
		print("**********SIMULACION {}*****************".format(it))
		coleccion_simulacion.append(ss.Sistema_Celular(params_simulacion, params_transmision, params_perdidas))
		it+=1

	simtest=coleccion_simulacion[0]
	simtest.info_sinr() #.info_sinr(True) para imprimir la sinr
	#test=simtest.sinr_db
	#simtest.ver_todo(1,False)
	#print(simtest.malla_x.shape)
	'''Crear matriz con ceros, reeemplazar cada valor con el maximo. Con la misma shape original.
	Crear otra matriz con el indice de la potencia mayor'''
	#print(simtest.hiperc_malla_distancias.shape)
	hiperm_ang=simtest.hiperc_malla_ganancia_relativa
	#print(hiperm_ang[1])
	#celdas=2, 2 matrices.
	#shape original de x,y
	'''
	print("------")
	print("shape original")
	print(simtest.malla_x)
	print("---")
	print(simtest.malla_y)
	print("------")

	#distancias hiper matriz.
	print("shape distancias", simtest.hiperc_malla_distancias.shape)
	print(simtest.hiperc_malla_distancias[0])
	print("---")
	print(simtest.hiperc_malla_distancias[1])
	#angulos hiper angulos
	print("---")
	print("hiper malla angulos")
	print(simtest.hiperc_malla_angulos.shape) #ok
	print("---------")
	#ganancia relativa.
	print("shape ganancia relativa ")
	print(simtest.hiperc_malla_ganancia_relativa.shape)
	print("--")
	print(simtest.hiperc_malla_ganancia_relativa)
	print("-------")
	#paths loss
	print("path loss")
	print(simtest.hiperc_malla_modelo_canal.resultado_path_loss)
	#potencia recibida.
	'''
	print("balance mcl")
	#print(simtest.hiperc_modelo_canal.resultado_balance)
	#print(simtest.hiperc_malla_modelo_canal.resultado_balance)

	pr=simtest.hiperc_malla_modelo_canal.resultado_balance
	prmax_v=np.maximum(pr[0],pr[1])
	pr_max=pr[0]
	for ind,pr_i in enumerate(pr):
		print("indice",ind)
		pr_max=np.maximum(pr_max, pr_i)
	#print(pr_max)
	pr_max=pr_max[:-1,:-1]
	z_min,z_max=-np.abs(pr_max).max(), np.abs(pr_max).max()
	print(z_min, z_max)
	fig,ax=plt.subplots()
	xx=simtest.malla_x
	yy=simtest.malla_y
	#c=ax.pcolormesh(xx,yy,pr_max, cmap='RdBu', vmin=z_min, vmax=z_max)
	c=ax.pcolormesh(xx,yy,pr_max, cmap='plasma', vmin=z_min, vmax=-40)
	fig.colorbar(c,ax=ax)
	#sinr.
	#compilado de matrices.
	#graficar.
	#plt.figure()
	#plt.plot(simtest.malla_x, simtest.malla_y, 'ro')
	#plt.plot(simtest.origen_cel_x,simtest.origen_cel_y,'gv')
	plt.grid(True)
	plt.show()

def prueba_sistema_v046_4():
	'''Prueba para implemenetar el requerimiento 1e del reporte version 39. Parte 4: intensida sinr, si iteracion==1.'''
	params_simulacion, params_transmision, params_perdidas=parametros_de_prueba_unitaria()
	n_cel=params_simulacion[0]
	print("**************************************************")
	print("**********Inicio de la prueba [top]****************")
	print("**************************************************")
	iteracion=1#
	coleccion_simulacion=[]
	it=0
	for n in range(iteracion):
		print("**********SIMULACION {}*****************".format(it))
		coleccion_simulacion.append(ss.Sistema_Celular(params_simulacion, params_transmision, params_perdidas))
		it+=1

	simtest=coleccion_simulacion[0]
	print("total",simtest.no_usuarios_total)
	simtest.info_sinr() #.info_sinr(True) para imprimir la sinr

	#test=simtest.sinr_db
	simtest.ver_todo(1,False)
	plt.show()
	#print(simtest.malla_x.shape)
	'''Crear matriz con ceros, reeemplazar cada valor con el maximo. Con la misma shape original.
	Crear otra matriz con el indice de la potencia mayor'''

def prueba_sistema_v047():
	'''Prueba para implemenetar el requerimiento 1e del reporte version 39. Guardar y cargar datos de configuracion.'''
	#params_simulacion, params_transmision, params_perdidas=parametros_de_prueba_unitaria()
	#n_cel=params_simulacion[0]
	print("**************************************************")
	print("**********Inicio de la prueba [top]****************")
	print("**************************************************")
	from utilidades import config as cfg
	import sistema2 as ss2
	import json
	#with open("utilidades/configs.json") as json_data_file:
	#	data = json.load(json_data_file)

	configuracion=cfg.cargar_variables(target_path="utilidades/")
	'''
	print("---------------")
	print(configuracion['cfg_simulador']['params_general'])
	print("---------------")
	print(configuracion['cfg_simulador']['params_propagacion'])

	print("---------------")
	print(configuracion['cfg_simulador']['params_balance'])
	print("---------------")
	print(configuracion['cfg_simulador']['params_antena'])
	'''
	pass
	'''Requerimiento 2:
		generar coordenadas de estacion base, que son fijas, por fuera de la simulacion. Optimizar.'''
	iteracion=1#
	coleccion_simulacion=[]
	it=0
	for n in range(iteracion):
		print("**********SIMULACION {}*****************".format(it))
		coleccion_simulacion.append(ss2.Sistema_Celular(params_simulacion, params_transmision, params_perdidas))
		it+=1


	simtest=coleccion_simulacion[0]
	




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
	#prueba_sistema_v041()
	#prueba_sistema_v042()
	#prueba_sistema_v043()
	#prueba_sistema_v044()
	#prueba_sistema_v045() #pruebas de sinr, 12db, conexino por color.
	#prueba_sistema_v045_1() #implementacion y comparacion
	#prueba_sistema_v045_2() #montecarlo
	#prueba_sistema_v046() #usuarios por celda, conectados vs desconectados, colores
	#prueba_sistema_v046_1() #verificacion prueba 46.
	#prueba_sistema_v046_2() #pruebas de mapa de intensidad de sinr_db. ok, pero no es conveniente.
	#prueba_sistema_v046_3() #pruebas con fixed data: pruebas con meshgrid. potencia recibida
	#prueba_sistema_v046_4() ##pruebas con fixed data: pruebas con meshgrid. sinr . En espera
	prueba_sistema_v047() #pruebas de archivo de configuracion.

else:
	print("Modulo Importado: [", os.path.basename(__file__), "]")

'''Requerimientos:

1. [ok] Si cada modelo de propagacion tiene sus propias variables, como las recibo? ->parametros de entrada del modelo,
	reciben el nombre del modelo y sus parametros. Cada funcino interna del modelo del canal, selecciona
	sus parametros internos de acuerdo a un orden establecido.
2. [ok] Seleccionar el modelo de canal segun las unidades de freccuencia y distancia.
O, convertir todo a una misma unidad para efectos de uso. -> funcion modelocanal.inicializar_tipo()

3. -----Supongamos que tenemos n realizaciones de instancias de la clase Sistema_Celular. Cada instancia tiene
diferentes longitudes de usuarios, por ser el resutlado de un numero poisson.
Luego, como realizar una comparacion entre simulaciones?. Que es lo que se compara en cobertura?
	a. idea 1: la probabilidad de outage es un valor unico en cada simulacion, puede compararse.
		1.1 debe ser un kpi comparable, que sea unico a pesar de los diferentes usuarios.

4. [OK] La funcion normal especifica un numero de puntos asociados, pero si estos no son especificados?
Por ejemplo, tengo un array numpy y deseo operar sobre ellos, como deberia operar? ->solucionado,np.random.normal, funciona con np.shape.

5. [OK] Deseo como parametro de entrada, especificar si quiero incorporar el desvanecimiento o no. ->

6. [ok] Modelo del canal debe especificar cuando se hace el balance del enlace, no la clase sistema.->todo se inicializa en modelo del canal
7. [OK] Revisar ecuacion del balance
	->corregido la sensibilidad. Ahora la sensibilidad se define negativo.
8. [ok] Implmentar balance del enlace, mcl. mcl debe ser un parametro de entrada?
	->no. Revisar las condiciones urbano.
9. ----Implementar clase usuario, crear view interactiva y obtener informacion, dada las coordendas.
	9.1 crear hiper matriz organizada.
		[ok] idea 1.- matriz con matrices adentro: VER DEFINICION PRUEBA 43. implementada, con transpose y stack.
				idea 1.1.-existen dos formas de conseguir los valores de un usuario. ejecutando la funcion de organizacion
				para cada parametro, o ejecutar 1 vez la funcion a la matriz de distancia que en ultimas es la matriz con
				la que se realizan los demas calculos.
		idea 2. super matriz con todos los valores.

10. [ok] El desvanecimiento lento es una suma al balance del enlace, pero el rayleigh no. El rayleigh modifica
las perdidas o el balance simple, se convierte a unidades lineales y finalmente logaritmicas.
Pero cuando se usa la ecuacion mcl, el patron no responde. Investigar y arreglar este inconveniente.
	->el error era el signo de la operacion. La ecuacion mcl opera con signos contrarios. Cuando se hace el
	cambio de pathloss por desvanecimiento de rayileght, el desvanecimiento tiene un signo contrario.
	pathloss+etc=>balance simplificado
	si es normal:
		a. (pathloss+etc)+N
		fin
	si es profundo:
		a. res=ray(pathloss+etc)
		b. usar ecuacion.
 11. [OK] Integrar las vistas en ver todo.


 12. [parcialmente terminado] implementar el borrado de variables locales, para optimizar el simulador, para varias simulaciones.
 13. Implementar grafico de intensidad, en funcion de sinr y coordendas de usuario.
 14. Implementar ARCHIVO DE CONFIGURACION.
 	14.1 "prueba_unitaria". Si prueba unitaria, descartar valor intensidad o poner 0, usar datos_prueba_unitaria.txt, con los valores de usuarios a probar.
	14.2 Si iteracion >1, play_intensidad=False. play_desv[1]->potencia recibida, play_intensidad[2]:sinr.
'''
