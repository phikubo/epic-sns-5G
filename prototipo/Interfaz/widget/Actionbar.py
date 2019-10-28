from kivy.app import App
from kivy.base import runTouchApp
from kivy.lang import Builder
runTouchApp(Builder.load_string('''

ActionBar:
	pos_hint: {'top': 1}
	ActionView:
		ActionPrevious:
			title: 'Simulador Tools'
			with_previous: False
		ActionOverflow:
		ActionButton:
			text: 'Guardar datos'
		ActionButton:
			text: 'Cobertura'
		ActionButton:
			text: 'resultados'


'''))