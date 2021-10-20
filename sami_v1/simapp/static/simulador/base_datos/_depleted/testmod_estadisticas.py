#import
import os
import pytest
import numpy as np
import matplotlib.pyplot as plt

def calcular_probabilidad(ocurrencia, num_realizaciones, bins):
	'''Calcula la probabilidad de datos estadisticos mediante la ocurrencia, numero de realizaciones y datos objetivos.'''
	arr_tp=np.array([59.334335156250006, 52.124325, 58.445371875000006, 53.224098749999996, 72.76188, 95.9808975, 75.067515, 67.989710625, 262.036125, 39.611227500000005, 90.79911249999999])
	data,bins=np.histogram(arr_tp,20)
	#print(bins)
	edgess=bins[2]-bins[1]
	prob=data/sum(data)
	bins=calcular_centros(bins)
	
	for a,b in zip(bins,prob):
		print(a,b)
	plt.bar(bins, width=edgess, height=prob,ec='black')
	
	plt.grid(True)
	plt.show()

	return probabilidad

def calcular_centros(bins):
	'''calcula un array con los centros de un array de edges'''
	edge=bins[1]-bins[0]
	lista=[]
	for ind,value in enumerate(bins):
		if ind>=len(bins)-1:
			break
		res=bins[ind]+bins[ind+1]
		cp=res/2
		lista.append(cp)
	return np.array(lista)
	
def test_calculo_prob1():
	'''prueba de la funcion de probabilidad, con los siguientes datos.
	Suponga que tiene un arreglo de TP <arr_tp>, encuentre la probabilidad.
	P(X=arr_tp_{i})=OCURRENCIA/TOTAL_valores'''
	arr_tp=np.array([10,20,30,15,25,34,50,16,18,19,12,34,23,13,24,32,23,13,24,14,15,16])
	ocurrencia, limites=0,0
	data_tp, bin_tp=np.histogram(arr_tp)
	print(np.shape(data_tp), np.shape(bin_tp))

	print(data_tp)
	print(bin_tp)

	plt.figure()
	plt.plot(bin_tp[:-1],data_tp)
	plt.hist(arr_tp)

	plt.figure()
	prob1=data_tp/len(arr_tp)
	print(prob1, sum(prob1))
	print(len(data_tp), len(prob1))
	plt.hist(prob1, cumulative=True)
	plt.figure()
	plt.plot(bin_tp[:-1],prob1, '-*')
	'''No se puede obtener probabilidad con el valor neto de tp, solo con una ocurrencia.
	Lo mas conveniente es contar ocurrencia y obtener probabilidad de ella. Tampoco se recomienda contar ocurrencia manualmente pues el rango de conteno puede ser
	del tamano del numero de simulaciones y esto no es practico.'''
	prob2=arr_tp/len(arr_tp)
	print(prob2, sum(prob2))
	
	
	plt.show()

def test_calculo_prob2():
	'''prueba de la funcion de probabilidad, con los siguientes datos.
	Suponga que tiene un arreglo de TP <arr_tp>, encuentre la probabilidad.
	P(X=arr_tp_{i})=OCURRENCIA/TOTAL_valores'''
	arr_tp=np.array([59.334335156250006, 52.124325, 58.445371875000006, 53.224098749999996, 72.76188, 95.9808975, 75.067515, 67.989710625, 262.036125, 39.611227500000005, 90.79911249999999])
	arr_tp2=np.sort(arr_tp)
	data,bins=np.histogram(arr_tp)
	print(data)
	print(bins)
	total=sum(arr_tp)
	probabilidades=arr_tp/total

	
	#plt.title("tp vs probabilidades")
	#plt.plot(arr_tp,probabilidades,"-o")

	#plt.figure()
	#plt.title(" probabilidades vs tp")
	#plt.plot(probabilidades,arr_tp,"-o")

	plt.figure()
	plt.grid(True)
	plt.title("bar tp vs probabilidades")
	plt.bar(arr_tp,probabilidades)

	plt.figure()
	plt.grid(True)
	plt.title("bar tp vs probabilidades cum")
	plt.bar(arr_tp,np.cumsum(probabilidades))


	plt.figure()
	plt.grid(True)
	plt.title("hist tp")
	plt.hist(arr_tp, density=True)

	plt.figure()
	plt.grid(True)
	plt.title("hist tp2")
	plt.hist(arr_tp, cumulative=True,density=True)
	
	plt.figure()
	plt.grid(True)
	plt.title("probabilidades histogramada")
	plt.hist(probabilidades, cumulative=True)

	plt.figure()
	plt.grid(True)
	plt.title("arr_tp histograma")
	plt.hist(arr_tp)
	#
	plt.grid(True)
	plt.show()
	

