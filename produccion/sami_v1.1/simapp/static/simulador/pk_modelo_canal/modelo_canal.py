#import
import matplotlib.pyplot as plt
import numpy as np
import math
import os
#como esto no usa submodulos, no necesito hacer try catch en esos modulos.
#en el futuro si puede ocurrir, asi que:

#try:
	#aqui van los submodulos.
#except:
	#pass

#modelo del canal incluye perdidas AWGN y RUIDO. Crear modulos awgn y ruido. desechado.

#Falta validar unidades de distancias y frequencias.

class Modelo_Canal:
	"""Clase que define el modelo del canal, calcula las perdidas del sistema. No adiciona AWGN ni Ruido."""
	def __init__(self, cfg, arreglos): #usar args and kwards, recibir tipo de primero, y sus parametros.
		#RX_PWR = TX_PWR – Max (pathloss – G_TX – G_RX, MCL)
		#ENTRADA
		self.arreglos=arreglos.copy()
		self.cfg_gen=cfg['params_general']
		self.cfg_prop=cfg['params_propagacion']
		self.cfg_bal=cfg['params_balance']

		try:
			self.mapa_calor=self.arreglos[3]
		except:
			pass

		if self.cfg_gen['debug']:
			print('parametros modelo', self.cfg_prop["params_modelo"])
			print('parametros desvanecimiento', self.cfg_prop["params_desv"])
		#AUXILIAR
		#self.distancias=0
		self.distancias=0 #distancia general
		self.portadora=self.cfg_gen["portadora"][0]

		#presimulacion
		self.custom_dist_flag=False
		#por defecto custom_dist no cambia de magnitud. La magnitud (km, m) se controla en las funciones que generan las imagenes de presimulacion.
		self.custom_dist=0

		self.tx_grel=self.arreglos[1] #en cero estan los valore,s en 1 estan las unidades.

		self.resultado_path_loss_antes=0 #eliminar, dejar solo en debug.
		self.desvanecimiento=0
		self.balance_simplificado_antes=0
		self.balance_simplificado=0

		#SALIDA
		self.resultado_path_loss=0
		self.resultado_balance=0

		self.resultado_margen=0 #DEPLETED

		self.resultado_balance_v=0

		#aplica desvanecimiento si aplica.
		self.inicializar_tipo()
		#se altera el orden para poder obtener los valores de perdidas, en el
		#desvanecimiento rayleight, y luego, adicionar ese desvanecimiento al balance del enlace
		self.balance_del_enlace_mcl() #f(configurar_desvanecimiento())
		#self.inicializar_balance()

	def configurar_desvanecimiento(self):
		'''Crea un array de desvanecimiento, dependiendo del tipo y especificaciones extras'''
		if self.custom_dist_flag:
			#perdidas positivo, ganancia de tx es maxima por que se transmite un solo lobulo.
			self.balance_simplificado=np.vstack(self.resultado_path_loss)-np.max(self.tx_grel)-self.cfg_bal["grx"]+self.cfg_bal["ltx"]+self.cfg_bal["lrx"]
		else:
			self.balance_simplificado=np.vstack(self.resultado_path_loss)-np.vstack(self.tx_grel)-self.cfg_bal["grx"]+self.cfg_bal["ltx"]+self.cfg_bal["lrx"]

		if self.cfg_prop["params_desv"]["display"]:
			if self.cfg_gen['debug']:
				print("[ok]-----configurar_desv. copia del balance.")

			self.balance_simplificado_antes=self.balance_simplificado.copy()

		if self.cfg_prop["params_desv"]["display"]:
			if self.cfg_prop["params_desv"]["tipo"]=="normal":
				mu=self.cfg_prop["params_desv"]["params"][2]
				sigma_xn=self.cfg_prop["params_desv"]["params"][1]
				self.desvanecimiento=np.random.normal(mu,sigma_xn,self.balance_simplificado.shape)
				self.balance_simplificado=self.balance_simplificado+np.vstack(self.desvanecimiento)
				if self.cfg_gen['debug']:
					print("[ok]-----configurar_desv,  normal")

			elif self.cfg_prop["params_desv"]["tipo"]=="rayl":
				if self.cfg_gen['debug']:
					print("[ok]-----configurar_desv, rayleight")
					#plt.plot(self.distancias, -self.balance_simplificado, 'r', label="sin desva, sin ptx")
				bal_simpl_desva=10**((self.cfg_bal["ptx"]-self.balance_simplificado)/10)
				bal_simpl_desva_r=np.sqrt(bal_simpl_desva)
				b=bal_simpl_desva_r/np.sqrt(np.pi/2)
				bray=np.random.rayleigh(b)
				bray=np.power(bray,2)
				self.desvanecimiento=10*np.log10(bray) #bray_dB
				self.balance_simplificado=-(self.desvanecimiento-self.cfg_bal["ptx"])

			elif self.cfg_prop["params_desv"]["tipo"]=="mixto":
				if self.cfg_gen['debug']:
					print("[ok]-----configurar_desv, MIXTO")
					#plt.plot(self.distancias, -self.balance_simplificado, 'r-',  label="sin ptx, simplificado")
				mu=self.cfg_prop["params_desv"]["params"][2]
				sigma_xn=self.cfg_prop["params_desv"]["params"][1]
				#if true, el desvanecimiento deja de ser 0 y se integra a las perdidas.
				#print("bal sim\n",self.balance_simplificado)
				self.desvanecimiento=np.random.normal(mu,sigma_xn,self.balance_simplificado.copy().shape)
				self.balance_simplificado=self.balance_simplificado.copy()+np.vstack(self.desvanecimiento)
				#print("CUSTOM3\n", self.desvanecimiento)
				#print("CUSTOM4\n",self.balance_simplificado)
				#rayleigh
				#correccion de signos desvanecimiento
				bal_simpl_desva=10**((self.cfg_bal["ptx"]-self.balance_simplificado)/10)
				bal_simpl_desva_r=np.sqrt(bal_simpl_desva)
				b=bal_simpl_desva_r/np.sqrt(np.pi/2)
				bray=np.random.rayleigh(b)
				bray=np.power(bray,2)
				self.desvanecimiento=10*np.log10(bray) #bray_dB
				print("CUSTOm5\n", self.desvanecimiento[:10])
				self.balance_simplificado=-(self.desvanecimiento-self.cfg_bal["ptx"])
		else:
			pass


	def inicializar_tipo(self):
		'''Segun el modelo de propagacion escogido, inicizalizar selecciona la funcion que calcula las perdidas.
		Por defecto, los parametros de la webUI se obtienen en metros y megahertz.'''

		if self.cfg_prop["modelo_perdidas"]=="espacio_libre":
			#km, GH
			if self.arreglos[0][1]=="m":
				#convierto a kilometros
				if self.custom_dist_flag==True:
					self.distancias=np.vstack(self.custom_dist)
				else:
					self.distancias=self.arreglos[0][0]/1000


			else:
				pass #opcion kilometro, no cambia.

			if self.cfg_gen["portadora"][1]=="mhz":
				#convierto a gigaherz
				self.portadora=self.cfg_gen["portadora"][0]/1000
			else:
				pass #opcion gigahez, no cambia.
			self.perdidas_espacio_libre_ghz()



		elif self.cfg_prop["modelo_perdidas"] =="okumura_hata":
			#km, mhz
			if self.arreglos[0][1]=="m":
				#convierto a kilometros
				if self.custom_dist_flag==True:
					self.distancias=np.vstack(self.custom_dist)
				else:
					self.distancias=self.arreglos[0][0]/1000
			else:
				pass #opcion kilometro, no cambia.
			
			if self.cfg_gen["portadora"][1]=="ghz":
				#convierto a megaherz, por la ecuacion, si ya esta en megaherz, pass
				self.portadora=self.cfg_gen["portadora"][0]*1000
			else:
				pass #opcion megaherz, no cambia.

			self.perdidas_okumura_hata_mhz()

		elif self.cfg_prop["modelo_perdidas"] =="umi_ci":
			#m, Ghz
			if self.arreglos[0][1]=="m":

				#las distancias debe estar en [m], por eso no cambia
				if self.custom_dist_flag==True:
					self.distancias=np.vstack(self.custom_dist)
					
				else:
					
					self.distancias=self.arreglos[0][0].copy()

			else:
				pass #opcion kilometro, no cambia.
			if self.cfg_gen["portadora"][1]=="ghz":
				#convierto a megaherz, por la ecuacion, si ya esta en megaherz, pass
				#self.portadora=self.cfg_gen["portadora"][0]*1000
				self.portadora=self.cfg_gen["portadora"][0]
			else:
				#pass #opcion megaherz, cambia a Ghz
				self.portadora=self.cfg_gen["portadora"][0]/1000
			self.perdidas_umi_ci()

		elif self.cfg_prop["modelo_perdidas"] =="umi_abg":
			#m, Ghz
			if self.arreglos[0][1]=="m":

				if self.custom_dist_flag==True:
					self.distancias=np.vstack(self.custom_dist)
					
				else:
					#las distancias debe estar en [m], no cambia.
					self.distancias=self.arreglos[0][0]

			else:
				pass #opcion kilometro, no cambia.
			if self.cfg_gen["portadora"][1]=="ghz":
				self.portadora=self.cfg_gen["portadora"][0]
			else:
				#pass #opcion megaherz, cambia a Ghz
				self.portadora=self.cfg_gen["portadora"][0]/1000
			self.perdidas_umi_abg()
			
		elif self.cfg_prop["modelo_perdidas"] =="uma_3gpp":
			#km, mhz
			#m, Ghz
			
			if self.arreglos[0][1]=="m":

				if self.custom_dist_flag==True:
					self.distancias=np.vstack(self.custom_dist)
				else:
					#las distancias debe estar en [m]
					self.distancias=self.arreglos[0][0]

			else:
				pass #opcion kilometro, no cambia.
			if self.cfg_gen["portadora"][1]=="ghz":
				#convierto a megaherz, por la ecuacion, si ya esta en megaherz, pass
				self.portadora=self.cfg_gen["portadora"][0]
			else:
				#pass #opcion megaherz, no cambia.
				self.portadora=self.cfg_gen["portadora"][0]/1000

			self.perdidas_uma_3gpp()
		else:
			pass


	def perdidas_espacio_libre_ghz(self):
		#outs dB
		'''Funcion que calcula las perdidas de espacio libre en dB'''
		self.resultado_path_loss=92.4+20*np.log10(self.portadora)+20*np.log10(self.distancias)


	def perdidas_okumura_hata_mhz(self):
		#outs dB
		#http://catarina.udlap.mx/u_dl_a/tales/documentos/lem/soriano_m_jc/capitulo2.pdf
		'''Funcion que calcula las perdidasd de espacio con el modelo hata 1980.
		Fuente:Empirical Formula for Propagation Loss in Land Mobile Radio Services'''
		#rangos
		#fc:150,1500 MHz
		#hb=30,200 m
		#R:1, 200 km #no es el radio, es la distancia.
		#hb=30 #m
		#alfa=0
		#hm=1.5
		hb=self.cfg_prop["params_modelo"][0]#hbs=25
		#alfa=self.cfg_prop["params_modelo"][1] #0 si hm=1.5m
		hm=self.cfg_prop["params_modelo"][2]

		#de la forma: Lp=A+Blog10(R)

		A=69.55+(26.16*np.log10(self.portadora))-13.82*np.log10(hb)
		B=44.9-6.55*np.log10(hb)
		E=3.2*(np.log10(11.75*hm))**2-4.97 #[dB] para ciudades grandes y fc>300 MHz
		#E=8.29*(np.log10(1.54*hm))**2 -1.1 #[dB] para ciudades grandes y fc<300 MHz
		#se guarda en un valor aparte, no es necesario, pero sirve de debug.

		if self.cfg_prop["params_desv"]["display"]:
			#print("\n\n!!!!!!!!!!!!!desvanecimiento.dist\n\n",self.distancias)
			self.resultado_path_loss_antes=A+B*np.log10(self.distancias)-E
		#print("\n\n!!!!!!!!!!!!!desvanecimiento.dist2\n\n",self.distancias)
		self.resultado_path_loss=A+(B*np.log10(self.distancias))-E #+ self.desvanecimiento


	def perdidas_umi_ci(self):
		'''Este modulo recrea las perdidas con distancia [m] frecuencia [GHz] con los parametros alpha_n: 3.1 y con Sigma_Xn:8.1 dB
		considerados por la documentacion valores en dB para sigma y veces para alpha_n
		***articulo Simulation path loss Propagation Path Loss models for 5G urban micro and macro-cellular Scenarios
		-rango de frecuencias debajo de 30GHz'''
		alpha_n=self.cfg_prop["params_desv"]["params"][0]#valor de alpha n para el parametro CI 
		#este parametro es de valor 3.1 fijo y tomado de https://ieeexplore.ieee.org/document/7504435
		sigma_xn=self.cfg_prop["params_desv"]["params"][1]#es la desviacion estandar que presenta la curva perdidas
		# y es un valor aleatorio, con una distribucion gausiana de media SIGMA_XN
		hbs=self.cfg_prop["params_modelo"][0]
		hut=self.cfg_prop["params_modelo"][2]
		sigma_xn=8.1
		alpha_n=3.1

		dist_3d=np.sqrt(self.distancias**2 +(hbs-hut)**2)
		correcion_freq_ghz=32.44+20*math.log10(self.portadora)
		correccion_dist_m=10*alpha_n*np.log10(dist_3d)

		#print("distancias ci modelo canal\n",np.vstack(self.distancias))
		self.resultado_path_loss=correcion_freq_ghz+correccion_dist_m
		#print("resultado path loss\n",self.resultado_path_loss)


	def perdidas_umi_abg(self):
		'''Este modulo recrea las perdidas con distacia [m] frecuencia [GHz] con los parametros alpha_n: 3.5 gamma : 1.9 (veces)
		-consideramos alpha y gamma como la dependencia de las perdidas en  relacion a la distancia y la frecuencia
		-Beta es un factor de correccion o compensacion de optimizacion en [dB],
		-sigma_Xn[dB]:8.0 desviacion estandar.
		***articulo Propagation Path Loss Models for 5G Urban Micro- and Macro-Cellular Scenarios✮
		-rango de frecuencias debajo de 30GHz'''
		alpha_n=self.cfg_prop["params_modelo"][0]
		beta=self.cfg_prop["params_modelo"][1]
		gamma=self.cfg_prop["params_modelo"][2]
		sigma_xn=self.cfg_prop["params_modelo"][3]
		hbs=self.cfg_prop["params_modelo"][0]
		hut=self.cfg_prop["params_modelo"][2]

		alpha_n=3.1
		beta=24.4
		gamma=1.9
		sigma_xn=8.0


		dist_3d=np.sqrt(self.distancias**2 +(hbs-hut)**2)
		correccion_freq_ghz=(10*gamma*math.log10(self.portadora))
		correcion_dist_m=(10*alpha_n*np.log10(dist_3d))
		self.resultado_path_loss=correccion_freq_ghz+correcion_dist_m+beta
	

	def evaluar_pl1(self, dist_3d ):
		'''evalua que funcion debe seleccionar dependiendo el parametro de entrada.'''
		#fc debe estar en Ghz, por eso FC/1000
		path_l=28.0+22*np.log10(dist_3d)+20*np.log10(self.portadora)
		return path_l

	def evaluar_pl2(self,dist_3d, bp_p, hbs, hut):
		#fc debe estar en Ghz, por eso FC/1000
		'''evalua que funcion debe seleccionar dependiendo el parametro de entrada.
		bp_p breakpoint prima.'''
		path_l=28+40*np.log10(dist_3d)+20*np.log10(self.portadora)-9*np.log10((bp_p**2)+(hbs-hut)**2)
		return path_l
	
	def evaular_pl0(distancias, bp):
		'''para el caso en que la distncia sea menor a 10 o mayor a 5000k. Este caso normalmente no se da por la restricccion en distancia que se ha fijado al principio de la funcion orignal.'''
		path_l=32.4+20*np.log10(self.portadora)+20*np.log10(dist_3d)
		return path_l

	def perdidas_uma_3gpp(self):
		'''Este modulo recrea las perdidas UMA LOS de la TR 138901, con distancia [m] y frecuencia FC en [Hz].
		De acuerdo con la fuente: https://www.etsi.org/deliver/etsi_tr/138900_138999/138901/15.00.00_60/tr_138901v150000p.pdf 
		
		La documentacion indica que HE es la altura relativa de la antena. Este parametro se define como HE=1m si hUT<13.
		El con prop[o]sito de ahorrar calculos, se define que la altura del terminal Hut<13 de tal modo que HE=1m.
		
		#variables necesarias

		#hbs (alturna de antena)  -> 25m
		#hut (altura de terminal) -> 1.5m <= hut <= 22.5
		#hbs_p (alturna de antena efectiva) 
		#hut_p (altura de terminal efectiva)
		#he (altura del ambiente) -> 1.0m
		#fc (frecuency carrier)   -> self.frecuency
		#dist_2d ------------------> self.distancias
		#VEL_C (velocidad de la luz 3.8*10**8)


		EL ESCENARIO NO PUEDE SER MAYOR A 5KM PARA LA DISTANCIA DEL USUARIO A LA ESTACION BASE.
		CUAL ES LA DISTANCIA MAXIMA ISD QUE SE PUEDE LOGRAR SIN SUPERAR ESTE LIMITE? 
		CUAL ES LA DISTNACIA MAXIMA ENTRE EL USUARIO BORDE Y LA BS DE LA CELDA MAS ALEJADA, EXTREMO A EXTREMO?
		'''
		hbs=self.cfg_prop["params_modelo"][0]
		hut=self.cfg_prop["params_modelo"][2]

		#0. calcular la distancia 3d
		
		#1. calcular la distancia 2d
		'''la distancia 2d es la misma variable self.distancia'''
		#2. calcular la distancia bp (breakpoint)
		#dist_breakpoint=4*hbs_p*hut_p*fc/VEL_C
		#2.1 calular la distncias primas
		#he=1 por defecto.
		he=1
		hbs_p=hbs-he
		hut_p=hut-he
		#portadora esta en MHz, la necesitamos en HZ de acuerdo a la documentacion.
		dist_breakpoint_prima=4*hbs_p*hut_p*((self.portadora*10)/3)#portadora en GHz
		#3. evaular PLuma_los (tr138901)
		'''evaluar para cada distancia de la siguiente manera
		PL1 si 10m < self.distancias < dist_breakpoint.
		PL2 si distancia_breakpoin < self.distnacias <= 5000m.
		
		Que sucede si es menor a 10?
		Se limpian los datos.
		Todos los valores menores a 10m, se dejan fijo en 10.
		Todos los valores mayores a 5000m se dejan fijo en 5000m
		Donde sebe hacerse este cambio con anterioridad para que no afecte los demas calculos?'''

		self.distancias=np.where(self.distancias<10, 10,self.distancias)
		self.distancias=np.where(self.distancias>5000, 5000,self.distancias)

		'''encontramos los indices donde 1 pl1 y 2 pl2'''
		map_pl1=np.where((10 <= self.distancias) & (self.distancias <= dist_breakpoint_prima), 1, self.distancias)
		#map_pl2=np.where((dist_breakpoint <= self.distancias) & (self.distancias <= 5000), 2, 0)
		#map_pl2 toma la referncia de map_pl1 y modifica sus valores.
		map_pl2=np.where((dist_breakpoint_prima <= map_pl1) & (map_pl1 <= 5000), 2, map_pl1)
		#convertir de 2D a 3D antes de generar las perdidas
		dist_3d=np.sqrt(self.distancias**2 +(hbs-hut)**2)
		referencia=np.where(map_pl2==1, self.evaluar_pl1(dist_3d), map_pl2)
		referencia=np.where(map_pl2==2, self.evaluar_pl2(dist_3d, dist_breakpoint_prima, hbs, hut), referencia)
		self.resultado_path_loss=referencia



	def balance_del_enlace_mcl(self):
		'''Funcion que calcula un balance del enlace, teniendo en cuenta el mcl.
		RX_PWR = TX_PWR – Max (pathloss – G_TX – G_RX, MCL)
		where:
		RX_PWR is the received signal power
		TX_PWR is the transmitted signal power
		G_TX is the transmitter antenna gain
		G_RX is the receiver antenna gain
		---
		Una ecuación de balance de enlace que incluye todos estos efectos, expresado de forma logarítmica,
		podría tener este aspecto:

		  P_ {RX} = P_ {TX} + G_ {TX} - L_ {TX} - L_ {FS} - L_M + G_ {RX} - L_ {RX} \,

		dónde:

		P_ {RX} = Potencia recibida (dBm)
		P_ {TX} = Potencia de salida del transmisor (dBm)
		G_ {TX}= Transmisor de ganancia de la antena (dBi)
		L_ {TX} = pérdidas transmisor (coaxiales, conectores, ...) (dB)
		L_ {FS}= Pérdida de trayecto , por lo general la pérdida de espacio libre (dB)
		L_M = Pérdidas diversas ( desvanecimiento margen, la pérdida del cuerpo, desadaptación de polarización, otras pérdidas ...) (dB)
		G_ {RX}= Receptor de ganancia de la antena (dBi)
		L_ {RX} = pérdidas receptor (coaxial, conectores, ...) (dB) '''
		#mcl=70 #dB para entorno urbano.
		#segmento_tx=self.tx_grel-self.tx_loss
		#segmento_rx=self.rx_g-self.rx_loss
		#self.resultado_balance=segmento_tx+segmento_rx-self.resultado_path_loss
		self.configurar_desvanecimiento()
		#print("CUSTOM7,\n",self.balance_simplificado.copy()[:10])
		self.resultado_balance=self.cfg_bal["ptx"]-np.maximum(self.balance_simplificado.copy(), self.cfg_bal["mcl"])
		#self.resultado_margen=self.resultado_balance-self.cfg_bal["sensibilidad"]



	def balance_del_enlace_simple(self):
		'''DEPLETED
		Funcion que calcula un balance del enlace sencillo:
		Potencia recibida ( dB ) = potencia transmitida (dB) + Ganancias (dB) - Pérdidas (dB)'''
		#segemento=ptx-perdidas+ganancia
		#ATENCION, DOCUMENTAR UNIDADES
		#"espacio_libre", pot_tx,loss_tx, gan_tx, gan_rx, loss_rx,sensibilidad
		#params_perdidas[0]:tipo de perdidas
		#params_perdidas[1]:potencia de tx
		#params_perdidas[2]:perdidas en tx

		#params_perdidas[3]:ganancia en tx

		#params_perdidas[4]:ganancia en rx
		#params_perdidas[5]:perdidas en rx
		#params_perdidas[6]:sensibilidad de todos los usuarios #en el futuro, sensibidad variable
		##segmento_tx=self.params_perdidas[1]-self.params_perdidas[2]+self.params_perdidas[3]
		##segmento_rx=self.params_perdidas[4]-self.params_perdidas[5]
		##self.resultado_balance=segmento_tx-self.resultado_path_loss+segmento_rx

		##self.resultado_margen=self.resultado_balance+self.params_perdidas[6]

		segmento_tx=self.tx_prw+self.tx_grel-self.tx_loss
		segmento_rx=self.rx_g-self.rx_loss
		self.resultado_balance=segmento_tx+segmento_rx-self.resultado_path_loss
		self.resultado_margen=self.resultado_balance-self.rx_sens




	def balance_del_enlace_LTE(self):
		'''Funcion que calcula el balance del enlace 5G/4G.
		Fuente:http://www.techplayon.com/5g-network-rf-planning-link-budget-basics/
		Received Signal Level at receiver (dBm) =
		gNodeB transmit power (dBm) – 10*log10 (subcarrier quantity) + gNodeB antenna gain (dBi)
		– gNodeB cable loss (dB) – Path loss (dB) – penetration loss (dB) – foliage loss (dB)
		– body block loss (dB) – interference margin (dB) – rain/ice margin (dB)
		– slow fading margin (dB) – body block loss (dB) + UE antenna gain (dB)
		'''

		self.resultado_balance=0

	def balance_del_enlace_5G(self):
		'''Funcion que calcula el balance del enlace 5G/4G.
		Fuente:http://www.techplayon.com/5g-network-rf-planning-link-budget-basics/
		Received Signal Level at receiver (dBm) =
		gNodeB transmit power (dBm) – 10*log10 (subcarrier quantity) + gNodeB antenna gain (dBi)
		– gNodeB cable loss (dB) – Path loss (dB) – penetration loss (dB) – foliage loss (dB)
		– body block loss (dB) – interference margin (dB) – rain/ice margin (dB)
		– slow fading margin (dB) – body block loss (dB) + UE antenna gain (dB)
		'''

		self.resultado_balance=0

	def balance_del_enlace_UMa(self):
		#mismo que el de 5G
		pass

	def balance_del_enlace_UMi(self):
		#mismo que el de 5G
		pass

	def debug_ver_balance(self):
		'''Funcion para observar el balance del enlace. Solo funciona localmente.'''
		#self.desvanecimiento es negativo

		plt.xlabel('Distancia m')
		plt.ylabel('Perdidas [dB]')
		plt.title('Perdidas modelo: '+ self.cfg_prop["modelo_perdidas"]+', desva: '+self.cfg_prop["params_desv"]["tipo"])
		if self.cfg_prop["params_desv"]["tipo"]=='normal':
			plt.plot(self.distancias, -self.balance_simplificado, label="normal+sin ptx, simplificado")
		else:
			pass
		plt.plot(self.distancias, self.desvanecimiento, label="desva "+self.cfg_prop["params_desv"]["tipo"])
		plt.plot(self.distancias, self.resultado_balance,'bx-', label="mcl y ptx")
		plt.legend(loc="upper left")
		#en el plot es negativo por aquello de la ecuacion mcl.
	
	def ver_perdidas_local(self, nombre):
		'''Funcion para ver las perdidas por trayectoria'''
		#cambio a un array custom
		plt.figure()
		self.custom_dist_flag=True
		#EN KILOMETROS
		if self.cfg_prop["modelo_perdidas"]=="okumura_hata":
			self.custom_dist=np.arange(1,20,.3)
		elif self.cfg_prop["modelo_perdidas"]=="uma_3gpp":
			self.custom_dist=np.arange(1,999,1)
		elif self.cfg_prop["modelo_perdidas"]=="umi_ci":
			#metros
			self.custom_dist=np.arange(1,999,1)
		elif self.cfg_prop["modelo_perdidas"]=="umi_abg":
			self.custom_dist=np.arange(1,999,1)
		else:
			print("modelo_canal.py:UN ERROR OCURRIRA.")
		#realizo la simulacion con el array custom diferente.
		self.inicializar_tipo()
		#obtengo resutlados
		plt.plot(self.custom_dist, self.resultado_path_loss, label="Pérdidas")
		plt.legend(loc="upper left")
		plt.title("Pérdidas de Propagación: {}".format(self.cfg_prop["modelo_perdidas"]))
		plt.xlabel("Distancia [Km]")

		if self.cfg_prop["modelo_perdidas"]=="okumura_hata":
			plt.xlabel("Distancia [Km]")
		else:
			plt.xlabel("Distancia [m]")

		plt.ylabel("Pérdidas [dB]")
		plt.grid(True)
		ruta="simapp/static/simulador/base_datos/imagenes/presim/{}.png".format(nombre)
		plt.savefig(ruta)

	
	def ver_desvanecimiento_local(self, nombre):
		'''Funcion para ver las perdidas por trayectoria'''
		#cambio a un array custom
		plt.figure()
		self.custom_dist_flag=True
		#EN KILOMETROS
		if self.cfg_prop["modelo_perdidas"]=="okumura_hata":
			self.custom_dist=np.arange(1,20,.3)
		elif self.cfg_prop["modelo_perdidas"]=="uma_3gpp":
			self.custom_dist=np.arange(1,999,1)
		elif self.cfg_prop["modelo_perdidas"]=="umi_ci":
			#metros
			self.custom_dist=np.arange(1,999,1)
		elif self.cfg_prop["modelo_perdidas"]=="umi_abg":
			self.custom_dist=np.arange(1,999,1)
		else:
			print("modelo_canal.py:UN ERROR OCURRIRA.")
		#realizo la simulacion con el array custom diferente.
		self.inicializar_tipo()
		self.balance_del_enlace_mcl()
		plt.grid(True)
		#obtengo resutlados


		fix_recta=np.zeros(len(self.custom_dist))
		plt.plot(self.custom_dist, self.desvanecimiento, "*-", label="desvanecimiento")
		plt.plot(self.custom_dist, fix_recta, "b-")
		plt.legend(loc="lower right")

		#si rayl-mixto, no sumar
		#label="normal+sin ptx, simplificado"
		plt.title("Desvanecimiento: {}".format(self.cfg_prop["params_desv"]["tipo"]))
		plt.xlabel("Distancia [Km]")
		plt.ylabel("Potencia Recibida [dBm]")
		ruta="simapp/static/simulador/base_datos/imagenes/presim/{}.png".format(nombre)
		plt.savefig(ruta)


	
	def ver_balance_local(self, nombre):
		'''Funcion para ver las perdidas por trayectoria'''
		#cambio a un array custom
		plt.figure()
		self.custom_dist_flag=True
		#EN KILOMETROS
		if self.cfg_prop["modelo_perdidas"]=="okumura_hata":
			self.custom_dist=np.arange(1,20,.3)
		elif self.cfg_prop["modelo_perdidas"]=="uma_3gpp":
			self.custom_dist=np.arange(1,999,1)
		elif self.cfg_prop["modelo_perdidas"]=="umi_ci":
			#metros
			self.custom_dist=np.arange(1,999,1)
		elif self.cfg_prop["modelo_perdidas"]=="umi_abg":
			self.custom_dist=np.arange(1,999,1)
		else:
			print("modelo_canal.py:UN ERROR OCURRIRA.")
		#realizo la simulacion con el array custom diferente.
		self.inicializar_tipo()
		self.balance_del_enlace_mcl()
		plt.grid(True)
		#obtengo resutlados
		#negativo por que aun no tiene en cuenta el mcl
		plt.plot(self.custom_dist, -self.balance_simplificado_antes,  label="balance antes")
		#plt.plot(self.custom_dist, self.balance_simplificado, label="balance después")
		plt.plot(self.custom_dist, -self.balance_simplificado, label="balance después *-1")
		#positivo por que tiene encuenta el mcl.
		plt.plot(self.custom_dist, self.resultado_balance, label="balance final")
		plt.legend(loc="lower right")

		#si rayl-mixto, no sumar
		#label="normal+sin ptx, simplificado"
		plt.title("Desvanecimiento: {}".format(self.cfg_prop["params_desv"]["tipo"]))
		plt.xlabel("Distancia [Km]")
		plt.ylabel("Potencia Recibida [dBm]")
		ruta="simapp/static/simulador/base_datos/imagenes/presim/{}.png".format(nombre)
		plt.savefig(ruta)
	
	#ADICIONAR02
	def ver_balance_sin_local(self, nombre):
		'''Funcion para ver las perdidas por trayectoria'''
		#cambio a un array custom
		plt.figure()
		self.custom_dist_flag=True
		#EN KILOMETROS
		if self.cfg_prop["modelo_perdidas"]=="okumura_hata":
			self.custom_dist=np.arange(1,20,.3)
		elif self.cfg_prop["modelo_perdidas"]=="uma_3gpp":
			self.custom_dist=np.arange(1,999,1)
		elif self.cfg_prop["modelo_perdidas"]=="umi_ci":
			#metros
			self.custom_dist=np.arange(1,999,1)
		elif self.cfg_prop["modelo_perdidas"]=="umi_abg":
			self.custom_dist=np.arange(1,999,1)
		else:
			print("modelo_canal.py:UN ERROR OCURRIRA.")
		#realizo la simulacion con el array custom diferente.
		self.inicializar_tipo()
		self.balance_del_enlace_mcl()
		plt.grid(True)
		#obtengo resutlados
		plt.plot(self.custom_dist, self.resultado_balance, label="balance final")
		plt.legend(loc="lower right")
		plt.title("Desvanecimiento: {}".format(self.cfg_prop["params_desv"]["tipo"]))
		plt.xlabel("Distancia [Km]")
		plt.ylabel("Potencia Recibida [dBm]")
		ruta="simapp/static/simulador/base_datos/imagenes/presim/{}.png".format(nombre)
		plt.savefig(ruta)

	
	def ver_relaciones_local(self, nombre):
		'''Funcion para ver las perdidas por trayectoria'''
		#cambio a un array custom
		plt.figure()
		self.custom_dist_flag=True
		#EN KILOMETROS
		if self.cfg_prop["modelo_perdidas"]=="okumura_hata":
			self.custom_dist=np.arange(1,20,.3)
		elif self.cfg_prop["modelo_perdidas"]=="uma_3gpp":
			self.custom_dist=np.arange(1,999,1)
		elif self.cfg_prop["modelo_perdidas"]=="umi_ci":
			#metros
			self.custom_dist=np.arange(1,999,1)
		elif self.cfg_prop["modelo_perdidas"]=="umi_abg":
			self.custom_dist=np.arange(1,999,1)
		else:
			print("modelo_canal.py:UN ERROR OCURRIRA.")
		#realizo la simulacion con el array custom diferente.
		self.inicializar_tipo()
		self.balance_del_enlace_mcl()
		plt.grid(True)
		#obtengo resutlados
		plt.plot(self.custom_dist, self.resultado_path_loss, label="pérdidas")

		fix_recta=np.zeros(len(self.custom_dist))
		plt.plot(self.custom_dist, self.desvanecimiento, "*-", label="desvanecimiento")
		plt.plot(self.custom_dist, fix_recta, "b-")

		#negativo por que aun no tiene en cuenta el mcl
		plt.plot(self.custom_dist, -self.balance_simplificado_antes,  label="balance antes")
		plt.plot(self.custom_dist, self.balance_simplificado, label="balance después")
		plt.plot(self.custom_dist, -self.balance_simplificado, label="balance después *-1")
		plt.plot(self.custom_dist, self.resultado_balance, label="balance final")
		plt.legend(loc="lower right")

		#si rayl-mixto, no sumar
		#label="normal+sin ptx, simplificado"
		plt.title("Desvanecimiento: {}".format(self.cfg_prop["params_desv"]["tipo"]))
		plt.xlabel("Distancia [km]")
		plt.ylabel("Potencia Recibida [dBm]")
		ruta="simapp/static/simulador/base_datos/imagenes/presim/{}.png".format(nombre)
		plt.savefig(ruta)





