tp6 = tuple([66,22,3,46,5,65,7,83,19])
print(tp6)

list1 = list(tp6)
list1.sort()   #排序串列(由小到大排列)
print(list1)
print('---------')

tp8 = tuple(list1)
tp9 = tuple(list1)

print(tp8)
print(tp8 == tp9)    #比較兩個數組tuple

#-------------------------------------------
print('------set-------')
st1 = set()    #空集合
st2 = set([1,2,3,4,5])    #串列轉集合
print(st2)
st3 = {'a','b','c','d','e'}  #沒有按照順序，隨機排
print(st3)
print('-------------')

st3.add('f')     #加上一個集合(從前面加)
print(st3)

st3.remove('d')   #移除一個集合
print(st3)
print('--------------')
print(st3.union(st2))         #聯集

st5 = {'a','b','c','d','e'}
print(st3.intersection(st5))  #交集
print(st3.difference(st5))    #差集