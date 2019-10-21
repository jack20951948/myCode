import random
import math
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import time
from sklearn.cluster import KMeans
from pandas import DataFrame
from minisom import MiniSom

def read_data():
    data = pd.read_csv('nba_allPlayerData_1819.csv')
    data_list = data.values.tolist()
    
    return data_list

def plot_3d(data, color):
    plt.scatter([x[11] for x in data], [x[17] for x in data], c=color)  #REB14,AST18
    plt.show()
    fig = plt.figure()
    ax = Axes3D(fig)
    ax.scatter([x[8] for x in data],[x[11] for x in data],[x[17] for x in data],c=color)#PTS5,AST18,REB17
    plt.show()
    fig = plt.figure()
    ax = Axes3D(fig)
    ax.scatter([x[8] for x in data],[x[20] for x in data],[x[17] for x in data],c=color)#PTS5,REB17,STL20
    plt.show()
    fig = plt.figure()
    ax = Axes3D(fig)
    ax.scatter([x[11] for x in data],[x[17] for x in data],[x[20] for x in data],c=color)#PTS5,AST18,REB17
    plt.show()
    fig = plt.figure()
    ax = Axes3D(fig)
    ax.scatter([x[8] for x in data],[x[11] for x in data],[x[20] for x in data],c=color)#PTS5,AST18,REB17
    plt.show()

def main():
    raw_data = read_data()
    data = []
    for x in raw_data:
        x.pop(0)
        x.pop(0)
        data.append(x)
    print(data)
    # print(data) 
    # plt.scatter([x[7] for x in data], [x[17] for x in data], s=12)
    # plt.show()
    # fig = plt.figure()
    # ax = Axes3D(fig)
    # ax.scatter([x[16] for x in data],[x[17] for x in data],[x[7] for x in data])
    # plt.show()

    kmeans = KMeans(n_clusters=2, init = 'random', n_init = 1)
    kmeans = kmeans.fit(data)

    labels = kmeans.predict(data)
    centroids = kmeans.cluster_centers_ 

    # print('l:',labels)
    print('c:',centroids)
    plot_3d(data, labels)

    item = []
    for i in data:
        item.append([i[8], i[11], i[17], i[20]])

    print(item)

    som = MiniSom(6 ,6, 4, sigma=0.5, learning_rate=0.2)
    som.train_random(item, 400)
    result1 = som.activation_response(item)
    print('result1 are: \n', result1)


main()