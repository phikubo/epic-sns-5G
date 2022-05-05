#import
import os
import shutil
import time

def install_json_files():
	'''Copia los archivos de configuracion a la base de datos para inicializar el simulador'''
	original="entorno_virtual_dependencias/configuracion_referencia/"
	target="produccion/sami_v1.1/simapp/static/simulador/base_datos/"
	shutil.copytree(original, target, dirs_exist_ok=True)
	print("Configuración completa...")
	time.sleep(3)

if __name__=="__main__":
	#Prototipo:
	install_json_files()
	#shutil.copyfile(original, target)
else:
	print("Modulo Importado: [", os.path.basename(__file__), "]")
