from kivy.app import App
from kivy.base import runTouchApp
from kivy.lang import Builder
from kivy.uix.textinput import TextInput
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty



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
	

class SimulatorApp(App):
	def build(self):
		return Backend()




if __name__ == "__main__":
	print("--------------------------------------")
	print("ash Nazg thrakatulûk, agh burzum-ishi krimpatul")
	print("--------------------------------------")

	SimulatorApp().run()





