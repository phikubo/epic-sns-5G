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

		#SALIDA
		self.resultado_path_loss=0
		self.resultado_balance=0
		self.resultado_margen=0
		#self.inicializar_distancias()
		self.inicializar_desvanecimiento()
		self.inicializar_tipo()
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
			self.balance_del_enlace_simple()


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
			self.balance_del_enlace_mcl() # ->generar errorees
			#self.balance_del_enlace_simple()
		else:
			pass

	def inicializar_desvanecimiento(self):
		'''Crea un array de desvanecimiento, dependiendo del tipo y especificaciones extras'''
		if self.params_desvanecimiento[0]=="lento":
			print("lento seleccionado")
			#distancias=np.arange(1,200,1)
			#sized=len(distancias)
			if self.params_desvanecimiento[1]:
				sigma_xn=self.params_desvanecimiento[2][1]
				mu=self.params_desvanecimiento[2][2]
				#if true, el desvanecimiento deja de ser 0 y se integra a las perdidas.
				self.desvanecimiento=np.random.normal(mu,sigma_xn,self.distancias.shape)
			else:
				pass #se suma 0, a las perdidas iniciales.


		elif self.params_desvanecimiento[0]=="rapido":
			print("rapido seleccionado")
		elif self.params_desvanecimiento[0]=="mixto":
			print("rapido+lento seleccionado")
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
		print("okumura_hata, says->A,B:",A,B)
		print("distancias")
		print(self.distancias)
		self.resultado_path_loss_antes=A+B*np.log10(self.distancias)-E
		self.resultado_path_loss=A+B*np.log10(self.distancias)-E + self.desvanecimiento


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
		G_RX is the receiver antenna gain '''
		mcl=70 #dB para entorno urbano.
		#segmento_tx=self.tx_grel-self.tx_loss
		#segmento_rx=self.rx_g-self.rx_loss
		#self.resultado_balance=segmento_tx+segmento_rx-self.resultado_path_loss
		print("-----------------------path loss: ")
		print(self.resultado_path_loss)
		balance_simplificado=self.resultado_path_loss-self.tx_grel-self.rx_g+self.tx_loss+self.rx_loss
		print("-----------------------balance simplificado: ")
		print(balance_simplificado)
		maxx=np.maximum(balance_simplificado, mcl)
		self.resultado_balance=self.tx_prw-np.maximum(balance_simplificado, mcl)
		print("-----------------------resultadao balance simplificado-> maxx: ")
		print(maxx)
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




def prueba_interna_resultado_path_loss():
	#obsoleta
	'''Funcion que prueba el concepto de perdidas de espacio libre con numpy'''
	freq=10 #en gigas
	distancias_km=np.array([0.1, 1, 2, 3, 4, 5, 6])
	modelo_simple=Modelo_Canal(freq, distancias_km)
	modelo_simple.perdidas_espacio_libre_ghz()
	l_bs=modelo_simple.resultado_path_loss
	print(l_bs)

def prueba_interna_desvanecimiento():
	'''Funcion que prueba el concepto de tipos desvanecimiento con numpy'''
	#params sim
	freq=1.5 #gigas?
	distancias=np.arange(1,200,1)

	#params perdidas
	params_modelo=[30, 0, 1.5] #hb, alfa, hm
	modelo=['okumura_hata',params_modelo] #si no: se pone, se escribe o se escribe bien, el pathloss es 0
	pot_tx=30,52 #18 #dBm
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
	tipo_desv='lento'
	alpha_n=3.1
	sigma_xn=8.1
	mu=0
	play_desv=False
	params_desv=[tipo_desv, play_desv, [alpha_n, sigma_xn, mu]]

	modelo_simple=Modelo_Canal(params_p, params_sim, params_desv)
	#LA PREGUNTA ES AQUI, CON LOS anteriores DEBERIA ARROJAR HATA, PERO ESTA REALIZANDO libre_ghz.... Corregido
	#modelo_simple.perdidas_espacio_libre_ghz()
	path_loss=modelo_simple.resultado_path_loss
	#print(path_loss)

	#desvanecimiento lento
	#distancias_np=np.array([[10,50,100],[130, 170, 200]])
	#print("shape", distancias_np.shape)

	#sized=len(distancias)
	N=np.random.normal(mu,sigma_xn,distancias.shape)
	path_loss_desv=path_loss+N
	plt.grid(True)
	plt.xlabel('Distancia m')
	plt.ylabel('Perdidas [dB]')
	plt.title('Perdidas modelo: '+ modelo[0])
	#plt.plot(distancias,path_loss,'b*')
	plt.plot(distancias,path_loss,'b*')
	plt.plot(distancias,path_loss_desv,'go')
	plt.show()


if __name__=="__main__":
	#Prototipo:
	#import #aqui van los submodulos nuevamente para envitar errores

	#prueba interna 1.
	#prueba_interna_resultado_path_loss()
	prueba_interna_desvanecimiento()
else:
	print("Modulo <escribir_nombre> importado")
