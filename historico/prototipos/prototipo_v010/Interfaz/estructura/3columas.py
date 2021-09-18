from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.lang import Builder
from kivy.base import runTouchApp

Builder.load_string("""

<BoxLayout>:
	orintation: 'horizontal'
	Button:
		text: 'B1'
	Button:
		text: 'B2'
		size_hint:2 ,0.5
		pos_hint:{'y': .5}
	Button:
		text: 'B3'

""")

class testApp(BoxLayout):
	pass

if __name__=='__main__':
	runTouchApp(testApp())