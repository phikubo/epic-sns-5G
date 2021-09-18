import kivy
from kivy.app import App 
from kivy.uix.gridlayout import GridLayout
from kivy.lang import Builder 

Builder.load_string(''' 

<Demo>:
	cols: 2
	BoxLayout:
		orientation: 'horizontal'
		Button:
			text: 'Deena'
			pos_hint :{'x':0}
		Button:
			text: 'papaya'
			pos_hint : {'x':0}











''')

class Demo(GridLayout):
		pass

class DemoApp(App):
		def build(self):
			return Demo()

if __name__=='__main__':
	DemoApp().run()