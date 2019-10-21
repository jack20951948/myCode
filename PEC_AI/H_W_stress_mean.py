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
        print(dataframe_da_n.tail())

    with open('PEC_AI\H_W_stress_s.csv', mode='r') as str_data_s:
        stress_data_s = str_data_s.read()
        #print(type(stress_data_s))

        list_da_s = stress_data_s.split('\n')
        list_da_s = list(map(str2list,list_da_s))
        #print(type(list_da_s))

        dataframe_da_s = pd.DataFrame(list_da_s[:-1][:], columns = ['W','H'])
        #print(type(dataframe_da_s))
        print(dataframe_da_s.tail())
    
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

def data_split(data):
    random.shuffle(data)
    train_data = data[:100]
    test_data = data[100:]
    return train_data, test_data

def test_data(test, mean_yes, mean_no):
    predict_yes = []
    predict_no = []
    for i in test:
        if ((pow(i[0] - mean_yes[0], 2) + pow(i[1] - mean_yes[1], 2))) < ((pow(i[0] - mean_no[0], 2) + pow(i[1] - mean_no[1], 2))):
            predict_yes.append(i)
        else:    
            predict_no.append(i)
    return predict_yes, predict_no



def main():
    wh_n, wh_s = read_data()
    plot(wh_n, wh_s)
    wh_n_train_data, wh_n_test_data = data_split(wh_n)
    wh_s_train_data, wh_s_test_data = data_split(wh_s)

    n_train_data_mean = [statistics.mean(wh_n_train_data[0]), statistics.mean(wh_n_train_data[1])]  #訓練資料中點
    s_train_data_mean = [statistics.mean(wh_s_train_data[0]), statistics.mean(wh_s_train_data[1])]
    print(n_train_data_mean, s_train_data_mean)

    n_predict_yes, n_predict_no = test_data(wh_n_test_data, n_train_data_mean, s_train_data_mean)
    s_predict_yes, s_predict_no = test_data(wh_s_test_data, s_train_data_mean, n_train_data_mean)
    plot(n_predict_yes, n_predict_no)
    plot(s_predict_yes, s_predict_no)

    predict_no = n_predict_no + s_predict_no
    plot(n_predict_yes, s_predict_yes, predict_no)



main()