'''
	Archivo  Simulador.kv 

	Contiene todo el estilo(colores, formas y distribucion en la interfaz),
	llamado de funciones de fondo(creadas por el archivo [gui.py]) para la interfaz,
	funciones de los botones, restricciones, de cada interfaz para el simulador.

	con el fin de entender como se distribuye el codigo, se comenta cada modulo de los archivos gui.py
	identificando cada interfaz con estas llaves <> (lenguaje de KIVY) dentro de estos se encuentra
	todo el diseño de esa interfaz, junto con la nomenclatura necesaria para diferenciar las divisiones.


	Nomenclatura  
	name: "" : distingues la etiqueta de la interfaz para tomar los datos de los archivos .py

	las variables dentro del .py tienen  los mismos nombres de las variables en el  .ky como forma de convencion 
	para mantener el orden de los objetos creados y distinguir.

	Boxlayout: son cajas de tamaños predefinidos por el programador, diferenciando los espacios de contenido
	y desplegados uno tras otro de forma horizontal y vertical.

	label: contenedores de texto para mostrar 

	Textinput: contenedores de texto para digitar de donde el ID es el mismo del objeto para los archivos .py

	Button: botones para acciones en la interfaz.


'''



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


import os 
import pruebas as p 



	


class ModelcanalUMI(Screen):
	nivel = ObjectProperty(None)
	radiocell = ObjectProperty(None)
	intensidadPPP = ObjectProperty(None)
	mrapapport = ObjectProperty(None)
	#ModelcanalUMI= Widget(None)
	current= ""
	#umibox=Widget()
	#umibox.add_widget(BoxLayout())
	def reloaded(self):
		print("aqui TOy umi")
	def evaluar(self, *ingore):
		umibox()
		#if noShowABG
	def openpdf(self):
		os.startfile(r'base_datos\\doc_help_gui\\L2S_interlink_Mapping_Table.pdf')


class ModelcanalUMA(Screen):

	nivel = ObjectProperty(None)
	radiocell = ObjectProperty(None)
	intensidadPPP = ObjectProperty(None)
	current= ""
	ISD_uma= StringProperty("")
	#radiocell=TextInput(text=MainWindow.rcell, multiline=False)
#	def add_datoimport(nivel,radiocell,intensidadPPP,Vsec):
	
#		print(rcell,"---",ISD_uma)
		#print(ISD_uma,"  --- ",rcell,"-----",self.ids.ISD_umak.text)
	#def add_radiocell(rcell):
	#	ISDuma= String
	#	ISDuma.text = rcell
	def reloaded(self):
		print("aqui TOy ")
	def openpdf(self):
		os.startfile(r'base_datos\\doc_help_gui\\L2S_interlink_Mapping_Table.pdf')

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
	def rcell_uma(self):
		rcelluma=str(MainWindow.rcell)
		#rcelluma=MainWindow.addrcell()
		print(rcelluma)
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
	rcell= StringProperty("")
	#layout_instance.do_layout ()
	#Widget.canvas.ask_update ()
	#def on_enter(self, *args):
	#	print("Nivel: ", self.nivel.text," radio celda: ", self.radiocell.text, " Intensidad PPP: ", self.intensidadPPP.text)
	#sr=Image(source='all_ppp_trisec.jpg') 
	
	def addrcell(self):
		rcell=self.rcell
		return rcell 
	def btn(self):
		#print("Nivel: ", self.nivel.text," radio celda: ", self.radiocell.text, " Intensidad PPP: ", self.intensidadPPP.text)
		#SecondWindow.add_dato()
		#get_dato(self.intensidadPPP.text)
		rcell=int(self.radiocell.text)
		nvl=int(self.nivel.text)
		inten=float(self.intensidadPPP.text)
		p.prueba_externa_1(nvl,rcell,inten)
		print(rcell)
		#ModelcanalUMA.ISD_uma=str(addrcell())

		sm.current = "caz"

kv = Builder.load_file("Simulator.kv")
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