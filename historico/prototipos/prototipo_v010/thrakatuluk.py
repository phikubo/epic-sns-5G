#import matplotlib.pyplot as plt
from kivy.app import App
from kivy.base import runTouchApp
from kivy.lang import Builder
from kivy.uix.textinput import TextInput
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty
from kivy.uix.screenmanager import ScreenManager, Screen

#import pkg1_durbatuluk as dk


#class MainWindow(Screen):
#	pass

#class SecondWindow(Screen):
#	pass

#class WindowManager(ScreenManager):
#	pass







class tinput(TextInput):
	
	def __init__(self, **kwargs):
		super(tinput,self).__init__(**kwargs)


		intext = TextInput(text = 'Button')
		self.add_widget(intext)

class Backend(Widget):
	nivel = ObjectProperty(None)
	radiocell = ObjectProperty(None)
	intensidadPPP = ObjectProperty(None)

	def btn(self):
		print("Nivel: ", self.nivel.text," radio celda: ", self.radiocell.text, " Intensidad PPP: ", self.intensidadPPP.text)
		

#kv = Builder.load_file("Simulator.kv")



class SimulatorApp(App):
	def build(self):
		return Backend()

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





