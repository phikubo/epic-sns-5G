from kivy.app import App
from kivy.base import runTouchApp
from kivy.lang import Builder
runTouchApp(Builder.load_string('''

<Button>:
	font_size: 32
	size_hint: .5 , .2


Label:
	Button:
		text: 'Hello'
		color: .8 , .9 ,.0 ,1
		pos_hint: {'x': 0 , 'y': 0}
		size_hint: .5 , .2

	Button:
		text: 'world'
		color: .8 , .9 ,.0 ,1
		pos_hint: {'x': 0, 'top':1}
		size_hint: .5 , .2


'''))