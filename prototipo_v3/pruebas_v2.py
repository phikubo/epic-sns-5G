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
	radio_cel=1732#DEFINICION, SIEMPRE EN METROS. La distancia tambien es en metros.

	frecuencia=(900,'mhz')
	bw=20 #'mhz') #1.4, 3, 5, 10, 15, 20, ..., 50, 100, 200, 400
	intensidad=10/radio_cel**2
	fr=5 #dB

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


	#distribucion=("prueba_unitaria",(np.array([[1000, 250],[1500, 1000]]),np.array([[0, 250],[500, 1500]])), mapa_calor) #celdas=2
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
	pot_tx=38 #dBm #para un 1w, 10 watts para rural.
	loss_tx=1 #dB
	gan_tx=15#dBi
	gan_rx=5 #dBi
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


def prueba_sistema_v047():
	'''Prueba para implemenetar el requerimiento 1e del reporte version 39. Guardar y cargar datos de configuracion.'''
	params_simulacion, params_transmision, params_perdidas=parametros_de_prueba_unitaria()
	#n_cel=params_simulacion[0]
	print("**************************************************")
	print("**********Inicio de la prueba [top]****************")
	print("**************************************************")
	from utilidades import config as cfg
	import v2_sistema as ss2
	import json
	#with open("utilidades/configs.json") as json_data_file:
	#	data = json.load(json_data_file)

	configuracion=cfg.cargar_variables(target_path="utilidades/")
	'''
	Requerimiento 2:
		generar coordenadas de estacion base, que son fijas, por fuera de la simulacion. Optimizar.
	'''
	iteracion=1#
	coleccion_simulacion=[]
	it=0
	for n in range(iteracion):
		print("**********SIMULACION {}*****************".format(it))
		coleccion_simulacion.append(ss.Sistema_Celular(params_simulacion, params_transmision, params_perdidas))
		it+=1


	simtest=coleccion_simulacion[0]
	simtest.info_sinr(True)
	simtest.ver_todo()





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
