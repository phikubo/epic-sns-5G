from kivy.base import runTouchApp 	
from kivy.lang import Builder


runTouchApp(Builder.load_string('''

StackLayout:
	Button:
		text: 'kivy'
		size_hint: .2,.2







'''))
