# import
import numpy as np
import os
#


def nombre_extension(ubicacion, extension, complemento):
    """Resuelve el nombre por defecto de un archivo con la extensión deseada"""
    ext = str(ubicacion)+"/"+"data_"+str(extension)+"_"+str(complemento)+"."+str(extension)
    return ext


def guardar_archivo(data, nombre_archivo, header):
    '''Guarda los datos con una libreria de numpy'''
    with open(nombre_archivo, 'wb') as archivo:  # si es a+ se hace append
        np.savetxt(archivo, [], header=header)
        np.savetxt(archivo, data, fmt='% 4.4f')
        archivo.flush()


def cargar_datos(nombre):
    '''Carga los datos en el workspace'''
    return np.loadtxt(nombre)


def guardar_cvs():
    '''Ejemplo no implmentado'''
    # https://stackabuse.com/reading-and-writing-csv-files-in-python/
    import csv
    weekdays = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
    sales = ['10', '8', '19', '12', '25']
    with open('sales.csv', 'w') as csv_file:
        csv_writer = csv.writer(csv_file, delimiter=',')
        csv_writer.writerow(weekdays)
        csv_writer.writerow(sales)


def guardar_json():
    '''No implementado'''
    # el metodo se encuentra en la carpeta basics, json files, en github.com/phikubo
    pass


if __name__ == "__main__":
    # Prototipo:
    pass
else:
    print("Modulo Importado: [", os.path.basename(__file__), "]")
