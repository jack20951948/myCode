import csv

def str2list(x):        #list副程式
    ans = x.split(',')
    return ans

f = open('csv_yob_08_17.csv','w',newline='')  #不加newline會有空行
f.close()

for i in range(2008,2018):
    with open('names\yob{}.txt'.format(i), mode='r') as bn_name:  #將i丟入大括號
        data = bn_name.read()
        print(type(data))

        list_da = data.split('\n')
        list_da = list(map(str2list,list_da))
        print(len(list_da))

    for j in range(len(list_da)):  #插入年份欄
        list_da[j].append('{}'.format(i))
    
    print(list_da[0:4])

    f = open('csv_yob_08_17.csv','a',newline='')  #不加newline會有空行
    w = csv.writer(f)
    w.writerows(list_da[0:100])   #各年只抓前一百筆資料
    f.close()

# with open('names\yob2017.txt', mode='r') as bn_2017:
#     data = bn_2017.read()
#     print(type(data))

#     list_da_17 = data.split('\n')
#     list_da_17 = list(map(str2list,list_da_17))
#     print(len(list_da_17))

#     for i in range(len(list_da_17)):  #插入年份欄
#         list_da_17[i].append('2017')
    
#     print(list_da_17[0:4])

# with open('names\yob2016.txt', mode='r') as bn_2016:
#     data = bn_2016.read()
#     print(type(data)) 

#     list_da_16 = data.split('\n')
#     list_da_16 = list(map(str2list,list_da_16))
#     print(len(list_da_16))

#     for i in range(len(list_da_16)):  #插入年份欄
#         list_da_16[i].append('2016')
    
#     print(list_da_16[0:4])

# with open('names\yob2015.txt', mode='r') as bn_2015:
#     data = bn_2015.read()
#     print(type(data)) 

#     list_da_15 = data.split('\n')
#     list_da_15 = list(map(str2list,list_da_15))
#     print(len(list_da_15))

#     for i in range(len(list_da_15)):  #插入年份欄
#         list_da_15[i].append('2015')
    
#     print(list_da_15[0:4])

# with open('names\yob2014.txt', mode='r') as bn_2014:
#     data = bn_2014.read()
#     print(type(data)) 

#     list_da_14 = data.split('\n')
#     list_da_14 = list(map(str2list,list_da_14))
#     print(len(list_da_14))

#     for i in range(len(list_da_14)):  #插入年份欄
#         list_da_14[i].append('2014')
    
#     print(list_da_14[0:4])

# with open('names\yob2013.txt', mode='r') as bn_2013:
#     data = bn_2013.read()
#     print(type(data)) 

#     list_da_13 = data.split('\n')
#     list_da_13 = list(map(str2list,list_da_13))
#     print(len(list_da_13))

#     for i in range(len(list_da_13)):  #插入年份欄
#         list_da_13[i].append('2013')
    
#     print(list_da_13[0:4])

# with open('names\yob2012.txt', mode='r') as bn_2012:
#     data = bn_2012.read()
#     print(type(data)) 

#     list_da_12 = data.split('\n')
#     list_da_12 = list(map(str2list,list_da_12))
#     print(len(list_da_12))

#     for i in range(len(list_da_12)):  #插入年份欄
#         list_da_12[i].append('2012')
    
#     print(list_da_12[0:4])

# with open('names\yob2011.txt', mode='r') as bn_2011:
#     data = bn_2011.read()
#     print(type(data)) 

#     list_da_11 = data.split('\n')
#     list_da_11 = list(map(str2list,list_da_11))
#     print(len(list_da_11))

#     for i in range(len(list_da_11)):  #插入年份欄
#         list_da_11[i].append('2011')
    
#     print(list_da_11[0:4])

# with open('names\yob2010.txt', mode='r') as bn_2010:
#     data = bn_2010.read()
#     print(type(data)) 

#     list_da_10 = data.split('\n')
#     list_da_10 = list(map(str2list,list_da_10))
#     print(len(list_da_10))

#     for i in range(len(list_da_10)):  #插入年份欄
#         list_da_10[i].append('2010')
    
#     print(list_da_10[0:4])

# with open('names\yob2009.txt', mode='r') as bn_2009:
#     data = bn_2009.read()
#     print(type(data)) 

#     list_da_09 = data.split('\n')
#     list_da_09 = list(map(str2list,list_da_09))
#     print(len(list_da_09))

#     for i in range(len(list_da_09)):  #插入年份欄
#         list_da_09[i].append('2009')
    
#     print(list_da_09[0:4])

# with open('names\yob2008.txt', mode='r') as bn_2008:
#     data = bn_2008.read()
#     print(type(data)) 

#     list_da_08 = data.split('\n')
#     list_da_08 = list(map(str2list,list_da_08))
#     print(len(list_da_08))

#     for i in range(len(list_da_08)):  #插入年份欄
#         list_da_08[i].append('2008')
    
#     print(list_da_08[0:4])


# f = open('csv_yob_08_17.csv','w',newline='')  #不加newline會有空行
# w = csv.writer(f)
# w.writerows(list_da_17)
# w.writerows(list_da_16)
# w.writerows(list_da_15)
# w.writerows(list_da_14)
# w.writerows(list_da_13)
# w.writerows(list_da_12)
# w.writerows(list_da_11)
# w.writerows(list_da_10)
# w.writerows(list_da_09)
# w.writerows(list_da_08)
# f.close()