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
		self.custom_dist=0

		self.tx_grel=self.arreglos[1] #en cero estan los valore,s en 1 estan las unidades.

		self.resultado_path_loss_antes=0 #eliminar, dejar solo en debug.
		self.desvanecimiento=0
		self.balance_simplificado_antes=0
		self.balance_simplificado=0

		#SALIDA
		self.resultado_path_loss=0
		self.resultado_balance=0
		self.resultado_margen=0

		self.resultado_balance_v=0

		#aplica desvanecimiento si aplica.
		self.inicializar_tipo()
		#se altera el orden para poder obtener los valores de perdidas, en el
		#desvanecimiento rayleight, y luego, adicionar ese desvanecimiento al balance del enlace
		#self.configurar_desvanecimiento()
		self.balance_del_enlace_mcl() #f(configurar_desvanecimiento())
		#self.inicializar_balance()

	def configurar_desvanecimiento(self):
		'''Crea un array de desvanecimiento, dependiendo del tipo y especificaciones extras'''

		if self.custom_dist_flag:
			self.balance_simplificado=self.resultado_path_loss-np.max(self.tx_grel)-self.cfg_bal["grx"]+self.cfg_bal["ltx"]+self.cfg_bal["lrx"]
		else:
			self.balance_simplificado=self.resultado_path_loss-self.tx_grel-self.cfg_bal["grx"]+self.cfg_bal["ltx"]+self.cfg_bal["lrx"]


		if self.cfg_prop["params_desv"]["display"]:
			if self.cfg_gen['debug']:
				print("[ok]-----configurar_desv. copia del balance.")

			self.balance_simplificado_antes=self.balance_simplificado.copy()

		if self.cfg_prop["params_desv"]["display"]:
			#print("[ok].debug: desvanecimiento activado.")
			if self.cfg_prop["params_desv"]["tipo"]=="normal":
				mu=self.cfg_prop["params_desv"]["params"][0]
				sigma_xn=self.cfg_prop["params_desv"]["params"][1]
				self.desvanecimiento=np.random.normal(mu,sigma_xn,self.distancias.shape)
				self.balance_simplificado=self.balance_simplificado+self.desvanecimiento*-1
				if self.cfg_gen['debug']:
					print("[ok]-----configurar_desv,  normal")
					#DESCOMENTAR SOLO EN DEBUG Y CUANDO SE EJECUTE ESTE MODULO LOCALMENTE.
					#plt.plot(self.distancias, -self.balance_simplificado, 'r-',  label="sin ptx, simplificado")

			elif self.cfg_prop["params_desv"]["tipo"]=="rayl":
				if self.cfg_gen['debug']:
					print("[ok]-----configurar_desv, rayleight")
					#plt.plot(self.distancias, -self.balance_simplificado, 'r', label="sin desva, sin ptx")
				bal_simpl_desva=10**(-self.balance_simplificado/10)
				bal_simpl_desva_r=np.sqrt(bal_simpl_desva)
				b=bal_simpl_desva_r/np.sqrt(np.pi/2)
				bray=np.random.rayleigh(b)
				bray=np.power(bray,2)
				self.desvanecimiento=10*np.log10(bray) #bray_dB
				self.balance_simplificado=-self.desvanecimiento

			elif self.cfg_prop["params_desv"]["tipo"]=="mixto":
				if self.cfg_gen['debug']:
					print("[ok]-----configurar_desv, MIXTO")
					#plt.plot(self.distancias, -self.balance_simplificado, 'r-',  label="sin ptx, simplificado")
				mu=self.cfg_prop["params_desv"]["params"][0]
				sigma_xn=self.cfg_prop["params_desv"]["params"][1]
				#if true, el desvanecimiento deja de ser 0 y se integra a las perdidas.
				self.desvanecimiento=np.random.normal(mu,sigma_xn,self.distancias.shape)
				self.balance_simplificado=self.balance_simplificado+self.desvanecimiento
				#rayleigh
				#correccion de signos desvanecimiento
				bal_simpl_desva=10**(-self.balance_simplificado/10)
				bal_simpl_desva_r=np.sqrt(bal_simpl_desva)
				b=bal_simpl_desva_r/np.sqrt(np.pi/2)
				bray=np.random.rayleigh(b)
				bray=np.power(bray,2)
				self.desvanecimiento=10*np.log10(bray) #bray_dB
				self.balance_simplificado=-self.desvanecimiento
		else:
			#print("[ok].debug:balance simplificado no cambia.")
			pass


	def inicializar_tipo(self):
		'''Segun el modelo de propagacion escogido, inicizalizar selecciona la funcion que calcula las perdidas'''

		if self.cfg_prop["modelo_perdidas"]=="espacio_libre":
			#km, GH
			if self.arreglos[0][1]=="m":
				#convierto a kilometros
				if self.custom_dist_flag==True:
					self.distancias=self.custom_dist
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
				#self.hiper_arreglos[0]=(self.hiperc_distancias, "m") #siempre en metros.
				#self.hiper_arreglos[1]=(self.hiperc_ganancia_relativa, "none")
				#convierto a kilometros
				if self.custom_dist_flag==True:
					self.distancias=self.custom_dist
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
			#km, mhz
			#print("[debug]:mod_canal:umi_ci")
			if self.arreglos[0][1]=="m":
				#self.hiper_arreglos[0]=(self.hiperc_distancias, "m") #siempre en metros.
				#self.hiper_arreglos[1]=(self.hiperc_ganancia_relativa, "none")
				#convierto a kilometros

				#ADICIONAR01
				if self.custom_dist_flag==True:
					self.distancias=self.custom_dist
				else:
					self.distancias=self.arreglos[0][0]/1000

			else:
				pass #opcion kilometro, no cambia.
			if self.cfg_gen["portadora"][1]=="ghz":
				#convierto a megaherz, por la ecuacion, si ya esta en megaherz, pass
				self.portadora=self.cfg_gen["portadora"][0]*1000
			else:
				pass #opcion megaherz, no cambia.
			#print(self.distancias.shape)
			self.perdidas_umi_ci()

		elif self.cfg_prop["modelo_perdidas"] =="umi_abg":
			#km, mhz
			print("[debug]:mod_perd:umi_abg")
			if self.arreglos[0][1]=="m":
				#self.hiper_arreglos[0]=(self.hiperc_distancias, "m") #siempre en metros.
				#self.hiper_arreglos[1]=(self.hiperc_ganancia_relativa, "none")
				#convierto a kilometros

				#ADICIONAR01
				if self.custom_dist_flag==True:
					self.distancias=self.custom_dist
				else:
					self.distancias=self.arreglos[0][0]/1000

			else:
				pass #opcion kilometro, no cambia.
			if self.cfg_gen["portadora"][1]=="ghz":
				#convierto a megaherz, por la ecuacion, si ya esta en megaherz, pass
				self.portadora=self.cfg_gen["portadora"][0]*1000
			else:
				pass #opcion megaherz, no cambia.
			#print(self.distancias.shape)
			self.perdidas_umi_abg()
			
		elif self.cfg_prop["modelo_perdidas"] =="uma_3gpp":
			#km, mhz
			if self.arreglos[0][1]=="m":
				#self.hiper_arreglos[0]=(self.hiperc_distancias, "m") #siempre en metros.
				#self.hiper_arreglos[1]=(self.hiperc_ganancia_relativa, "none")
				#convierto a kilometros

				#ADICIONAR01
				if self.custom_dist_flag==True:
					self.distancias=self.custom_dist
				else:
					self.distancias=self.arreglos[0][0]/1000

			else:
				pass #opcion kilometro, no cambia.
			if self.cfg_gen["portadora"][1]=="ghz":
				#convierto a megaherz, por la ecuacion, si ya esta en megaherz, pass
				self.portadora=self.cfg_gen["portadora"][0]*1000
			else:
				pass #opcion megaherz, no cambia.
			#print(self.distancias.shape)
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
		hb=self.cfg_prop["params_modelo"][0]
		alfa=self.cfg_prop["params_modelo"][1] #0 si hm=1.5m
		hm=self.cfg_prop["params_modelo"][2]

		#de la forma: Lp=A+Blog10(R)

		A=69.55+(26.16*np.log10(self.portadora))-13.82*np.log10(hb)-alfa*(hm)
		B=44.9-6.55*np.log10(hb)
		E=3.2*(np.log10(11.75*hm))**2 -4.97 #[dB] para ciudades grandes y fc>300 MHz
		#E=8.29*(np.log10(1.54*hm))**2 -1.1 #[dB] para ciudades grandes y fc<300 MHz
		#print("okumura_hata, says->A,B:",A,B)
		#se guarda en un valor aparte, no es necesario, pero sirve de debug.
		print("---------------------------------->>>>>>>>>>>>>>>>>>>>\n", self.distancias)
		if self.cfg_prop["params_desv"]["display"]:
			self.resultado_path_loss_antes=A+B*np.log10(self.distancias)-E
		self.resultado_path_loss=A+(B*np.log10(self.distancias))-E #+ self.desvanecimiento


	def perdidas_umi_ci(self):
		'''Este modulo recrea las perdidas con distancia [m] frecuencia [GHz] con los parametros alpha_n: 3.1 y con Sigma_Xn:8.1 dB
		considerados por la documentacion valores en dB para sigma y veces para alpha_n
		***articulo Simulation path loss Propagation Path Loss models for 5G urban micro and macro-cellular Scenarios
		-rango de frecuencias debajo de 30GHz'''
		alpha_n=self.cfg_prop["params_modelo"][0]#valor de alpha n para el parametro CI 
		#este parametro es de valor 3.1 fijo y tomado de https://ieeexplore.ieee.org/document/7504435
		sigma_xn=self.cfg_prop["params_modelo"][1]#es la desviacion estandar que presenta la curva perdidas
		# y es un valor aleatorio, con una distribucion gausiana de media SIGMA_XN
		sigma_xn=8.1
		alpha_n=3.1
		correcion_freq_ghz=32.4+20*math.log10(self.portadora)
		correccion_dist_m=10*alpha_n*np.log10(self.distancias)
		self.resultado_path_loss=correcion_freq_ghz+correccion_dist_m+sigma_xn


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

		alpha_n=3.5
		beta=24.4
		gamma=1.9
		sigma_xn=8.0
		correccion_freq_ghz=(10*gamma*math.log10(self.portadora))
		correcion_dist_m=(10*alpha_n*np.log10(self.distancias))
		self.resultado_path_loss=correccion_freq_ghz+correcion_dist_m+beta+sigma_xn


	def parametro_uma_pl(self, dist ,dist_ref,dist_3d):
		'''Falta documentar, falta corregir variables locales y globales (self.dist?)'''
		if (dist <= dist_ref) and (dist>= 10):
			path_l=28.0+22*math.log10(dist_3d)+20*math.log10(self.portadora)
		elif self.dist>disbp and dist<=5000:
			path_l=13.54+39.08*math.log10(dist_3d)+20*math.log10(self.portadora)-0.6*(Hut-1.5)
		else:
			path_l=32.4+20*log10(self.portadora)+20*log10(10)
		return path_l


	def perdidas_uma_3gpp(self):
		'''Este modulo recrea las perdidas con distancia[m] y frecuencia[GHz] con los parametros
		-distancia breakpoint: 4(Hbs-He)*(Hut-He)*fc/C
		-rango de frecuencias para escenario UMa son por debajo de 6Ghz
		Fuente: https://www.etsi.org/deliver/etsi_tr/138900_138999/138901/15.00.00_60/tr_138901v150000p.pdf'''
		frecuencia_hz= self.portadora*math.pow(10,9)
		distancia_3d=np.sqrt(Hbs**2+self.distancias**2)
		dist_breakpoint=(4*(Hbs-He)*(Hut-He)*frecuencia_hz)/(3*math.pow(10, 8))
		dist_bp=np.array(np.ones_like(self.distancias)*dist_breakpoint)
		pl=[self.parametro_uma_pl(distancias,dist_ref,dist_3d) for distancias,dist_ref,dist_3d in zip(self.distancias,dist_bp,distancia_3d)]
		self.path_loss=np.array(pl)
	

	def evaluar_pl1(distancias, bp):
		'''evalua que funcion debe seleccionar dependiendo el parametro de entrada.'''
		path_l=28.0+22*math.log10(dist_3d)+20*math.log10(self.portadora)
		return path_l

	def evaluar_pl2(distancias, bp):
		'''evalua que funcion debe seleccionar dependiendo el parametro de entrada.'''
		path_l=13.54+39.08*math.log10(dist_3d)+20*math.log10(self.portadora)-0.6*(Hut-1.5)
		return path_l
	
	def evaular_pl0(distancias, bp):
		'''para el caso en que la distncia sea menor a 10 o mayor a 5000k'''
		path_l=32.4+20*log10(self.portadora)+20*log10(10)
		return path_l

	def perdidas_uma_refactor(self):
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
		dist_3d=np.sqrt(self.distancia**2 +(hbs-hut)**2)
		#1. calcular la distancia 2d
		'''la distancia 2d es la misma variable self.distancia'''
		#2. calcular la distancia bp (breakpoint)
		#dist_breakpoint=4*hbs_p*hut_p*fc/VEL_C
		#2.1 calular la distncias primas
		he=1
		hbs_p=hbs-he
		hut_p=hut-he
		dist_breakpoint=4*hbs_p*hut_p*(fc/3.8*10**8)
		#3. evaular PLuma_los (tr138901)
		'''evaluar para cada distancia de la siguiente manera
		PL1 si 10m < self.distancias < dist_breakpoint.
		PL2 si distancia_breakpoin < self.distnacias <= 5000m.
		
		Que sucede si es menor a 10?
		Se limpian los datos.
		Todos los valores menores a 10m, se dejan fijo en 10.
		Todos los valores mayores a 5000m se dejan fijo en 5000m
		Donde sebe hacerse este cambio con anterioridad para que no afecte los demas calculos?'''
		self.distancias=np.where(self.distancias<(10/1000), (10/1000),self.distancias)
		self.distancias=np.where(self.distancias>(5000/1000), (5000/1000),self.distancias)


		map_pl1=np.where((10 <= self.distancias) & (self.distancias <= dist_breakpoint), 1, self.distancias)
		'''si alimento nuevamente el array con el anterior, el ciclo se repite, es decir, se pueden reemplazar elementos nuevamente distorsionando el array'''
		#map_pl2=np.where((dist_breakpoint <= self.distancias) & (self.distancias <= 5000), 2, 0)
		map_pl2=np.where((dist_breakpoint <= mpl1) & (mpl1 <= 5000), 2, mpl1)

		referencia=-9999999*np.ones(np.shape(self.distancias))
		referencia=np.where(map_pl2==1, self.evaluar_pl1(self.distancias), referencia)
		referencia=np.where(map_pl2==2, self.evaluar_pl2(self.distancias), referencia)
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
		#print("\n[modelo_canal.func.mcl] MCL")
		#print(np.maximum(self.balance_simplificado, mcl))
		self.resultado_balance=self.cfg_bal["ptx"]-np.maximum(self.balance_simplificado, self.cfg_bal["mcl"])

		self.resultado_margen=self.resultado_balance-self.cfg_bal["sensibilidad"]



	def balance_del_enlace_simple(self):
		'''Funcion que calcula un balance del enlace sencillo:
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
		#print(self.balance_simplificado)->tiene que ser positivo
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
		self.custom_dist=np.arange(1,20,.9)
		#realizo la simulacion con el array custom diferente.
		self.inicializar_tipo()
		#obtengo resutlados
		plt.plot(self.custom_dist, self.resultado_path_loss, label="Pérdidas")
		plt.legend(loc="upper left")
		plt.title("Pérdidas de Propagación: {}".format(self.cfg_prop["modelo_perdidas"]))
		plt.xlabel("Distancia [Km]")
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
		self.custom_dist=np.arange(1,20,.5)
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
		self.custom_dist=np.arange(1,20,.5)
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
		self.custom_dist=np.arange(1,20,.5)
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
		self.custom_dist=np.arange(1,20,.5)
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
	freq=1.5 #gigas?
	distancias=np.arange(1,200,1)

	#params perdidas
	params_modelo=[30, 0, 1.5] #hb, alfa, hm
	modelo=['okumura_hata',params_modelo] #si no: se pone, se escribe o se escribe bien, el pathloss es 0
	pot_tx=18 #18 #dBm
	loss_tx=5
	gan_tx=5
	gan_rx=8
	loss_rx=0
	sensibilidad=-92 #dBm
	##
	params_p=[modelo, pot_tx,loss_tx, gan_tx, gan_rx, loss_rx,sensibilidad]
	#
	params_sim=[(freq,"ghz"),(distancias, "km")]
	#
	#params desv
	tipo_desv='rayl'
	alpha_n=3.1
	sigma_xn=4
	mu=0
	play_desv=False
	params_desv=[tipo_desv, play_desv, [alpha_n, sigma_xn, mu]]

	modelo_simple=Modelo_Canal(params_p, params_sim, params_desv)
	#LA PREGUNTA ES AQUI, CON LOS anteriores DEBERIA ARROJAR HATA, PERO ESTA REALIZANDO libre_ghz.... Corregido
	#modelo_simple.perdidas_espacio_libre_ghz()
	#path_loss=modelo_simple.resultado_path_loss
	balance=modelo_simple.resultado_balance
	#print(path_loss)

	#desvanecimiento normal
	#distancias_np=np.array([[10,50,100],[130, 170, 200]])
	#print("shape", distancias_np.shape)

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
	freq=1.5 #gigas?
	distancias=np.arange(1,200,0.2)

	#params perdidas
	params_modelo=[30, 0, 1.5] #hb, alfa, hm
	modelo=['okumura_hata',params_modelo] #si no: se pone, se escribe o se escribe bien, el pathloss es 0
	pot_tx=18 #18 #dBm
	loss_tx=5
	gan_tx=5
	gan_rx=8
	loss_rx=0
	sensibilidad=-92 #dBm
	##
	params_p=[modelo, pot_tx,loss_tx, gan_tx, gan_rx, loss_rx,sensibilidad]
	#
	params_sim=[(freq,"ghz"),(distancias, "km")]
	#
	#params desv
	tipo_desv='mixto' #normal, rayl, mixto=normal+rayl
	alpha_n=3.1
	sigma_xn=4
	mu=0
	play_desv=True
	params_desv=[tipo_desv, play_desv, [alpha_n, sigma_xn, mu]]

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
	#prueba_interna_desvanecimiento_normal() #se observa unos puntos planos al principo del array, se debe al mcl.
	prueba_interna_desvanecimiento_prof()
	
else:
	print("Modulo Importado: [", os.path.basename(__file__), "]")
