#import
import os
import json

def cargar_variables(target_path):
	'''Abre el archivo de configuracion y lo carga en el sistema.'''
	print(target_path)
	with open(target_path+"configs.json") as json_data_file:
		data = json.load(json_data_file)
	#print(data)
	#print("--")
	#print(data["cfg_simulador"]["params_general"])
	#print(type(data))
	return data

def test_integracion(target):
	print("Integracion")

def guardar_cfg2(data,target_path):
	'''Guarda en formato json el archivo de configuracion del simulador'''
	with open(target_path+"configs2.json", "w") as outfile:
		json.dump(data, outfile)

def guardar_cfg(data,target_path):
	'''Guarda en formato json el archivo de configuracion del simulador'''
	with open(target_path+"configs.json", "w") as outfile:
		json.dump(data, outfile)

if __name__=="__main__":
	#Prototipo:
	d=cargar_variables()
	guardar_variables(d)
else:
	print("Modulo Importado: [", os.path.basename(__file__), "]")
