import numpy as np

a = np.zeros((10,3))
print(a)
print('-----------------')
b = a.T   #轉置
print(b)
print('-----------------')
c = np.reshape(b, (5,6))
print(c)

#-----------------------------
print('-----------------')
d = np.arange(10)
print(d)
print('-----------------')
d = d.reshape((2,5))
print(d)
print('-----------------')
print(np.ravel(d))