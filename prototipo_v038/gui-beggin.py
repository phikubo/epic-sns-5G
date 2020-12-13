from kivy.app import App
from kivy.base import runTouchApp
from kivy.lang import Builder
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty
from kivy.properties import StringProperty
from kivy.properties import BooleanProperty
from kivy.uix.dropdown import DropDown
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.image import AsyncImage, Image

"""
Importamos los datos del archivo Json en la seccion de cfg_gui  llamados desde el 
MainWindow uniendo el backen y el frontend del simulador. usando las funciones del
archivo kivy donde se declaran las variables de la GUI para ser guardadas y 
posteriormente evaluadas para su debido  funcionamiento 

"""
from utilidades import config as cfg 
import json
#with open("simulator-beggin.kv", encoding='utf-8', errors="surrogateescape") as kv_file:
#    Builder.load_string(kv_file.read())

#for line in f:

#import pruebas as p 



class ModelcanalUMI(Screen):
	noShownCI = BooleanProperty(True)
	noShownABG= BooleanProperty(True)
	nivel = ObjectProperty(None)
	radiocell = ObjectProperty(None)
	intensidadPPP = ObjectProperty(None)
	#ModelcanalUMI= Widget(None)
	current= ""
	#umibox=Widget()
	#umibox.add_widget(BoxLayout())
	def evaluar(self, *ingore):
		umibox()

		if self.noShownABG==True:  
			self.remove_widget(umibox)	

		else:
			pass

		#if noShowABG
class ModelcanalUMA(Screen):

	nivel = ObjectProperty(None)
	radiocell = ObjectProperty(None)
	intensidadPPP = ObjectProperty(None)
	current= ""

#	def add_datoimport(nivel,radiocell,intensidadPPP,Vsec):	
class contenedorgrilla(Screen):
	pass
class SecondWindow(Screen):
	#sr = StringProperty('C:/Users/PIPE_PC/Documents/UNIVERSIDAD/TESIS/epic-sns-5G/prototipo/all_ppp_trisec.jpg')
#	nivel = ObjectProperty(None)
#	radiocell = ObjectProperty(None)
	#intensidadPPP = ObjectProperty(None)
	#self.add_widget(image)
	#sr=Image(source='all_ppp_trisec.jpg')
 	#self.sr.reload()
	#intensidadPPP=intensidadPPP.text
#	current= ""
	#sr=Image(source='all_ppp_trisec.jpg')
#	sr.Image(source='all_ppp_trisec.jpg')
#	add_widget(Boxlayout())

	#def add_dato(self):
	#	sr = StringProperty('C:/Users/PIPE_PC/Documents/UNIVERSIDAD/TESIS/epic-sns-5G/prototipo/all_ppp_trisec.jpg')
		#print('por aqui pase')
		#Image(im)
		
	#	sr ='C:/Users/PIPE_PC/Documents/UNIVERSIDAD/TESIS/epic-sns-5G/prototipo/all_ppp_trisec.jpg'
			#sr.reload()
	#	sm.current= "caz"
	#	return SecondWindow()
		
	
		#dk.gestionar_celdas(nvl,rcell,inten)
		
		#dk.prot_funciones_especiales.prot_poissonpp.distribuir_circulo(dk.apotema,0,0,inten)
		#		print("intensidadPPP:", intensidadPPP)
	pass
class WindowManager(ScreenManager):
	pass
class hidenWindow(TextInput):
	def __init__(hidenWindow,self, **kwargs):
		super(hidenWindow,self).__init__(**kwargs)
		intext = TextInput(text = 'Button')
		self.add_widget(hidenWindow)
		self.clear_widget()
