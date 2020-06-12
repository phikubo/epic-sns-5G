#import
import numpy as np
import math
#como esto no usa submodulos, no necesito hacer try catch en esos modulos.
#en el futuro si puede ocurrir, asi que:

#try:
	#aqui van los submodulos.
#except:
	#pass

#modelo del canal incluye perdidas AWGN y RUIDO. Crear modulos awgn y ruido.
class Modelo_Canal:
	"""Clase que define el modelo del canal, calcula las perdidas del sistema. No adiciona AWGN ni Ruido."""
	def __init__(self, params_perdidas,frecuencia, params_distancia): #usar args and kwards, recibir tipo de primero, y sus parametros.
		#params_perdidas[0]:tipo de perdidas
		#params_perdidas[1]:potencia de tx
		#params_perdidas[2]:perdidas en tx
		#params_perdidas[3]:ganancia en tx
		#params_perdidas[4]:ganancia en rx
		#params_perdidas[5]:perdidas en rx
		#params_perdidas[6]:sensibilidad de todos los usuarios #en el futuro, sensibidad variable

		self.frecuencia=frecuencia #en gigaherz
		self.distancias, self.unidades=params_distancia
		self.params_perdidas=params_perdidas
		self.distancia_km=0
		self.tipo_perdidas=params_perdidas[0]

		self.resultado_path_loss=0
		self.resultado_balance=0
		self.resultado_margen=0
		self.inicializar_distancias_km()
		#self.inicializar_tipo()

	def inicializar_distancias_km(self):
		if self.unidades=="m" and self.tipo_perdidas=="espacio_libre":
			self.distancia_km=self.distancias/1000
		elif self.unidades=="m" and self.tipo_perdidas=="okumura_hata":
			self.distancia_km=self.distancias/1000
		elif self.unidades=="km":
			pass

	def perdidas_espacio_libre_ghz(self):
		'''Funcion que calcula las perdidas de espacio libre en dB'''
		self.resultado_path_loss=92.4+20*np.log10(self.frecuencia)+20*np.log10(self.distancia_km)

	def perdidas_okumura_hata_mhz(self):
		'''Funcion que calcula las perdidasd de espacio con el modelo hata 1980.
		Fuente:Empirical Formula for Propagation Loss in Land Mobile Radio Services'''
		#rangos
		#fc:150,1500 MHz
		#hb=30,200 m
		#R:1, 200 km
		hb=30 #m
		alfa=0
		hm=1.5
		#de la forma: Lp=A+Blog10(R)
		A=69.55+26.16*np.log10(self.frecuencia)-13.82*np.log10(hb)-alfa*(hm)
		B=44.9-6.55*np.log10(hb)
		E=3.2*(np.log10(11.75*hm))**2 -4.97 #[dB] para ciudades grandes y fc>300 MHz
		#E=8.29*(np.log10(1.54*hm))**2 -1.1 #[dB] para ciudades grandes y fc<300 MHz
		print("a,b:",A,B)
		self.resultado_path_loss=A+B*np.log10(self.distancia_km)-E


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


	def parametro_uma_pl(self, dist ,dist _ref,dist_3d):
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
		'''Funcion que calcula un balance del enlace sencillo'''
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
		segmento_tx=self.params_perdidas[1]-self.params_perdidas[2]+self.params_perdidas[3]
		segmento_rx=self.params_perdidas[4]-self.params_perdidas[5]
		self.resultado_balance=segmento_tx-self.resultado_path_loss+segmento_rx
		#print("[mod canal] margen")
		self.resultado_margen=self.resultado_balance+self.params_perdidas[6]

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
	'''Funcion que prueba el concepto de perdidas de espacio libre con numpy'''
	freq=10 #en gigas
	distancias_km=np.array([0.1, 1, 2, 3, 4, 5, 6])
	modelo_simple=Modelo_Canal(freq, distancias_km)
	modelo_simple.perdidas_espacio_libre_ghz()
	l_bs=modelo_simple.resultado_path_loss
	print(l_bs)



if __name__=="__main__":
	#Prototipo:
	#import #aqui van los submodulos nuevamente para envitar errores

	#prueba interna 1.
	prueba_interna_resultado_path_loss()
else:
	print("Modulo <escribir_nombre> importado")
