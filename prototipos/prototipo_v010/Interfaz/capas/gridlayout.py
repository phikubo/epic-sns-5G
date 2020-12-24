from kivy.app import App
from kivy.base import runTouchApp
from kivy.lang import Builder
runTouchApp(Builder.load_string('''

<Button>:
	color: .8 ,.9 ,0 ,1
	font_size: 32
	size_hint: .3 ,.2

FloatLayout:
	Button:
		text: 'Hello'
		pos_hint: {'x': 0 , 'top': 1}
	Button:
		text: 'world'
		pos_hint: {'right': 1 , 'y': 0}
		
'''))