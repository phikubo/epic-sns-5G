# import
import numpy as np
import os
#
def nombre_extension(ubicacion, extension, complemento):
    """Resuelve el nombre por defecto de un archivo con la extensión deseada"""
    ext = str(ubicacion)+"/"+"data_"+str(extension)+"_"+str(complemento)+"."+str(extension)
    return ext


def guardar_data(ruta, nombre_archivo, data, descripcion):
    '''Guarda los datos con una libreria de numpy'''
    #build route
    #example>
    #ruta="home/etc"
    #nombre_archivo="test_file".
    ruta=ruta+'/'+nombre_archivo+'.txt'
    with open(ruta, 'wb') as archivo:  # si es a+ se hace append
        #np.savetxt(archivo, [], header=descripcion)
        np.savetxt(archivo, data, fmt='% 4.4f', header=descripcion)
        archivo.flush()


def cargar_datos(full_ruta):
    '''Carga los datos en el workspace'''
    return np.loadtxt(full_ruta)


def guardar_csv(params):
    '''Guarada el archivo especificado en params. No disponible en SAMI.V.01'''
    pass


def cargar_csv(params):
    '''Carga el archivo especificado en params. No disponible en SAMI.V.01'''
    pass


def test_almacenamiento1():
    data=np.array([59.334335156250006, 52.124325, 58.445371875000006, 53.224098749999996, 72.76188, 95.9808975, 75.067515, 67.989710625, 262.036125, 39.611227500000005, 90.79911249999999])
    descripcion='Test array'
    ruta=""
    nombre_archivo="test.txt"
    guardar_data(ruta, nombre_archivo, data, descripcion)


if __name__ == "__main__":
    # Prototipo:
    test_almacenamiento1()
    
else:
    print("Modulo Importado: [", os.path.basename(__file__), "]")
