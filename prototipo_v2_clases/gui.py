from kivy.app import App
from kivy.base import runTouchApp
from kivy.lang import Builder
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from functools import partial
from kivy.properties import ObjectProperty
from kivy.properties import StringProperty
from kivy.properties import BooleanProperty
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.image import AsyncImage, Image


import pruebas as p 



	


class ModelcanalUMI(Screen):
	noShownCI = BooleanProperty(True)
	noShownABG= BooleanProperty(True)
	nivel = ObjectProperty(None)
	radiocell = ObjectProperty(None)
	intensidadPPP = ObjectProperty(None)
	mrapapport = ObjectProperty(None)
	#ModelcanalUMI= Widget(None)
	current= ""
	#umibox=Widget()
	#umibox.add_widget(BoxLayout())
	
	def disable(self, instance, *args):
		instance.disabled= True
	def reloaded(self):
		print("aqui TOy ")
		

	def build(self):
		mrappaport.bind(on_press=partial(self.disable,mrappaport))
		mrappaport.bind(on_press=partial(self.reloaded,mrappaport))
		return mrappaport
	def evaluar(self, *ingore):
		umibox()

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
	nivel = ObjectProperty(None)
	radiocell = ObjectProperty(None)
	intensidadPPP = ObjectProperty(None)
	sr = ObjectProperty(None)
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
		rcell=int(self.radiocell.text)
		nvl=int(self.nivel.text)
		inten=float(self.intensidadPPP.text)

		p.prueba_pk_dispositivos(nvl,rcell,inten)
		
		#SecondWindow.add_dato(self)
		

		sm.current = "caz"

		

kv = Builder.load_file("Simulator.kv")
sm = WindowManager()
screens = [MainWindow(name="poche"),SecondWindow(name="caz"),ModelcanalUMA(name="king"),ModelcanalUMI(name="sking")]
for screen in screens:
	sm.add_widget(screen)
  

#def get_dato(intensidadPPP):
#	inten=int(intensidadPPP)
#	return intePPP
	


sm.current="sking"

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