class MainWindow(Screen):
	fp = ObjectProperty(None)
	bw= ObjectProperty(None)
	isd= ObjectProperty(None)
	ppp= ObjectProperty(None)
	esc= ObjectProperty(None)
	mp= ObjectProperty(None)
	desv= ObjectProperty(None)
	nf= ObjectProperty(None)
	ptx= ObjectProperty(None)
	patron= ObjectProperty(None)
	celdas= ObjectProperty(None)

	
	current= ""

	#layout_instance.do_layout ()
	#Widget.canvas.ask_update ()

	#def on_enter(self, *args):
	#	print("Nivel: ", self.nivel.text," radio celda: ", self.radiocell.text, " Intensidad PPP: ", self.intensidadPPP.text)
	#sr=Image(source='all_ppp_trisec.jpg') 

	def btn(self):
		#print("Nivel: ", self.nivel.text," radio celda: ", self.radiocell.text, " Intensidad PPP: ", self.intensidadPPP.text)
		#SecondWindow.add_dato()
		#get_dato(self.intensidadPPP.text)

		print("**************************************************")
		print("**********Inicio INTERNAS GUI****************")
		print("**************************************************")

		print(int(self.fp.text))
		print(int(self.bw.text))
		print(int(self.isd.text))
		print(str(self.ppp.text))
		print(str(self.esc.text))
		print(str(self.mp.text))
		print(str(self.desv.text))
		print(int(self.nf.text))
		print(int(self.ptx.text))
		print(str(self.patron.text))
		print(int(self.celdas.text))


		config2=cfg.cargar_variables(target_path="base_datos/")
		config2["cfg_gui"]["freqport"]= int(self.fp.text)
		config2["cfg_gui"]["bwMHz"]=int(self.bw.text)
		config2["cfg_gui"]["ppp"]=str(self.ppp.text)
		config2["cfg_gui"]["escenario"]=str(self.esc.text)
		config2["cfg_gui"]["isd"]=int(self.isd.text)
		config2["cfg_gui"]["modperdidas"]=str(self.mp.text)
		config2["cfg_gui"]["desvanecimiento"]=str(self.desv.text)
		config2["cfg_gui"]["nf"]=int(self.nf.text)
		config2["cfg_gui"]["ptx"]=int(self.ptx.text)
		config2["cfg_gui"]["patron"]=str(self.patron.text)
		config2["cfg_gui"]["nceldas"]=int(self.celdas.text)
		
						
		print("**************************************************")
		print("**********FIN PRUEBA INTENAS GUI****************")
		print("**************************************************")

		print(config2)

		print("**************************************************")
		print("**********Inicio pruebas GUI****************")
		print("**************************************************")

		#cfg.guardar_variables(configuracion,target_path="base_datos/")
		#print(configuracion)

		print("**************************************************")
		print("**********pruebas JSON CONFIGURACION GUI****************")
		print("**************************************************")
		

		cfg.guardar_variables(config2,target_path="base_datos/")
		print(config2)

		print("**************************************************")
		print("**********pruebas JSON CONFIG2 GUI****************")
		print("**************************************************")
		
		#rcell=int(self.radiocell.text)
		#nvl=int(self.nivel.text)
		#inten=float(self.intensidadPPP.text)

		#p.prueba_pk_dispositivos(nvl,rcell,inten)
		
		#SecondWindow.add_dato(self)
		

		sm.current = "caz"

		

kv = Builder.load_file("Simulator-beggin.kv")
sm = WindowManager()
screens = [MainWindow(name="poche"),SecondWindow(name="caz"),ModelcanalUMA(name="king"),ModelcanalUMI(name="sking")]
for screen in screens:
	sm.add_widget(screen)
  

#def get_dato(intensidadPPP):
#	inten=int(intensidadPPP)
#	return intePPP
	


sm.current="poche"

class SimulatorApp(App):
	def build(self):
		return sm

if __name__ == "__main__":
	print("--------------------------------------")
	print("ash Nazg thrakatulûk, agh burzum-ishi krimpatul")
	print("--------------------------------------")
	#
#	ward_Backend()
	#nivel,radiocell,intensidadPPP=self.nivel.tex, self.radiocell.text, self.intensidadPPP
	#print("nivel :",nivel,"radiocell  :",radiocell,"intensidadPPP:  ",intensidadPPP)
	#dk.gestionar_celdas(nivel,radiocell)

	SimulatorApp().run()