def test_calculo_prob3():
	'''prueba de la funcion de probabilidad, con los siguientes datos.
	Suponga que tiene un arreglo de TP <arr_tp>, encuentre la probabilidad.
	P(X=arr_tp_{i})=OCURRENCIA/TOTAL_valores'''
	arr_tp=np.array([59.334335156250006, 52.124325, 58.445371875000006, 53.224098749999996, 72.76188, 95.9808975, 75.067515, 67.989710625, 262.036125, 39.611227500000005, 90.79911249999999])
	arr_tp2=np.sort(arr_tp)
	data,bins=np.histogram(arr_tp2)
	print(data)
	print(bins)

	
	total=sum(arr_tp2)
	probabilidades=arr_tp2/total
	data2,bins2=np.histogram(probabilidades)
	print(probabilidades)
	print(data2)
	print(bins2)

	plt.figure()
	plt.grid(True)
	plt.title("bar tp vs probabilidades")
	plt.bar(arr_tp,probabilidades)

	plt.grid(True)
	plt.show()


def test_calculo_prob4():
	'''prueba de la funcion de probabilidad, con los siguientes datos.
	Suponga que tiene un arreglo de TP <arr_tp>, encuentre la probabilidad.
	P(X=arr_tp_{i})=OCURRENCIA/TOTAL_valores
	
	>>> x=np.array([10,15,20,25,30,35,40,45])
	>>> f=np.array([30,60,80,50,30,20,10,5])
	>>> p=np.array([0.0211,0.0421,0.0561,0.0351,0.0211,0.014,0.007,0.0035])

	'''
	arr_tp=np.array([59.334335156250006, 52.124325, 58.445371875000006, 53.224098749999996, 72.76188, 95.9808975, 75.067515, 67.989710625, 262.036125, 39.611227500000005, 90.79911249999999])
	arr_tp2=np.sort(arr_tp)
	data,bins=np.histogram(arr_tp2)
	print(data)
	print(bins)

	plt.hist(arr_tp2, density=True)
	
	total=sum(arr_tp2)
	probabilidades=arr_tp2/total
	data2,bins2=np.histogram(probabilidades)
	print(probabilidades)
	print(data2)
	print(bins2)

	plt.figure()
	plt.grid(True)
	plt.title("bar tp vs probabilidades")
	plt.bar(bins,bins2)

	# = 500
	plt.figure()
	data = arr_tp.copy()
	count, bins_count = np.histogram(data, bins=10)
	pdf = count / sum(count)
	cdf = np.cumsum(pdf)
	plt.plot(bins_count[1:], pdf, color="red", label="PDF")
	plt.plot(bins_count[1:], cdf, label="CDF")
	plt.hist(arr_tp2, density=True, cumulative=True)
	plt.legend()
 


	plt.grid(True)
	plt.show()


def test_calculo_prob5():
	'''prueba de la funcion de probabilidad, con los siguientes datos.
	Suponga que tiene un arreglo de TP <arr_tp>, encuentre la probabilidad.
	P(X=arr_tp_{i})=OCURRENCIA/TOTAL_valores
	
	>>> x=np.array([10,15,20,25,30,35,40,45])
	>>> f=np.array([30,60,80,50,30,20,10,5])
	>>> p=np.array([0.0211,0.0421,0.0561,0.0351,0.0211,0.014,0.007,0.0035])

	'''
	arr_tp=np.array([59.334335156250006, 52.124325, 58.445371875000006, 53.224098749999996, 72.76188, 95.9808975, 75.067515, 67.989710625, 262.036125, 39.611227500000005, 90.79911249999999])
	arr_tp2=np.sort(arr_tp)
	data,bins=np.histogram(arr_tp2)
	edges=bins[2]-bins[1]
	print(data)
	print(bins)

	prob=data/len(data)
	
	
	plt.figure()
	plt.hist(arr_tp2)

	plt.figure()
	plt.hist(arr_tp2, density=True)
	


	plt.figure()
	plt.bar(bins[:-1], width=edges, height=prob)


	plt.grid(True)
	plt.show()
	

def calcular_centros(bins):
	'''calcula un array con los centros de un array de edges'''
	edge=bins[1]-bins[0]
	lista=[]
	for ind,value in enumerate(bins):
		if ind>=len(bins)-1:
			break
		res=bins[ind]+bins[ind+1]
		cp=res/2
		lista.append(cp)
	return np.array(lista)
		
	#cm=np.cumsum(bins)
	#print(1,cm)
	#cp=cm[1:]
	#return cp/2

def test_calculo_prob6():
	'''calculo de probabilidad a partir de un histograma de tp'''
	arr_tp=np.array([59.334335156250006, 52.124325, 58.445371875000006, 53.224098749999996, 72.76188, 95.9808975, 75.067515, 67.989710625, 262.036125, 39.611227500000005, 90.79911249999999])
	data,bins=np.histogram(arr_tp,20)
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
	#test_calculo_prob1()
	#test_calculo_prob2()
	#test_calculo_prob3()
	#test_calculo_prob4()
	#test_calculo_prob5()
	test_calculo_prob6()
else:
	print("Modulo Importado: [", os.path.basename(__file__), "]")
