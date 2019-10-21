import random
import math
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import time
from pandas import DataFrame

def read_data():
    data = pd.read_csv('rock_data.csv')
    data_list = data.values.tolist()
    
    return data_list

def normalize(w):
    summ = 0
    for j in range(len(w)):
        summ += (w[j]**2)
    root = pow(summ, 0.5)
    weight = []
    for i in range(len(w)):
        weight.append(w[i]/root)
    return weight
    

def wta(data_list):
    wr = random.random()
    wg = random.random()
    wb = random.random()
    wh = random.random()
    w_list = normalize([wr, wg, wb, wh])

    score = 0
    for trainingData in data_list:
        normalized_data = normalize(trainingData)
        score += (w_list[0] * normalized_data[0] + w_list[1] * normalized_data[1] + w_list[2] * normalized_data[2] + w_list[3] * normalized_data[3])

    return score, w_list

def perceptron(weight, data, learninge_rate):
    


def main():
    data_list = read_data()
    k = 10

    wta_list = []
    for i in range(k):
        score, w_list = wta(data_list)
        wta_list.append([score, w_list])
    
    biggest = wta_list[0]
    b = 0
    for h in range(k):
        if wta_list[h] > biggest:
            biggest = wta_list[h]
            b = h
    print('big:', biggest)

    learninge_rate = 0.05
    perceptron(biggest[1], data_list, learninge_rate)


            



main()