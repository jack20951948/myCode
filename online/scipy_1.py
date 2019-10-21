import numpy as np
from scipy import linalg
A = np.array([[1,3,5],[2,5,1],[2,3,8]])  #產生矩陣
print(A)
print(linalg.inv(A))        #A的反矩陣
print(A.dot(linalg.inv(A)))      #dot:內積
