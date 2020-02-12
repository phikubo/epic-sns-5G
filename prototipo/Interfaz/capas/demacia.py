from kivy.app import App
from kivy.base import runTouchApp
from kivy.lang import Builder
runTouchApp(Builder.load_string('''
AnchorLayout:
	anchor_x: 'left'
	anchor_y: 'top'
	Button:
		text: 'A1'
		size_hint: 1 , 1
	
	StackLayout:
		orientation: 'rl-tb'
		padding: 10
		spacing: 5
		Button:
			text: 'S1'
			size_hint: .2, .1
		Button:
			text:'S2'
			size_hint: .2 ,.1
		Button:
			text: 'S3'
			size_hint: .2, .1
		Button:
			text: 'S4'
			size_hint: .2, .1

'''))