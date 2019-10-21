import pandas as pd
import numpy as np
import random
import matplotlib.pyplot as plt
from pandas import DataFrame

def read_data():
    data = pd.read_csv('rock_data.csv')
    data_list = data.values.tolist()
    return data_list

def normalize(list):
    summ = 0
    for j in range(len(list)):
        summ += (list[j]**2)
    root = summ**0.5
    normal = []
    for i in range(len(list)):
        normal.append(list[i]/root)
    return normal

def perceptron(data, k, learning_rate=10):
    data_normal = []
    for i in range(len(data)):
        data_normal.append(normalize(data[i]))
    for i in range(k):
        wr = random.random()
        wg = random.random()
        wb = random.random()
        wh = random.random()
        globals()['w{}'.format(i)] =  normalize([wr, wg, wb, wh])    

    for d in data_normal:
        perceptron_number = 0
        biggest = 0
        for j in range(k):
            weight = globals()['w{}'.format(j)]
            score = (weight[0]*d[0] + weight[1]*d[1] + weight[2]*d[2] + weight[3]*d[3])
            if score > biggest:
                biggest = score
                perceptron_number = j

        print(perceptron_number)
        for q in range(len(globals()['w{}'.format(perceptron_number)])):
            globals()['w{}'.format(perceptron_number)][q] = learning_rate * (d[q] - globals()['w{}'.format(perceptron_number)][q])

    result = []
    for d in data_normal:
        perceptron_number = 0
        for j in range(k):
            biggest = 0
            weight = globals()['w{}'.format(j)]
            score = (weight[0]*d[0] + weight[1]*d[1] + weight[2]*d[2] + weight[3]*d[3])
            if score > biggest:
                biggest = score
                perceptron_number = j
        d.append(perceptron_number)
        result.append(d)
    # print(result)
    return result    

def main():
    data_list = read_data()
    result = perceptron(data_list, 6)

    #plot data
    color = [x[4] for x in result]
    print(color)
    plt.scatter([x[1] for x in result], [x[0] for x in result], s=12, c=color)
    plt.show()
    plt.scatter([x[2] for x in result], [x[1] for x in result], s=12, c=color)
    plt.show()
    plt.scatter([x[3] for x in result], [x[0] for x in result], s=12, c=color)
    plt.show()

main()