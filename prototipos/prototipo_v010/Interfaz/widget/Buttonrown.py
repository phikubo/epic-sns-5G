from kivy.app import App
from kivy.base import runTouchApp
from kivy.lang import Builder
runTouchApp(Builder.load_string('''


GridLayout:
	rows: 5 
	Button:
		text: 'Button 1'
		size_hint_x:None
		width: 500
	Button:
		text: 'Button 2'
	Button:
		text: 'Button 3'
	Button:
		text: 'Button 4'
	Button:
		text: 'Button 5'


'''))