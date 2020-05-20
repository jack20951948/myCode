import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import random
import statistics

def str2list(x):        #list副程式
    ans = x.split(',')
    return ans

def read_data():
    with open('PEC_AI\H_W_stress_n.csv', mode='r') as str_data_n:
        stress_data_n = str_data_n.read()
        #print(type(stress_data_n))

        list_da_n = stress_data_n.split('\n')
        list_da_n = list(map(str2list,list_da_n))
        #print(type(list_da_n))

        dataframe_da_n = pd.DataFrame(list_da_n[:-1][:], columns = ['W','H'])
        #print(type(dataframe_da_n))
        #print(dataframe_da_n.tail())

    with open('PEC_AI\H_W_stress_s.csv', mode='r') as str_data_s:
        stress_data_s = str_data_s.read()
        #print(type(stress_data_s))

        list_da_s = stress_data_s.split('\n')
        list_da_s = list(map(str2list,list_da_s))
        #print(type(list_da_s))

        dataframe_da_s = pd.DataFrame(list_da_s[:-1][:], columns = ['W','H'])
        #print(type(dataframe_da_s))
        #print(dataframe_da_s.tail())
    
    x_w_n = dataframe_da_n['W'].values.tolist()
    y_h_n = dataframe_da_n['H'].values.tolist()
    x_w_s = dataframe_da_s['W'].values.tolist()
    y_h_s = dataframe_da_s['H'].values.tolist()
    
    x_w_n_i = list(map(float,x_w_n))  #一維list
    y_h_n_i = list(map(float,y_h_n))
    x_w_s_i = list(map(float,x_w_s))
    y_h_s_i = list(map(float,y_h_s))  
    
    wh_n = [[]*2 for range in range(len(x_w_n_i))]   #二維list
    wh_s = [[]*2 for range in range(len(x_w_s_i))]
    for i in range(0,len(x_w_n_i)):
        wh_n[i].append(x_w_n_i[i])         
        wh_n[i].append(y_h_n_i[i])

    for i in range(0,len(x_w_s_i)):
        wh_s[i].append(x_w_s_i[i])         
        wh_s[i].append(y_h_s_i[i])
    # print(wh_n) 
    # print(wh_s)
    return wh_n, wh_s

def plot(class_1=None, class_2=None, class_3=None):
    plt.scatter([x[1] for x in class_1],[x[0] for x in class_1],s=15, color='b')
    plt.scatter([x[1] for x in class_2],[x[0] for x in class_2],s=15, color='g')
    if class_3 != None:
        plt.scatter([x[1] for x in class_3],[x[0] for x in class_3],s=15, color='r')
    plt.show()


def test_data(test, mean_1, mean_2):
    class_1 = []
    class_2 = []
    temp_list = []
    while 1:
        for i in test:
            if ((pow(i[0] - mean_1[0], 2) + pow(i[1] - mean_1[1], 2))) < ((pow(i[0] - mean_2[0], 2) + pow(i[1] - mean_2[1], 2))):
                class_1.append(i)
            else:    
                class_2.append(i)
        if class_1 == temp_list:
            break
        else:
            temp_list = class_1
            mean_1 = [statistics.mean(class_1[0]), statistics.mean(class_1[1])]
            mean_2 = [statistics.mean(class_2[0]), statistics.mean(class_2[1])]
        
        
    return class_1, class_2



def main():
    wh_n, wh_s = read_data()
    plot(wh_n, wh_s)

    data = wh_n + wh_s
    random.shuffle(data)
    start_mean_1 = data[0][:]
    start_mean_2 = data[1][:]

    class_1, class_2 = test_data(data, start_mean_1, start_mean_2)
    plot(class_1, class_2)


main()