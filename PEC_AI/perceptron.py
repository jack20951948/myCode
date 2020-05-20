import pandas as pd
import numpy as np
import random
import time
import matplotlib.pyplot as plt
from pandas import DataFrame

def read_data():
    data_n_stress = pd.read_csv('AI-Practice02-Data-notStressed.csv')
    data_stress = pd.read_csv('AI-Practice02-Data-Stressed.csv')
    n_stress_li = data_n_stress.values.tolist()
    stress_li = data_stress.values.tolist()
    return n_stress_li, stress_li

def plot_data(class_1, class_2, fault=None):
    plt.scatter([x[1] for x in class_1], [x[0] for x in class_1], s=15, c='g')
    plt.scatter([x[1] for x in class_2], [x[0] for x in class_2], s=15, c='b')
    if fault!=None:
        plt.scatter([x[1] for x in fault], [x[0] for x in fault], s=15, c='r')
    plt.show()

def train_data_classify(class_0, class_1):
    df_ns = pd.DataFrame(class_0)
    df_s = pd.DataFrame(class_1)
    df_ns.insert(2, '', 0)
    df_s.insert(2, '', 1)
    class_0 = df_ns.values.tolist()
    class_1 = df_s.values.tolist()
    return class_0, class_1

def split_data(data, percent):
    random.shuffle(data)
    train_data = []
    test_data = []
    for i in range(0, int(len(data)*percent)):
        train_data.append(data[i])
    for j in range(int(len(data)*percent), int(len(data))):
        test_data.append(data[j])
    return train_data, test_data

def perceptron(train_data, test_data):
    def step_function(y):
        return 0 if y <= 0 else 1

    def testing(data):
        fault_count = 0
        fault = []
        for i in data:
            y_hat = step_function(w1 * i[0] + w2 * i[1] + w0)
            if y_hat != i[2]:
                fault_count += 1
                fault.append(i)
        return fault, fault_count

    random.shuffle(train_data)
    w0 = random.uniform(0, 1)
    w1 = random.uniform(0, 1)
    w2 = random.uniform(-1, 1)
    learning_rate = 0.0005

    
    iteration = 0
    while True:
        fault, fault_count = testing(test_data)
        if fault_count < (len(test_data)*0.1//1):
            print('converged')
            break
        elif iteration > 50000:
            print("didn't converged")
            break
        for data in train_data:
            y_hat = step_function(w1 * data[0] + w2 * data[1] + w0)
            w1 += learning_rate * (data[2] - y_hat) * data[0]
            w2 += learning_rate * (data[2] - y_hat) * data[1]
            w0 += learning_rate * (data[2] - y_hat)
        iteration += 1
    print('w1:', w1)
    print('w2:', w2)
    print('w0:', w0)
    print('accuracy:',1-(len(fault)/len(test_data)))
    return fault
    
def main():
    n_stress_li, stress_li = read_data()    #read_data
    n_stress_li, stress_li = train_data_classify(n_stress_li, stress_li)    #mark the data
    plot_data(n_stress_li, stress_li)   #plot all data
    train_n_s, test_n_s = split_data(n_stress_li, 0.5)   #split data of no stressed
    train_s, test_s = split_data(stress_li, 0.5)   #split data of stressed
    train_data = train_n_s + train_s
    test_data = test_n_s + test_s

    start_time = time.time()
    fault = perceptron(train_data, test_data)
    run_time = time.time() - start_time
    plot_data(test_n_s, test_s, fault)
    print('run time:',run_time)

main()


