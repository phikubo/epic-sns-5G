from kivy.app import App
from kivy.base import runTouchApp
from kivy.lang import Builder
runTouchApp(Builder.load_string('''


BoxLayout:
	padding: 20
	canvas:
		Color:
			rgb: 1,1,1
		Rectangle:
			pos:self.pos
			size:self.size

	BoxLayout:
		padding: 5
		orientation: 'vertical'


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

		BoxLayout:
			orientation: 'horizontal'
			padding: 5 


			AnchorLayout:
				anchor_x: 'right'
				anchor_y: 'bottom'
				Button:
					text: 'A1'
					size_hint: 1 , 1
				Button:
					text: 'Calcular'
					pos_hint: {'x': 1  , 'y': 0}
					size_hint: .2 , .1





'''))