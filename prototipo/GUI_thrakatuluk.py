#import matplotlib.pyplot as plt
from kivy.app import App
from kivy.base import runTouchApp
from kivy.lang import Builder
from kivy.uix.textinput import TextInput
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.image import AsyncImage, Image

import pkg1_durbatuluk as dk


class SecondWindow(Screen):

#	nivel = ObjectProperty(None)
#	radiocell = ObjectProperty(None)
	#intensidadPPP = ObjectProperty(None)

	#intensidadPPP=intensidadPPP.text
#	current= ""

	def add_dato(nivel,radiocell,intensidadPPP):
		nvl=''
		rcell=''
		rcell=int(radiocell)
		nvl=int(nivel)
		inten=float(intensidadPPP)

		dk.gestionar_celdas(nvl,rcell,inten)

		#dk.prot_funciones_especiales.prot_poissonpp.distribuir_circulo(dk.apotema,0,0,inten)
		#		print("intensidadPPP:", intensidadPPP)

	

class WindowManager(ScreenManager):
	pass







class tinput(TextInput):
	
	def __init__(self, **kwargs):
		super(tinput,self).__init__(**kwargs)
		intext = TextInput(text = 'Button')
		self.add_widget(intext)

class MainWindow(Screen):
	nivel = ObjectProperty(None)
	radiocell = ObjectProperty(None)
	intensidadPPP = ObjectProperty(None)
	sr = ObjectProperty(None)
	current= ""

	#layout_instance.do_layout ()
	#Widget.canvas.ask_update ()
	#def on_enter(self, *args):
	#	print("Nivel: ", self.nivel.text," radio celda: ", self.radiocell.text, " Intensidad PPP: ", self.intensidadPPP.text)
	sr=Image(source='all_ppp_trisec.jpg')
	def btn(self):
		#print("Nivel: ", self.nivel.text," radio celda: ", self.radiocell.text, " Intensidad PPP: ", self.intensidadPPP.text)
		SecondWindow.add_dato(self.nivel.text, self.radiocell.text, self.intensidadPPP.text)
		#get_dato(self.intensidadPPP.text)
		sm.current = "caz"	
kv = Builder.load_file("Simulator.kv")
sm = WindowManager()
screens = [MainWindow(name="poche"),SecondWindow(name="caz")]
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





