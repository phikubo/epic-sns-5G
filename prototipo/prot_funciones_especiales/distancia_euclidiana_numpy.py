#import
#recipes: https://semantive.com/high-performance-computation-in-python-numpy-2/
#list to numpy: https://www.geeksforgeeks.org/numpy-asarray-in-python/
import numpy as np

def dummy_mat(mat_v, mat_u):
   return [sum((v_i - u_i)**2 for v_i, u_i in zip(v, u))**0.5 for v, u in zip(mat_v, mat_u)]

def bare_numpy_mat(mat_v, mat_u):
   return np.sqrt(np.sum((mat_v - mat_u) ** 2, axis=1))

def l2_norm_mat(mat_v, mat_u):
   return np.linalg.norm(mat_v - mat_u, axis=1)

def scipy_distance_mat(mat_v, mat_u):
   # Unfortunately, the scipy_distance only works on 1D-arrays, so we are not able to vectorize it again.
   return list(map(distance.euclidean, mat_v, mat_u))

def einsum_mat(mat_v, mat_u):
   mat_z = mat_v - mat_u
   return np.sqrt(np.einsum('ij,ij->i', mat_z, mat_z))

if __name__=="__main__":
	#Prototipo:
	pass
else:
	print("Modulo <escribir_nombre> importado")
