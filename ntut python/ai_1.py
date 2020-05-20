A = '10'
B = "10"
C = 100.04
D = A + B
E= ['345',1,3,"simple",{1:10}]

print(True or not True)

print('x' not in 'abcdefg')

print (len([[1,2,3,4,'a'],]))

print('Understanding Find command fully! '.find('f'))

print([['a',1],['b',1],'c',3][1][1])


ls = [1,2,3,4,5]
print(ls==ls[0:len(ls)])

ls = [1,2,3,4,5]
print(ls[:3:-1])  #不知道三姣

print(list(range(6)))


print([x**2 for x in range(1,5) if x%3 == 0])

#method: 副程式叫做def 副程式的集合就叫做Class class裡面包含的副程式就叫做method



ls1 = ['a']
print(ls1*11)

ls1 = ['a'*11]
print(ls1)


def get_larger(x,y):
    if x > y:
        ans = x
    
    else:
        ans = y
    return ans  

m = get_larger(3,4)

print(m)


x=2
y=4
z=10
def func(x,y):
    x+=1
    y=y*4
    w=x+y+z
    return w

res = func(x,5)

print(res)
print(x)
print(y)
print(z)
print(w)



def simple_devide(a,b)
    

m1 = simple_devide(5,2)
m2 = simple_devide(11,2)
print(m1)
print(m2)


