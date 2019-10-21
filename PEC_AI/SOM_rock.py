import pandas as pd
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from mpl_toolkits.mplot3d import Axes3D
from minisom import MiniSom
import numpy as np

def read_data():
    data = pd.read_csv('rock_data.csv')
    data_list = data.values.tolist()
    
    return data_list

def plot3d(datalist, labels):
    fig = plt.figure()
    ax = Axes3D(fig)
    ax.scatter([x[1] for x in datalist], [x[2] for x in datalist], [x[3] for x in datalist], c=labels)
    plt.show()

def main():
    data_list = read_data()

    kmeans = KMeans(n_clusters=5)
    kmeans = kmeans.fit(data_list)
    labels = kmeans.predict(data_list)
    centroids = kmeans.cluster_centers_

    print('centroids are: \n', centroids)
    plot3d(data_list, labels)

    som = MiniSom(6 ,6, 4, sigma=0.5, learning_rate=0.5)
    som.train_random(data_list, 100)
    result1 = som.activation_response(data_list)
    print('result1 are: \n', result1)


main()