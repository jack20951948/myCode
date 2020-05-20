import numpy as np
print('np.陣列')

myarr = np.array([[1,2,3],[4,5,6]])  #np 陣列
print(myarr)

myarr_zero = np.zeros((3,5),dtype = np.int16)
print(myarr_zero)

#---------------------------------
print('-----------')
print('np.矩陣')

my_onedim = np.arange(15,dtype = np.int64)  #np 一維矩陣
print(my_onedim)

#---------------------------------
print('-----------')
print('np.建立矩陣')
my_reshape_arr = np.arange(15,dtype = np.int64).reshape((3,5))
print(my_reshape_arr)

#建立巴等分陣列，min=1，max=100
my_slice_arr = np.linspace(1,100,8)
print(my_slice_arr)

#建立隨機在0~1之間的矩陣
my_random_arr = np.random.random((2,3))
print(my_random_arr)

#--------------------------------
#矩陣運算
print('------------------')
print('矩陣運算')

a = np.arange(25).reshape((5,5))
b = np.arange(25).reshape((5,5))

print(a+b)
print(a-b)
print(a*b)
print(a/b)
print(a**2)
print(a<b)
print(a>b)
print(a.dot(b)) #a,b內積