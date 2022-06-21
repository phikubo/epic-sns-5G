#import
import os
import shutil
import time

def instalar_archivos_de_configuracion():
	'''Copia los archivos de configuracion a la base de datos para inicializar el simulador'''
	original="entorno_virtual_dependencias/configuracion_referencia/"
	target="produccion/sami_v1.1/simapp/static/simulador/base_datos/"
	shutil.copytree(original, target, dirs_exist_ok=True)
	print("[OK] Copia de archivos.")
	time.sleep(1)

def instalar_librerias():
	'''Ejecuta el comando de instalacion de paquetes iniciales.'''
	ruta_actual=os.path.dirname(os.path.abspath(__name__))
	ruta_actual=ruta_actual.replace("\\",'/')+"/entorno_virtual_dependencias/"
	os.system('pip install -r {}requirements.txt --upgrade'.format(ruta_actual))
	print("[PUNTO DE CONTROL 1] Si existe un ERROR, por favor verifique su conexión a internet, firewall, etc.")
	print("[PUNTO DE CONTROL 2] Si los paquetes se han instalado exitosamente, por favor continúe con la instalación del simulador.")
	time.sleep(3)

if __name__=="__main__":
	#Prototipo:
	instalar_archivos_de_configuracion()
	instalar_librerias()
	print("[TERMINADO]")
	time.sleep(10)
	#shutil.copyfile(original, target)
else:
	print("Modulo Importado: [", os.path.basename(__file__), "]")
