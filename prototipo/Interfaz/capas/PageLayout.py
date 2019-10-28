from kivy.app import App
from kivy.base import runTouchApp
from kivy.lang import Builder
runTouchApp(Builder.load_string('''

PageLayout:
	Button:
		text: 'Pag 1'
		size_hint: .5 , .5
	Button:
		size_hint: .5 , .5
		text: 'Pag 2'
	Button:
		size_hint: .5 , .5
		text: 'PaG 3'

'''))