#import
import matplotlib.pyplot as plt
from matplotlib.patches import RegularPolygon
import numpy as np
import math

if __name__=="__main__":
	#Prototipo:
	radio=100
	coef=2*radio
	coord = [[0,0,0]]
	hcoord = [coef*c[0] for c in coord]
	vcoord = [2. * np.sin(np.radians(60)) * (coef*c[1] - coef*c[2]) /3. for c in coord]
	colors = [["Green"]]
	labels = [['1)0,0,0']]
	fig, ax = plt.subplots(1)
	ax.set_aspect('equal')
	
	'''for x, y, c, l in zip(hcoord, vcoord, colors, labels):
		color = c[0].lower()
		hex = RegularPolygon((x, y), numVertices=6, radius=radio, orientation=np.radians(30), facecolor=color, alpha=0.2, edgecolor='k')
		ax.add_patch(hex)
		ax.text(x, y+0.2, l[0], ha='center', va='center', size=20)
	ax.scatter(hcoord, vcoord, c=[c[0].lower() for c in colors], alpha=0.5)
	'''
	color = colors[0][0].lower()
	hexagonal=RegularPolygon((0, 0), numVertices=6, radius=radio, orientation=np.radians(30), facecolor=color,alpha=0.2, edgecolor='k')
	ax.add_patch(hexagonal)
	#ax.text(0, 0, ["holi"], ha='center', va='center', size=20)
	ax.scatter(0, 0, alpha=0.5)
	plt.grid(True)
	plt.savefig("uma_celda.png")
	plt.show()


else:
	print("Modulo <escribir_nombre> importado")
