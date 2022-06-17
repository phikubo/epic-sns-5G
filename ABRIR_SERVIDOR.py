#import
import os
import time

def abrir_servidor():
	'''Ejecuta el entorno virtual y abre el servidor en el local host'''
	print("Intentando abrir")
	
	ruta_actual=os.path.dirname(os.path.abspath(__name__))
	ruta_actual=ruta_actual.replace("\\",'/')+"/produccion/sami_v1.1/"
	print(ruta_actual)
	#os.system('workon tesis & python {}manage.py runserver'.format(ruta_actual))
	#print("ok workon?")
	os.system('python {}manage.py runserver'.format(ruta_actual))
	print("Configuración completa...")
	time.sleep(50)

if __name__=="__main__":
	#Prototipo:
	abrir_servidor()
	#shutil.copyfile(original, target)
else:
	print("Modulo Importado: [", os.path.basename(__file__), "]")