def prueba_interna_resultado_path_loss():
	#obsoleta
	'''Funcion que prueba el concepto de perdidas de espacio libre con numpy'''
	freq=10 #en gigas
	distancias_km=np.array([0.1, 1, 2, 3, 4, 5, 6])
	modelo_simple=Modelo_Canal(freq, distancias_km)
	modelo_simple.perdidas_espacio_libre_ghz()
	l_bs=modelo_simple.resultado_path_loss
	print(l_bs)

def prueba_interna_desvanecimiento_normal():
	'''Funcion que prueba el concepto de tipos desvanecimiento con numpy'''
	#params sim
	freq=44000 #gigas?
	distancias=np.arange(1,200,1)

	#params perdidas
	params_modelo=[30, 0, 1.5] #hb, alfa, hm
	modelo=['modelo_ci',params_modelo] #si no: se pone, se escribe o se escribe bien, el pathloss es 0
	pot_tx=44 #18 #dBm
	loss_tx=1
	gan_tx=15
	gan_rx=1
	loss_rx=0
	sensibilidad=-92 #dBm
	##
	params_p=[modelo, pot_tx,loss_tx, gan_tx, gan_rx, loss_rx,sensibilidad]
	#
	params_sim=[(freq,"mhz"),(distancias, "m")]
	#
	#params desv
	tipo_desv='none'
	alpha_n=3.1
	sigma_xn=4
	mu=0
	play_desv=False
	params_desv=[play_desv, tipo_desv, [alpha_n, sigma_xn, mu]]

	modelo_simple=Modelo_Canal(params_p, params_sim, params_desv)
	#LA PREGUNTA ES AQUI, CON LOS anteriores DEBERIA ARROJAR HATA, PERO ESTA REALIZANDO libre_ghz.... Corregido
	#modelo_simple.perdidas_espacio_libre_ghz()
	#path_loss=modelo_simple.resultado_path_loss
	balance=modelo_simple.resultado_balance
	#desvanecimiento normal
	#distancias_np=np.array([[10,50,100],[130, 170, 200]])

	#sized=len(distancias)
	N=np.random.normal(mu,sigma_xn,distancias.shape)
	balance_desv=balance+N
	plt.grid(True)
	plt.xlabel('Distancia m')
	plt.ylabel('Perdidas [dB]')
	plt.title('Perdidas modelo: '+ modelo[0])
	#plt.plot(distancias,path_loss,'b*')
	plt.plot(distancias,balance,'bx')
	plt.plot(distancias,balance_desv,'go-')
	plt.show()

