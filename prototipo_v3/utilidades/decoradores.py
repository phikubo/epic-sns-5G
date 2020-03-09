#import

def decorador_rastrear(func):
	def funcion_decorada(*args, **kwargs):
		print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>En la función",func.__name__+"()")
		value=func(*args, **kwargs)
		print("Ok<<<<<<<<<<<<<<<<<<<<<<<<<<")
		return value
	return funcion_decorada


if __name__=="__main__":
	#Prototipo:
	pass
else:
	print("Modulo <escribir_nombre> importado")
