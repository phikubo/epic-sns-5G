#import
import os


class Simulador:
	def __init__(self):
		pass

	def configurar_tipo_asignacion(self):
		#ATENCION, ESTO DEBERIA SER EN OTRA PARTE, EN TOP, O EN MODELO DE CANAL.
		#O EN GUI.
		'''Configura variables estaticas de acuerdo a la frecuencia portadora
		en el archivo de configuracion.'''

		self.cfg_plan["trama_tol"]=14
		self.cfg_plan["simb_ofdm_dl"]=10
		self.cfg_plan["frame"]=10
		self.cfg_plan["sub_ofdm"]=12

		if self.cfg_gen["portadora"][0]>150 and self.cfg_gen["portadora"][0]<=1500:
			print("frecuencia banda 900, okumura_hata")
			self.cfg_plan["bw"][0]=10 #megaherz, SELECCION 10,20,40 MHZ.
			self.cfg_plan["numerologia"]=1
			self.cfg_plan["g_bw_khz"]=845
			self.cfg_plan["n_rb_sin_gbw"]=273

			self.cfg_plan["caso_de_uso"]=['mMTC']
			#CORREGIR LOS DATOS DE ARRIBA. OK CASO DE USO.
		elif self.cfg_gen["portadora"][0]>1500 and self.cfg_gen["portadora"][0]<=3500:
			print("frecuencia banda 3.5")
			#OFDM_CP='Normal'
			#Parametro fijo para el ancho de banda del sistema
			self.cfg_plan["bw"][0]=100
			#frportadoraGHz= 3.5
			self.cfg_plan["numerologia"]=1
			self.cfg_plan["g_bw_khz"]=845
			self.cfg_plan["n_rb_sin_gbw"]=273

			self.cfg_plan["caso_de_uso"]=['URLLC','mMTC']

		elif self.cfg_gen["portadora"][0]>20000 and self.cfg_gen["portadora"][0]<=24000:
			print("frecuencia banda 20-24")
			self.cfg_plan["bw"][0]=200
			self.cfg_plan["numerologia"]=2
			self.cfg_plan["g_bw_khz"]=4930
			self.cfg_plan["n_rb_sin_gbw"]=264

			self.cfg_plan["caso_de_uso"]=['URLLC','mMTC','eBMM']


		elif self.cfg_gen["portadora"][0]>70000 and self.cfg_gen["portadora"][0]<=73000:
			print("frecuencia banda 70-73")
			self.cfg_plan["bw"][0]=400
			self.cfg_plan["numerologia"]=3
			self.cfg_plan["g_bw_khz"]=9860
			self.cfg_plan["n_rb_sin_gbw"]=264

			self.cfg_plan["caso_de_uso"]=['URLLC','mMTC','eBMM']

		else:
			try:
				raise Exception("PORTADORA NO SOPORTADA")
			except Exception as error:
				print("-----------------------------------------ERROR: {}".format(error))
		print("self.cfg_plan",self.cfg_plan)

if __name__=="__main__":
	#Prototipo:
	pass
else:
	print("Modulo Importado: [", os.path.basename(__file__), "]")
