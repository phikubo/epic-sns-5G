import matplotlib.pyplot as plt
from matplotlib.patches import RegularPolygon
import numpy as np
import math
#http://magomar.github.io/deludobellico//programming/java/hexagonal-maps/2013/10/10/mapas-hexagonales-2.html
#https://joseguerreroa.wordpress.com/2016/11/17/como-producir-rejillas-grid-hexagonales-mediante-pyqgis/
#https://gamedevelopment.tutsplus.com/es/tutorials/introduction-to-axial-coordinates-for-hexagonal-tile-based-games--cms-28820
#https://gamedevelopment.tutsplus.com/es/tutorials/hexagonal-character-movement-using-axial-coordinates--cms-29035
 
#modificado por: John Michael (phikubo)

'''La modificación consiste en que se puede escalar los hexagonos al radio que uno fije, en ese sentido
la grilla de hexagono mantiene su forma.

Por el momento el script solo permite 7 celdas, 

En la próxima entrega se hara sectorización (por 3) y se permitirá varios niveles (vueltas respecto al origen) en la grilla.''' 

radio=100
def calcular_radio_externo(radio):
	#print(math.sin(30), math.radians(30), math.degrees(30))
	lado=radio*2*math.sin(math.radians(30))
	#print("lado", lado, radio)
	radio_externo=radio+lado/2
	return radio_externo
	
#calcular_radio_externo(radio)
rae=calcular_radio_externo(radio)
print(rae)
coef=rae
 
 
def generar_lista(coordenadas,rae):
	#funcion que no se implementa por que es inutil
	for j in range(len(coordenadas)):
		for m in range(len(coordenadas[0])):
			c=coordenadas[j][m]
			print(c)


coord = [[0,0,0],[0,1,-1],[-1,1,0],[-1,0,1],[0,-1,1],[1,-1,0],[1,0,-1]]
# Horizontal cartesian coords
hcoord = [coef*c[0] for c in coord]

# Vertical cartersian coords
vcoord = [2. * np.sin(np.radians(60)) * (coef*c[1] - coef*c[2]) /3. for c in coord]
print(hcoord)
print(vcoord)	 
 
#coord = [[0,0,0],[0,1,-1],[-1,1,0],[-1,0,1],[0,-1,1],[1,-1,0],[1,0,-1]]
#coordenadas cubicas ejes axiales para grilla hexagonales
#cual es la relacion entre el tres y el radio dos.
###coord = [[0,0,0],[0,3,-3],[-3,3,0],[-3,0,3],[0,-3,3],[3,-3,0],[3,0,-3]]
#cuales serían las coordenadas para una grilla mas grande. Existe algun algoritmo para sacar las 
#coordenadas de forma dinamica?. Que cada hexagono se ubique del centro hacia afuera y cada suma
#se ubique contra las manecillas del reloj.
colors = [["Green"],["Blue"],["Green"],["Green"],["Red"],["Green"],["Green"]]
labels = [['1)0,0,0'],['2)0,3,-3'],['3)-3,3,0'],['4)-3,0,3'],['5)0,-3,3'],['6)3,-3,0'],['7)3,0,-3']]
#orden = [ [],[],[],[],[],[],[] ]
# Horizontal cartesian coords
##hcoord = [c[0] for c in coord]
 
# Vertical cartersian coords
##vcoord = [2. * np.sin(np.radians(60)) * (c[1] - c[2]) /3. for c in coord]

fig, ax = plt.subplots(1)
ax.set_aspect('equal')

# Add some coloured hexagons
for x, y, c, l in zip(hcoord, vcoord, colors, labels):
    color = c[0].lower()  # matplotlib understands lower case words for colours
    hex = RegularPolygon((x, y), numVertices=6, radius=radio, #0.67
                         orientation=np.radians(30), #con 60 grados funciona perfecto, pero las coordenadas cambian. Antes 30
                         facecolor=color, alpha=0.2, edgecolor='k')
                         #cambiar radius=2. / 3. , cuando se usa coord_0
    ax.add_patch(hex)
    # Also add a text label
    ax.text(x, y+0.2, l[0], ha='center', va='center', size=20)

# Also add scatter points in hexagon centres
ax.scatter(hcoord, vcoord, c=[c[0].lower() for c in colors], alpha=0.5)
plt.grid(True)
plt.savefig("grillahex.png")
plt.show()



 
 
  
