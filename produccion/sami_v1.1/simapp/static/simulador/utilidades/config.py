#import
import os
import json


def guardar_cfg(data,target_path):
	'''Guarda en formato json el archivo de configuracion del simulador'''
	with open(target_path+"/configs.json", "w") as outfile:
		json.dump(data, outfile)


def cargar_cfg(target_path):
	'''Abre el archivo de configuracion y lo carga en el sistema.'''
	with open(target_path+"/configs.json") as json_data_file:
		data = json.load(json_data_file)
	return data


def guardar_json(data,target_path):
	'''Guarda en formato json el archivo especificado'''
	with open(target_path+".json", "w") as outfile:
		json.dump(data, outfile)


def cargar_json(target_path):
	'''Abre el archivo json especificado y lo carga en el sistema.
	Uso: cargar_json("path/name_of_file"'''
	with open(target_path+".json") as json_data_file:
		data = json.load(json_data_file)
	return data


def guardar_json_full(data,target_path):
	'''Guarda en formato json el archivo especificado'''
	with open(target_path, "w") as outfile:
		json.dump(data, outfile)


def cargar_json_full(target_path):
	'''Abre el archivo json especificado y lo carga en el sistema.
	Uso: cargar_json("path/name_of_file"'''
	with open(target_path) as json_data_file:
		data = json.load(json_data_file)
	return data

if __name__=="__main__":
	#Prototipo:
	d=cargar_cfg()
	guardar_cfg(d)
else:
	print("Modulo Importado: [", os.path.basename(__file__), "]")
