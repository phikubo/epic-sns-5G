#import
import os
import pytest
import numpy as np
import matplotlib.pyplot as plt

def calcular_probabilidad(arreglo, numero):
	'''Calcula la probabilidad de un arreglo de datos, mediante el conteo de ocurrencia de un histograma.'''
	ocurrencia,limites=np.histogram(arreglo,numero)
	limite=limites[2]-limites[1]
	prob=ocurrencia/sum(ocurrencia)
	centros=calcular_centros(limites)
	#for a,b in zip(centros,prob):
	#	print(a,b)
	return prob, centros, limite

def calcular_centros(bins):
	'''calcula un array con los puntos centros de un array de edges, para graficar en un plt.bar'''
	#print(bins)
	edge=bins[1]-bins[0]
	lista=[]
	for ind,value in enumerate(bins):
		if ind>=len(bins)-1:
			break
		res=bins[ind]+bins[ind+1]
		cp=res/2
		lista.append(cp)
	return np.array(lista)


def test_calculo_prob6():
	'''calculo de probabilidad a partir de un histograma de tp'''
	arr_tp=np.array([59.334335156250006, 52.124325, 58.445371875000006, 53.224098749999996, 72.76188, 95.9808975, 75.067515, 67.989710625, 262.036125, 39.611227500000005, 90.79911249999999])
	data,bins=np.histogram(arr_tp,numero)
	#print(bins)
	edgess=bins[2]-bins[1]
	prob=data/sum(data)
	bins=calcular_centros(bins)
	
	for a,b in zip(bins,prob):
		print(a,b)
	plt.bar(bins, width=edgess, height=prob,ec='black')
	
	plt.grid(True)
	plt.show()



if __name__=="__main__":
	#Prototipo:
	arr_tp=np.array([59.334335156250006, 52.124325, 58.445371875000006, 53.224098749999996, 72.76188, 95.9808975, 75.067515, 67.989710625, 262.036125, 39.611227500000005, 90.79911249999999])
	probabilidad, centros, ancho=calcular_probabilidad(arr_tp,20)
	fig, ax = plt.subplots()
	#ax.bar(centros, width=ancho, height=probabilidad,ec='black')
	ax.bar(centros, width=ancho, height=probabilidad,ec='black')
	prob=list(probabilidad)
	for i, (name, height) in enumerate(zip(centros, probabilidad)):
		ax.text(i, height, ' ' + str(round(name,2)), color='seashell', ha='center', va='top', rotation=-90, fontsize=18)

	# Creating the legend of the bars in the plot
	plt.legend(labels = ['legend example'])
	# Giving the tilte for the plot
	plt.title("title example")
	# Namimg the x and y axis
	plt.xlabel('xXample')
	plt.ylabel('yxample')
	plt.grid(True)
	
	

	plt.show()
else:
	print("Modulo Importado: [", os.path.basename(__file__), "]")
