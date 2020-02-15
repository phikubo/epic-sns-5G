import numpy as np
import time
#Get: github/phikubo/recursos-python
#RECIPE: https://www.pythonforthelab.com/blog/introduction-to-storing-data-in-files/, https://stackabuse.com/saving-text-json-and-csv-to-a-file-in-python/
#indexing: https://www.pythoninformer.com/python-libraries/numpy/index-and-slice/
#optimal transport papers:
#https://hal.archives-ouvertes.fr/hal-01717967/document
#https://ljk.imag.fr/membres/Emmanuel.Maitre/lib/exe/fetch.php?media=b07.stflour.pdf
#http://www.math.cmu.edu/~mthorpe/OTNotes
#https://arxiv.org/pdf/1602.01532.pdf
#https://arxiv.org/pdf/1602.01532.pdf
#https://lchizat.github.io/files/presentations/chizat2019IFCAM_OT.pdf
#https://www.math.u-psud.fr/~filippo/Grenoble%20Introduction.pdf
def nombre_extension(extension, complemento):
    """Resuelve el nombre por defecto de un archivo con la extensión deseada"""
    ext="data_"+str(extension)+"_"+str(complemento)+"."+str(extension)
    return ext


def guardar_data_simple(bandera,ext):
    """Guarda estaticamente un array simple en un archivo de extensión deseada"""
    data = np.linspace(0,1,201)
    if bandera:
        nombre_archivo_data=nombre_extension(ext)
        np.savetxt(nombre_archivo_data, data)

def guardar_data_lines(bandera,ext):
    """Guarda estaticamente dos arrays de 2x201 o 201x2"""
    x = np.linspace(0, 200, 201)
    y = np.random.random(201)
    header="coolumna x, columna y"
    print(np.shape([x, y]))
    print(np.shape(np.transpose([x,y])))
    if bandera:
        nombre_archivo_data=nombre_extension(ext)
        #np.savetxt(nombre_archivo_data, [x, y]) # en dos filas
        #np.savetxt(nombre_archivo_data, np.transpose([x, y])) #en dos columnas
        np.savetxt(nombre_archivo_data, np.column_stack((x,y)), header=header) #exactamente igual a transpose


def cargar_datos():
    #data=np.loadtxt('data_txt.txt')
    data=np.loadtxt('data_txt_2columnas.txt')
    x=data[:,0]
    y=data[:,1]
    #data = np.loadtxt('data.dat', comments='@') #cuando el primer comentario es @


def guardar_with_numpy():
    header="coolumna x, columna y"
    x = np.linspace(0, 200, 201)
    y = np.random.random(201)
    nombre_archivo=nombre_extension("txt")
    with open(nombre_archivo, 'wb') as archivo:
        np.savetxt(archivo, [], header=header)
        for i in range(201):
            data=np.column_stack([x[i], y[i]])
            np.savetxt(archivo, data)
            archivo.flush()
            time.sleep(0.1)


def guardar_with():
    x = np.linspace(0, 100, 201)
    nombre_archivo=nombre_extension("txt", "with_solo")
    with open(nombre_archivo, 'w') as archivo:
        archivo.write("#This is the header\n")
        for data in x:
            #archivo.write(str(data)+"\n")
            #archivo.write('{}\n'.format(data)) #segunda opcion
            #archivo.write('{:.3f}\n'.format(data)) #tercera opcion TRUNCA DECIMALES
            archivo.write('{:4.1f}\n'.format(data)) #4ta op. formatea espacios
            

def guardar_with_2colums():
    x = np.linspace(0, 200, 201)
    y = np.random.random(201)
    header="coolumna x, columna y"
    nombre_archivo=nombre_extension("txt", "2columnas")
    with open(nombre_archivo, 'w') as archivo:
        archivo.write("#This is the header\n")
        for i in range(len(x)):
            archivo.write('{:4.1f} {:.4f}\n'.format(x[i], y[i]))
            #write('{:4.1f}\t{:.4f}\n'.format(x[i], y[i])) #con tab en lugar de espacio como separador


def guardar_cvs():
    #https://stackabuse.com/reading-and-writing-csv-files-in-python/
    import csv
    weekdays = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
    sales = ['10', '8', '19', '12', '25']
    with open('sales.csv', 'w') as csv_file:
        csv_writer = csv.writer(csv_file, delimiter=',')
        csv_writer.writerow(weekdays)
        csv_writer.writerow(sales)

def guardar_json():
    #el metodo se encuentra en la carpeta basics, json files.

if __name__=="__main__":
	#Prototipo:
    #guardar_data_simple(False,"txt")
    #guardar_data_lines(True,"txt")
    #guardar_with_numpy()
    #guardar_with()
    #guardar_with_2colums()
    #cargar_datos()
    guardar_cvs()

else:
    print("Importado")