def prueba_interna_desvanecimiento_prof():
	'''Funcion que prueba el concepto de tipos desvanecimiento con numpy'''
	#params sim
	freq=44000 #gigas?
	distancias=np.arange(1,200,0.2)

	#params perdidas
	params_modelo=[20, 0, 1.5] #hb, alfa, hm
	modelo=['modelo_ci',params_modelo] #si no: se pone, se escribe o se escribe bien, el pathloss es 0
	pot_tx=44 #18 #dBm
	loss_tx=1
	gan_tx=15
	gan_rx=1
	loss_rx=0
	sensibilidad=-92 #dBm
	##
	params_p=[modelo, pot_tx,loss_tx, gan_tx, gan_rx, loss_rx,sensibilidad]
	#
	params_sim=[(freq,"mhz"),(distancias, "m")]
	#
	#params desv
	tipo_desv='none' #normal, rayl, mixto=normal+rayl
	alpha_n=3.1
	sigma_xn=8
	mu=0
	play_desv=False
	params_desv=[play_desv, tipo_desv,[alpha_n, sigma_xn, mu]]
	modelo_simple=Modelo_Canal(params_p, params_sim, params_desv)
	#LA PREGUNTA ES AQUI, CON LOS anteriores DEBERIA ARROJAR HATA, PERO ESTA REALIZANDO libre_ghz.... Corregido
	#modelo_simple.perdidas_espacio_libre_ghz()
	#path_loss=modelo_simple.resultado_path_loss
	balance=modelo_simple.resultado_balance
	modelo_simple.debug_ver_balance()
	plt.grid(True)

	plt.show()


if __name__=="__main__":
	#Prototipo:
	#import #aqui van los submodulos nuevamente para envitar errores

	#prueba interna 1.
	#prueba_interna_resultado_path_loss()
	prueba_interna_desvanecimiento_normal() #se observa unos puntos planos al principo del array, se debe al mcl.
	#prueba_interna_desvanecimiento_prof()
	
else:
	print("Modulo Importado: [", os.path.basename(__file__), "]")
