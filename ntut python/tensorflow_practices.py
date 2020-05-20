import numpy as np

x = np.array([1,2,3,4,5,6])
y = x.astype('float64')
print(x)
print(type(x))
print(y.dtype)
print(y)

print('-----------------')
x = np.ones([2, 3])   
print(x) 
y = x.reshape([3, 2])    
print(y) 
z=np.array([[1,2,3,4], [5,6,7,8], [9,10,11,12], [13,14,15,16], [17,18,19,20]]) 
print(z[:,::-1])    #z[:,m:n:s]即取矩陣z 的所有行中，第m 到n-1 列資料，含左不含右。 
print(z[:,0]) 
print(z[:,1]) 
print(z[:,2:3])
