#import
import matplotlib.pyplot as plt
import numpy as np
import math
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
	def __init__(self, params_perdidas, params_simulacion, params_desvanecimiento): #usar args and kwards, recibir tipo de primero, y sus parametros.
		#params_perdidas[0]:tipo de perdidas
		#params_perdidas[1]:potencia de tx
		#params_perdidas[2]:perdidas en tx
		#params_perdidas[3]:ganancia en tx ***array numpy *s cambia por ganancia relativa previamente.
		#params_perdidas[4]:ganancia en rx
		#params_perdidas[5]:perdidas en rx
		#params_perdidas[6]:sensibilidad de todos los usuarios #en el futuro, sensibidad variable
		#print("from modelo canal", frecuencia)
		#RX_PWR = TX_PWR – Max (pathloss – G_TX – G_RX, MCL)
		#ENTRADA
		self.debug=False#true si local, false si externo.

		self.tx_prw=params_perdidas[1]
		self.tx_loss=params_perdidas[2]
		self.tx_grel=params_perdidas[3] #relativa
		#--
		self.rx_g=params_perdidas[4] #no relativa
		self.rx_loss=params_perdidas[5]
		self.rx_sens=params_perdidas[6]

		#--
		self.frecuencia=params_simulacion[0][0] #en gigaherz
		self.unidades_freq=params_simulacion[0][1]
		#
		self.distancias=params_simulacion[1][0]
		self.unidades_dist=params_simulacion[1][1]

		self.params_perdidas=params_perdidas
		self.params_desvanecimiento=params_desvanecimiento

		self.tipo_perdidas=params_perdidas[0][0]
		self.params_modelo=params_perdidas[0][1]
		print('parametros modelo', self.params_modelo)
		print('parametros desvanecimiento', self.params_desvanecimiento)
		#AUXILIAR
		#self.distancias=0
		self.resultado_path_loss_antes=0 #eliminar, dejar solo en debug.
		self.desvanecimiento=0
		self.balance_simplificado_antes=0
		self.balance_simplificado=0

		#SALIDA
		self.resultado_path_loss=0
		self.resultado_balance=0
		self.resultado_margen=0
		#self.inicializar_distancias()
		self.inicializar_tipo()
		#se altera el orden para poder obtener los valores de perdidas, en el
		#desvanecimiento rayleight, y luego, adicionar ese desvanecimiento al balance del enlace
		#self.configurar_desvanecimiento()
		self.balance_del_enlace_mcl()
		#self.inicializar_balance()


	def inicializar_tipo(self):
		'''Segun el modelo de propagacion escogido, inicizalizar selecciona la funcion que calcula las perdidas'''
		if self.tipo_perdidas =="espacio_libre":
			#km, GHz
			if self.unidades_dist=="m":
				#convierto a kilometros
				self.distancias=self.distancias/1000
			else:
				pass #opcion kilometro, no cambia.

			if self.unidades_freq=="mhz":
				#convierto a gigaherz
				self.unidades_freq=self.unidades_freq/1000
			else:
				pass #opcion gigahez, no cambia.
			self.perdidas_espacio_libre_ghz()



		elif self.tipo_perdidas =="okumura_hata":
			#km, mhz
			if self.unidades_dist=="m":
				#convierto a kilometros
				self.distancias=self.distancias/1000
			else:
				pass #opcion kilometro, no cambia.
			if self.unidades_freq=="ghz":
				#convierto a megaherz
				self.unidades_freq=self.unidades_freq*1000
			else:
				pass #opcion megaherz, no cambia.
			self.perdidas_okumura_hata_mhz()

		else:
			pass

	def configurar_desvanecimiento(self):
		'''Crea un array de desvanecimiento, dependiendo del tipo y especificaciones extras'''
		if self.params_desvanecimiento[0]=="normal":
			print("normal seleccionado")
			#distancias=np.arange(1,200,1)
			#sized=len(distancias)
			if self.params_desvanecimiento[1]:
				sigma_xn=self.params_desvanecimiento[2][1]
				mu=self.params_desvanecimiento[2][2]
				#if true, el desvanecimiento deja de ser 0 y se integra a las perdidas.
				self.desvanecimiento=np.random.normal(mu,sigma_xn,self.distancias.shape)
				self.balance_simplificado=self.resultado_path_loss-self.tx_grel-self.rx_g+self.tx_loss+self.rx_loss
				#solo en debug
				self.balance_simplificado_antes=self.balance_simplificado
				#COMENTAR en produccion. solo para propositos demostrativos
				if self.debug:
					plt.plot(self.distancias, -self.balance_simplificado, 'r-',  label="sin ptx, simplificado")
				else:
					pass

				self.balance_simplificado=self.balance_simplificado+self.desvanecimiento
				#plt.plot(self.distancias, -self.balance_simplificado, "go-",  label="sin ptx + desva")
			else:
				pass #se suma 0, a las perdidas iniciales.

		elif self.params_desvanecimiento[0]=="rayl":
			print("(rayleight) seleccionado")
			if self.params_desvanecimiento[1]:
				#self.resultado_path_loss es positivo. por eso la ecuacion cambia.
				self.balance_simplificado=self.resultado_path_loss-self.tx_grel-self.rx_g+self.tx_loss+self.rx_loss
				#QUITAR LUEGO
				self.balance_simplificado_antes=self.balance_simplificado
				#COMENTAR en produccion. solo para propositos demostrativos
				if self.debug:
					plt.plot(self.distancias, -self.balance_simplificado, 'r', label="sin desva, sin ptx")
				else:
					pass
				#debe ser negativo siempre.
				bal_simpl_desva=10**(-self.balance_simplificado/10)
				bal_simpl_desva_r=np.sqrt(bal_simpl_desva)
				b=bal_simpl_desva_r/np.sqrt(np.pi/2)
				bray=np.random.rayleigh(b)
				bray=np.power(bray,2)
				self.desvanecimiento=10*np.log10(bray) #bray_dB
				self.balance_simplificado=-self.desvanecimiento
			else:
				pass #se suma 0, a las perdidas iniciales.

		elif self.params_desvanecimiento[0]=="mixto":
			print("RAY+NORMAL seleccionado")
			'''Idea1. el balance simplificado de la normal, se recibe como parametro en la rayleigh'''
			#normal
			sigma_xn=self.params_desvanecimiento[2][1]
			mu=self.params_desvanecimiento[2][2]
			#if true, el desvanecimiento deja de ser 0 y se integra a las perdidas.
			self.desvanecimiento=np.random.normal(mu,sigma_xn,self.distancias.shape)
			self.balance_simplificado=self.resultado_path_loss-self.tx_grel-self.rx_g+self.tx_loss+self.rx_loss
			#QUITAR LUEGO
			self.balance_simplificado_antes=self.balance_simplificado
			#COMENTAR en produccion. solo para propositos demostrativos
			if self.debug:
				plt.plot(self.distancias, -self.balance_simplificado, 'r-',  label="sin ptx, simplificado")
			else:
				pass

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

			'''Idea2. al balance rayleig, se sumo la N, de la distribucion normal. Opcion viable.'''
		else:
			pass

	def perdidas_espacio_libre_ghz(self):
		#outs dB
		'''Funcion que calcula las perdidas de espacio libre en dB'''
		self.resultado_path_loss=92.4+20*np.log10(self.frecuencia)+20*np.log10(self.distancias)

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
		hb=self.params_modelo[0]
		alfa=self.params_modelo[1] #0 si hm=1.5m
		hm=self.params_modelo[2]
		#de la forma: Lp=A+Blog10(R)

		A=69.55+26.16*np.log10(self.frecuencia)-13.82*np.log10(hb)-alfa*(hm)
		B=44.9-6.55*np.log10(hb)
		E=3.2*(np.log10(11.75*hm))**2 -4.97 #[dB] para ciudades grandes y fc>300 MHz
		#E=8.29*(np.log10(1.54*hm))**2 -1.1 #[dB] para ciudades grandes y fc<300 MHz
		#print("okumura_hata, says->A,B:",A,B)
		#print("distancias")
		#print(self.distancias)
		self.resultado_path_loss_antes=A+B*np.log10(self.distancias)-E
		self.resultado_path_loss=A+B*np.log10(self.distancias)-E #+ self.desvanecimiento


	def perdidas_umi_ci(self):
		'''Este modulo recrea las perdidas con distancia [m] frecuencia [GHz] con los parametros alpha_n: 3.1 y con Sigma_Xn:8.1 dB
		considerados por la documentacion valores en dB para sigma y veces para alpha_n
		***articulo Simulation path loss Propagation Path Loss models for 5G urban micro and macro-cellular Scenarios
		-rango de frecuencias debajo de 30GHz'''
		alpha_n=3.1
		sigma_xn=8.1
		correcion_freq_ghz=32.4+20*math.log10(self.frecuencia)
		correccion_dist_m=10*alpha_n*np.log10(self.distancias)
		self.resultado_path_loss=correcion_freq_ghz+correccion_dist_m+sigma_xn


	def perdidas_umi_abg(self):
		'''Este modulo recrea las perdidas con distacia [m] frecuencia [GHz] con los parametros alpha_n: 3.5 gamma : 1.9 (veces)
		-consideramos alpha y gamma como la dependencia de las perdidas en  relacion a la distancia y la frecuencia
		-Beta es un factor de correccion o compensacion de optimizacion en [dB],
		-sigma_Xn[dB]:8.0 desviacion estandar.
		***articulo Propagation Path Loss Models for 5G Urban Micro- and Macro-Cellular Scenarios✮
		-rango de frecuencias debajo de 30GHz'''
		alpha_n=3.5
		beta=24.4
		gamma=1.9
		sigma_xn=8.0
		correccion_freq_ghz=(10*gamma*math.log10(self.frecuencia))
		correcion_dist_m=(10*alpha_n*np.log10(self.distancias))
		self.resultado_path_loss=correccion_freq_ghz+correcion_dist_m+beta+sigma_xn


	def parametro_uma_pl(self, dist ,dist_ref,dist_3d):
		'''Falta documentar, falta corregir variables locales y globales (self.dist?)'''
		if (dist <= dist_ref) and (dist>= 10):
			path_l=28.0+22*math.log10(dist_3d)+20*math.log10(self.frecuencia)
		elif self.dist>disbp and dist<=5000:
			path_l=13.54+39.08*math.log10(dist_3d)+20*math.log10(self.frecuencia)-0.6*(Hut-1.5)
		else:
			path_l=32.4+20*log10(self.frecuencia)+20*log10(10)
		return path_l


	def perdidas_tr_38901(self):
		'''Este modulo recrea las perdidas con distancia[m] y frecuencia[GHz] con los parametros
		-distancia breakpoint: 4(Hbs-He)*(Hut-He)*fc/C
		-rango de frecuencias para escenario UMa son por debajo de 6Ghz
		Fuente: https://www.etsi.org/deliver/etsi_tr/138900_138999/138901/15.00.00_60/tr_138901v150000p.pdf'''
		frecuencia_hz= self.frecuencia*math.pow(10,9)
		distancia_3d=np.sqrt(Hbs**2+self.distancias**2)
		dist_breakpoint=(4*(Hbs-He)*(Hut-He)*frecuencia_hz)/(3*math.pow(10, 8))
		dist_bp=np.array(np.ones_like(self.distancias)*dist_breakpoint,dtype='int32')
		#print(distbreakpoint)
		#CORREGIR
		pl=[self.parametro_uma_pl(distancias,dist_ref,dist_3d) for distancias,dist_ref,dist_3d in zip(self.distancias,dist_bp,distancia_3d)]
		self.path_loss=np.array(pl,dtype='float32')


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
		mcl=70 #dB para entorno urbano.
		#segmento_tx=self.tx_grel-self.tx_loss
		#segmento_rx=self.rx_g-self.rx_loss
		#self.resultado_balance=segmento_tx+segmento_rx-self.resultado_path_loss
		self.configurar_desvanecimiento()
		'''
		if self.params_desvanecimiento[0]=="normal":
			self.balance_simplificado=self.resultado_path_loss-self.tx_grel-self.rx_g+self.tx_loss+self.rx_loss
			plt.plot(self.distancias, -self.balance_simplificado, 'r-',  label="sin ptx, simplificado")
			self.balance_simplificado=self.balance_simplificado+self.desvanecimiento
			plt.plot(self.distancias, -self.balance_simplificado, "go-",  label="sin ptx + desva")

		elif self.params_desvanecimiento[0]=="profundo":
			self.balance_simplificado=-self.desvanecimiento-self.tx_grel-self.rx_g+self.tx_loss+self.rx_loss
			balance_simplificado_original=self.resultado_path_loss-self.tx_grel-self.rx_g+self.tx_loss+self.rx_loss
			plt.plot(self.distancias, -balance_simplificado_original, "r-",  label="sin ptx. simplificado")
			plt.plot(self.distancias, -self.balance_simplificado, "go-",  label="sin ptx. desva insted pl")
		else:
			pass
		'''

		#
		#print("\n[modelo_canal.func.mcl] MCL")
		#print(np.maximum(self.balance_simplificado, mcl))
		self.resultado_balance=self.tx_prw-np.maximum(self.balance_simplificado, mcl)
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
		plt.title('Perdidas modelo: '+ self.tipo_perdidas+', desva: '+self.params_desvanecimiento[0])
		if self.params_desvanecimiento[0]=='normal':
			plt.plot(self.distancias, -self.balance_simplificado, label="normal+sin ptx, simplificado")
		else:
			pass
		plt.plot(self.distancias, self.desvanecimiento, label="desva "+self.params_desvanecimiento[0])
		plt.plot(self.distancias, self.resultado_balance,'bx-', label="mcl y ptx")
		plt.legend(loc="upper left")
		#en el plot es negativo por aquello de la ecuacion mcl.




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
	print("Modulo <escribir_nombre> importado")
