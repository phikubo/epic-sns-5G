from kivy.app import App
from kivy.base import runTouchApp
from kivy.lang import Builder
runTouchApp(Builder.load_string(''' 


RelativeLayout:
	padding: 30
	Button:
		text: 'R1'
		size_hint: .3 , .3
		pos: 50 ,100
	Button:
		text: 'R2'
		size_hint: .2 , .2
		pos: 500 , 0



'''))