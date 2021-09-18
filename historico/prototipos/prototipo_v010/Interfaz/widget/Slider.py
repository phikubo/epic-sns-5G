from kivy.app import App
from kivy.base import runTouchApp
from kivy.lang import Builder
runTouchApp(Builder.load_string('''

BoxLayout:
	size_hint_y:None
	height: sp(100)
	Label:
		text: 'Slider'
	Slider:
		min: -100
		mix: 100
		value: 40
		id: 'Label'	

'''))