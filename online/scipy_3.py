import numpy as np
from scipy import linalg as la
A = np.array([[1,5,2],[2,4,1],[3,6,2]])
lna,v = la.eig(A)      #ㄍㄛ
l1,l2,l3 = lna
#Eigenvalue
print(l1,l2,l3)
print('--------------')
#Eigenvalue
print(v)
print('--------------')
print(v[:,0])
print(v[:,1])
print(v[:,2])
v1 = np.array(v[:,0]).T
print('--------------')
print(v1)
print(la.norm(A.dot(v1)-l1*v1))